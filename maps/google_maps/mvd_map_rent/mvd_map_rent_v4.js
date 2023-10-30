let allRentsData; // Variable to store the fetched data

async function fetchData() {
  const response = await fetch("https://alquivago-flask-apis.vercel.app/api/v1/rent/mapa/todo");
  allRentsData = await response.json();
  // Store the data in local storage
  localStorage.setItem("rentData", JSON.stringify(allRentsData));
}

// Check if data is already in local storage and fetch if not
if (localStorage.getItem("rentData")) {
  allRentsData = JSON.parse(localStorage.getItem("rentData"));
} else {
  fetchData();
}

async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker"); // Import AdvancedMarkerElement
  const map = new Map(document.getElementById("map"), {
    center: { lat: -34.8167, lng: -56.1833 }, // Peñarol - Zoom 12
    zoom: 12,
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

  const createInfoWindow = (position, content) => {
    // Create an InfoWindow to display price information
    const infoWindow = new google.maps.InfoWindow({
      position,
      content: `${content}<button onclick=alert('Hello')>Detalles</button>`, // Add the button inside the content
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
            createInfoWindow(
              {
                lat: rent.location.latitude,
                lng: rent.location.longitude,
              },
              priceInfo
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

initMap();