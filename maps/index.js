// ########## Map 1. Initial map divided by zones #############

async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  var map = new google.maps.Map(document.getElementById('map'), {
    // center: { lat: -34.901112, lng: -56.164532 }, // Montevideo
    // center: { lat: -34.86574, lng: -56.17798 }, // Brazo Oriental - Zoom 13
    center: { lat: -34.8167, lng: -56.1833 }, // Peñarol - Zoom 12
    zoom: 12
  });

  // Fetch the coordinates from 'mvd_coordinates' CSV file
  const response = await fetch('mvd_coordinates.csv');
  const text = await response.text();
  const rows = text.split('\n');

  const polygons = {};
  let currentPolygon = null;

  rows.forEach(row => {
    const [name, lat, lng] = row.split(',');
    if (!polygons[name]) {
      polygons[name] = [];
      currentPolygon = name;
    }
    polygons[currentPolygon].push({ lat: parseFloat(lat), lng: parseFloat(lng) });
  });

  // Fetch data from the API endpoint
  const apiResponse = await fetch('https://alquivago-flask-apis.vercel.app/api/v1/rent/conteo_zona');
  const apiData = await apiResponse.json();

  for (const name in polygons) {
    addPolygon(map, polygons[name], name, apiData);
  }
}

async function addPolygon(map, coordinates, name, apiData) {
  const polygon = new google.maps.Polygon({
    paths: coordinates,
    strokeColor: '#0000FF',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: 'transparent',
    fillOpacity: 0.35
  });

  polygon.setMap(map);

  // Create an InfoWindow
  const infoWindow = new google.maps.InfoWindow();

  // Calculate the center of the polygon
  const bounds = new google.maps.LatLngBounds();
  coordinates.forEach(coord => bounds.extend(new google.maps.LatLng(coord.lat, coord.lng)));
  const polygonCenter = bounds.getCenter();

  // Add mouseover event listener
  polygon.addListener('mouseover', async function() {
    polygon.setOptions({ fillColor: '#0000FF' });

    // Find the data for the current zone from the API response
    const zoneData = apiData.rents.find(rent => rent.zona === name);

    if (zoneData) {
      infoWindow.setContent(`${name}<br>Alquileres: ${zoneData.cantidad}`);
    } else {
      infoWindow.setContent(`${name}<br>Alquileres: 0`);
    }

    infoWindow.setPosition(polygonCenter);
    infoWindow.open(map);
  });

  // Add mouseout event listener
  polygon.addListener('mouseout', function() {
    polygon.setOptions({ fillColor: 'transparent' });
    infoWindow.close();
  });

  // Add click event listener
  polygon.addListener('click', function() {
    const polygonCenter = bounds.getCenter();
    alert(`Polygon Name: ${name}\nCenter: Lat ${polygonCenter.lat()}, Lng ${polygonCenter.lng()}`);
  });
}

// ########## Secondary Maps. After clicking over any zone #############


let allRentsData; // Variable to store the fetched data

async function fetchData() {
  const response = await fetch("https://alquivago-flask-apis.vercel.app/api/v1/rent/mapa/1");
  allRentsData = await response.json();
  // initMap2(); // Call the initMap2 function after fetching the data
}

async function initMap2() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker"); // Import AdvancedMarkerElement
  const map = new Map(document.getElementById("map"), {
    center: { lat: -34.906698, lng: -56.2076854 }, // Ciudad Vieja - Montevideo
    zoom: 15,
    mapId: "16aaecb986532f9a",
  });

  let markers = []; // Store created markers in an array

  function createBlueCircleMarker(position) {
    // Create blue circle markers
    const blueCircleSvgString = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="blue" /></svg>';
    const blueCircleSvg = new DOMParser().parseFromString(blueCircleSvgString, "image/svg+xml").documentElement;

    const marker = new AdvancedMarkerElement({
      map,
      position,
      content: blueCircleSvg,
      title: "Zoom in to check the price",
    });

    markers.push(marker); // Store the created marker in the array
  }

  const infoWindows = []; // Store created InfoWindows in an array

  const createInfoWindow = (position, priceInfo, url_link, origin, zone) => {
    // Create an InfoWindow to display price information and URL link
    const content = `<div><strong>${priceInfo}</strong></div>
      <div onmouseover="(() => {
        if (!this.hasAppendedLink) {
          var linkDiv = document.createElement('div');
          var link = document.createElement('a');
          link.href = '${url_link}';
          link.target = '_blank'; // Open the URL in a new tab
          link.textContent = 'URL: ${url_link}';
          linkDiv.appendChild(link);
          this.appendChild(linkDiv);
          var originDiv = document.createElement('div');
          originDiv.textContent = 'Fuente: ${origin}';
          this.appendChild(originDiv);
          var zoneDiv = document.createElement('div');
          zoneDiv.textContent = 'Zona: ${zone}';
          this.appendChild(zoneDiv);
          this.hasAppendedLink = true; // Set the flag to true to prevent further appends
        }
      })()">Ver detalles</div>`;
    const infoWindow = new google.maps.InfoWindow({
      position,
      content: content,
      disableAutoPan: true, // Disable automatic centering
    });

    // Open the InfoWindow by default
    infoWindow.open(map);

    infoWindows.push(infoWindow); // Store the created InfoWindow in the array
  };

  const handleZoomChange = () => {
    const zoom = map.getZoom();
    console.log(`Zoom level: ${zoom}`); // Log the zoom level

    // Close existing InfoWindows
    infoWindows.forEach((infoWindow) => {
      infoWindow.close();
    });
    infoWindows.length = 0; // Clear the InfoWindows array

    // Remove existing markers from the map
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers.length = 0; // Clear the markers array

    if (zoom >= 16) {
      if (allRentsData && allRentsData.rents) {
        allRentsData.rents.forEach((rent) => {
          if (rent.location && rent.location.latitude && rent.location.longitude) {
            // Determine the price format based on the currency
            let priceInfo;
            if (rent.currency === "UYU") {
              priceInfo = `<div><strong>$ ${rent.price} ${rent.currency}</strong></div>`;
            } else if (rent.currency === "USD") {
              priceInfo = `<div><strong>U$S ${rent.price} ${rent.currency}</strong></div>`;
            } else {
              // Use a default format if currency is neither UYU nor USD
              priceInfo = `<div><strong>${rent.price} ${rent.currency}</strong></div>`;
            }
            let url_link;
            url_link = rent.url_link;
            let origin;
            origin = rent.origin;
            let zone;
            zone = rent.zone_name;
            createInfoWindow(
              {
                lat: rent.location.latitude,
                lng: rent.location.longitude,
              },
              priceInfo,
              url_link,
              origin,
              zone
            );
          }
        });
      }
    } else if (zoom < 16) {
      if (allRentsData && allRentsData.rents) {
        allRentsData.rents.forEach((rent) => {
          if (rent.location && rent.location.latitude && rent.location.longitude) {
            // Create a blue circle marker for each item
            createBlueCircleMarker({
              lat: rent.location.latitude,
              lng: rent.location.longitude,
            });
          }
        });
      }
    }
  };

  // Call the handler once after initializing the map
  handleZoomChange();

  // Listen for zoom changes
  map.addListener("zoom_changed", handleZoomChange);
}

// Call fetchData to fetch data from the API when the script loads
fetchData();


initMap();
