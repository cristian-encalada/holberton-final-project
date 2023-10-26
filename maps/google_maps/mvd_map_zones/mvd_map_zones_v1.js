async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  var map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -34.901112, lng: -56.164532 },
      zoom: 12
  });

  var ciudadViejaCoordinates = [
    { lat: -34.910648, lng: -56.200458 },
    { lat: -34.910211, lng: -56.204658 },
    { lat: -34.911703, lng: -56.210773 },
    { lat: -34.909839, lng: -56.214195 },
    { lat: -34.906343, lng: -56.215283 },
    { lat: -34.901569, lng: -56.202808 },
    { lat: -34.905723, lng: -56.201064 },
    { lat: -34.908468, lng: -56.200126 },
    { lat: -34.910648, lng: -56.200458 }
  ];

  var tresCrucesCoordinates = [
    { lat: -34.893296, lng: -56.171464 },
    { lat: -34.893102, lng: -56.168894 },
    { lat: -34.891996, lng: -56.168999 },
    { lat: -34.891924, lng: -56.167647 },
    { lat: -34.890870, lng: -56.167755 },
    { lat: -34.890779, lng: -56.166661 },
    { lat: -34.889844, lng: -56.166787 },
    { lat: -34.889671, lng: -56.165438 },
    { lat: -34.889409, lng: -56.165461 },
    { lat: -34.886292, lng: -56.163870 },
    { lat: -34.889512, lng: -56.160370 },
    { lat: -34.891906, lng: -56.158848 },
    { lat: -34.894898, lng: -56.165133 },
    { lat: -34.902133, lng: -56.164305 },
    { lat: -34.901929, lng: -56.165136 },
    { lat: -34.902079, lng: -56.169085 },
    { lat: -34.900410, lng: -56.169251 },
    { lat: -34.897041, lng: -56.171130 },
    { lat: -34.893297, lng: -56.171467 }
  ];

  addPolygon(map, ciudadViejaCoordinates);
  addPolygon(map, tresCrucesCoordinates);
}

function addPolygon(map, coordinates) {
  var polygon = new google.maps.Polygon({
      paths: coordinates,
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35
  });

  polygon.setMap(map);
}

initMap();
