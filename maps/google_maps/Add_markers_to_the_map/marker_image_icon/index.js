// This example adds a custom marker to indicate the position of a rental property,
// published at Mercado Libre
// Montevideo/Uruguay.
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: -34.901112, lng: -56.164532 },
    // center: { lat: -33, lng: 151 },
  });
  const image = {
    url: "https://github.com/cristian-encalada/Alquivago/blob/main/vite-project/src/assets/mercadolibre-logo.png?raw=true",
    scaledSize: new google.maps.Size(32, 32),
  };
  const mluMarker = new google.maps.Marker({
    position: { lat: -34.9007063, lng: -56.1829068 },
    map,
    icon: image,
  });
}

window.initMap = initMap;