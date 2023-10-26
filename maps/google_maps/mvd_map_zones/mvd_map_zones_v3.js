async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
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
    strokeColor: '#FF0000',
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
    polygon.setOptions({ fillColor: '#FF0000' });

    // Find the data for the current zone from the API response
    const zoneData = apiData.rents.find(rent => rent.zona === name);

    if (zoneData) {
      infoWindow.setContent(`${name}<br>Number of rents: ${zoneData.cantidad}`);
    } else {
      infoWindow.setContent(name);
    }

    infoWindow.setPosition(polygonCenter);
    infoWindow.open(map);
  });

  // Add mouseout event listener
  polygon.addListener('mouseout', function() {
    polygon.setOptions({ fillColor: 'transparent' });
    infoWindow.close();
  });
}

initMap();
