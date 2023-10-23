let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Map options
  var options = {
    // Montevideo lat/long
    center: { lat: -34.901112, lng: -56.164532 },
    /*
    The following list shows the approximate level of detail to expect to see at each zoom level:
        1: World
        5: Landmass/continent
        10: City
        15: Streets
        20: Buildings
    */
    zoom: 12,
  }

  // New map
  map = new Map(document.getElementById("map"), options);

  
}

initMap();