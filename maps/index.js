// ########## Map 1. Initial map divided by zones #############

const zoneMapping = {
  "Ciudad Vieja": 1,
  "Centro": 2,
  "Barrio Sur": 3,
  "Cordón": 4,
  "Palermo": 5,
  "Parque Rodó": 6,
  "Punta Carretas": 7,
  "Pocitos": 8,
  "Buceo": 9,
  "Parque Batlle": 10,
  "Malvín": 11,
  "Malvín Norte": 12,
  "Punta Gorda": 13,
  "Carrasco": 14,
  "Carrasco Norte": 15,
  "Bañados de Carrasco": 16,
  "Maroñas": 17,
  "Flor de Maroñas": 18,
  "Las Canteras": 19,
  "Punta de Rieles": 20,
  "Jardines del Hipódromo": 21,
  "Ituzaingó": 22,
  "Unión": 23,
  "Villa Española": 24,
  "Mercado Modelo": 25,
  "Castro": 26,
  "Cerrito de la Victoria": 27,
  "Las Acacias": 28,
  "Aires Puros": 29,
  "Casavalle": 30,
  "Piedras Blancas": 31,
  "Manga": 32,
  "Paso de las Duranas": 33,
  "Peñarol": 34,
  "Villa del Cerro": 35,
  "Casabó": 36,
  "La Paloma": 37,
  "La Teja": 38,
  "Prado": 39,
  "Capurro": 40,
  "Aguada": 41,
  "Reducto": 42,
  "Atahualpa": 43,
  "Jacinto Vera": 44,
  "La Figurita": 45,
  "Larrañaga": 46,
  "La Blanqueada": 47,
  "Villa Muñoz": 48,
  "La Comercial": 49,
  "Tres Cruces": 50,
  "Brazo Oriental": 51,
  "Sayago": 52,
  "Conciliación": 53,
  "Belvedere": 54,
  "Nuevo París": 55,
  "Tres Ombúes": 56,
  "Paso de la Arena": 57,
  "Colón Sureste": 58,
  "Colón Centro y Noroeste": 59,
  "Lezica": 60,
  "Villa García": 61,
  "Manga": 62,
  "Villa Dolores": 63,
  "Parque Guaraní": 64,
  "Bella Italia": 65,
  "Bolívar": 66,
  "Marconi": 67,
  "Toledo Chico": 68,
  "Lavalleja": 69,
  "Pajas Blancas": 70,
  "Tomkinson": 71,
  "Nueva Savona": 72,
  "Bella Vista": 73,
  "Arroyo Seco": 74,
  "Retiro": 75,
  "Goes": 76,
  "Paso Molino": 77,
  "Pueblo Victoria": 78,
  "Santiago Vázquez": 79,
  "Abayubá": 80
};

async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  var map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: -34.86500, lng: -56.17861 }, // Montevideo - Zoom 12
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
    addPolygon(map, polygons[name], name, apiData, zoneMapping[name]);
  }
}

async function addPolygon(map, coordinates, name, apiData, zoneNumber) {
  const polygon = new google.maps.Polygon({
    paths: coordinates,
    strokeColor: 'black',
    strokeOpacity: 0.8,
    strokeWeight: 1,
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

  // Click event listener
  polygon.addListener('click', function() {
  const polygonCenter = bounds.getCenter();
  // Use the polygon's center coordinates for the clicked zone
  const centerCoordinates = { lat: polygonCenter.lat(), lng: polygonCenter.lng() };

  // Call initMap2 with the selected coordinates
  initMap2(centerCoordinates, zoneNumber); 
  });
}

// ########## Secondary Maps. After clicking over any zone #############


let allRentsData; // Variable to store the fetched data

async function fetchData() {
  const response = await fetch("https://alquivago-flask-apis.vercel.app/api/v1/rent/mapa/1");
  allRentsData = await response.json();
}


async function initMap2(centerCoordinates, zoneNumber) {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  // API URL using the zoneNumber
  const apiUrl = `https://alquivago-flask-apis.vercel.app/api/v1/rent/mapa/${zoneNumber}`;
  const response = await fetch(apiUrl);
  allRentsData = await response.json();
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker"); // Import AdvancedMarkerElement
  const map = new Map(document.getElementById("map"), {
    center: centerCoordinates,
    zoom: 14,
    mapId: "16aaecb986532f9a",
  });

  // "Mapa por Zonas" button
  const mainMapButton = document.createElement('button');
  mainMapButton.textContent = 'Mapa por Zonas';
  mainMapButton.style.position = 'absolute';
  mainMapButton.style.top = '10px'; // Adjust the top position as needed
  mainMapButton.style.left = '50%'; // Center horizontally
  mainMapButton.style.zIndex = '1';
  mainMapButton.style.backgroundColor = 'white';
  mainMapButton.style.padding = '5px';
  mainMapButton.style.border = '1px solid #ccc';
  mainMapButton.style.cursor = 'pointer';

  // Add the button to the map container
  const mapContainer = document.getElementById("map");
  mapContainer.appendChild(mainMapButton);

  // Add an event listener to the "Main Map" button to call initMap()
  mainMapButton.addEventListener('click', () => {
    // Remove the button
    mainMapButton.remove();
    
    // Call initMap() to return to the main map
    initMap();
  });

  let markers = []; // Store created markers in an array

  function createBlueCircleMarker(position) {
    // Create blue circle markers
    const blueCircleSvgString = '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 20 20"><circle cx="10" cy="10" r="8" fill="red" /></svg>';
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

    if (zoom >= 14) {
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
    } else if (zoom < 14) {
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
