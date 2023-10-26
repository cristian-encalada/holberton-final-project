async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  var map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -34.901112, lng: -56.164532 },
      zoom: 13
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

  for (const name in polygons) {
    addPolygon(map, polygons[name]);
  }
}

function addPolygon(map, coordinates) {
  var polygon = new google.maps.Polygon({
      paths: coordinates,
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: 'transparent',
      fillOpacity: 0.35
  });

  polygon.setMap(map);

  // mouseover and mouseout event listeners
  polygon.addListener('mouseover', function() {
    polygon.setOptions({ fillColor: '#FF0000' });
  });

  polygon.addListener('mouseout', function() {
    polygon.setOptions({ fillColor: 'transparent' });
  
  });

}

initMap();