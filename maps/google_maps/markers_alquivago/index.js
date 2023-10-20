async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const map = new Map(document.getElementById("map"), {
    center: { lat: 37.4239163, lng: -122.0947209 },
    zoom: 14,
    mapId: "YOUR_MAP_ID", // Replace with your map ID
  });

  // Make an HTTP request to the API
  const apiUrl = 'https://alquivago-flask-apis.vercel.app/api/v1/rent/inmuebles';
  const response = await fetch(apiUrl);
  const data = await response.json();

  // Iterate through the rents and add markers for each valid location
  data.rents.forEach(rent => {
    const latitude = rent.location.latitude;
    const longitude = rent.location.longitude;

    // Check for valid latitude and longitude
    if (latitude && longitude) {
      const marker = new AdvancedMarkerElement({
        map,
        position: { lat: latitude, lng: longitude },
      });
    }
  });
}

initMap();
