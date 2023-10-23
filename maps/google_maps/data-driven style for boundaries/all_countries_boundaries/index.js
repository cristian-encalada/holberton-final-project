async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const mapDiv = document.getElementById("map")
  const options = {
    center: { lat: -32.875, lng: -56.081 }, // Centered on Uruguay
    // center: { lat: 40.76, lng: -101.64 },  // Centered on U.S.A.
    zoom: 7,
    mapId: "16aaecb986532f9a",
  };
  const map = new google.maps.Map(mapDiv, options);
  const countryLayer = map.getFeatureLayer(google.maps.FeatureType.COUNTRY);
  countryLayer.style = {
    // 'fillColor': 'yellow',
    'fillOpacity': 0.1,
    'strokeColor' : 'blue',
    // 'strokeOpacity': 0.5,
    'strokeWeight': 1
  }
};

initMap();
