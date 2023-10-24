async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const { Place } = await google.maps.importLibrary("places");
  const map = new Map(document.getElementById("map"), {
    center: { lat: -34.901112, lng: -56.164532 },
    zoom: 14,
    mapId: "16aaecb986532f9a",
  });

  let markers = []; // Store created markers in an array

  const handleZoomChange = () => {
    const zoom = map.getZoom();
    console.log(`Zoom level: ${zoom}`); // Log the zoom level

    // Remove existing markers from the map
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = []; // Clear the markers array

    if (zoom >= 14) {
      // Fetch data from the API endpoint
      fetch("https://alquivago-flask-apis.vercel.app/api/v1/rent/mapa")
        .then((response) => response.json())
        .then((data) => {
          if (data && data.rents && Array.isArray(data.rents)) {
            data.rents.forEach((rent) => {
              if (rent.location && rent.location.latitude && rent.location.longitude) {
                const glyphImg = document.createElement("img");
                let iconSrc;

                // Determine the icon source based on the "origin" field
                switch (rent.origin) {
                  case "gallito":
                    iconSrc = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/maps/maps/google_maps/assets/gallito_logo.svg";
                    break;
                  case "infocasas":
                    iconSrc = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/maps/maps/google_maps/assets/infocasas_logo.svg";
                    break;
                  case "mercado_libre":
                    iconSrc = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/maps/maps/google_maps/assets/mercado_libre_logo.svg";
                    break;
                  default:
                    // Use a default icon if "origin" doesn't match any of the cases
                    iconSrc = "default-icon-url.png";
                }

                glyphImg.src = iconSrc;
                glyphImg.width = 20;
                glyphImg.height = 20;

                // Create a marker with the determined icon source
                const glyphSvgPinElement = new PinElement({
                  glyph: glyphImg,
                });

                // Create a marker
                const marker = new AdvancedMarkerElement({
                  map,
                  position: {
                    lat: rent.location.latitude,
                    lng: rent.location.longitude,
                  },
                  content: glyphSvgPinElement.element,
                  title: rent.title,
                });

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

                // Create an InfoWindow to display price information
                const infoWindow = new google.maps.InfoWindow({
                  content: priceInfo,
                });

                // Open the InfoWindow by default for each marker
                infoWindow.open(map, marker);

                markers.push(marker); // Store the created marker in the array
              }
            });
          }
        });
    }
  };

  // Call the handler once after initializing the map
  handleZoomChange();

  // Listen for zoom changes
  map.addListener("zoom_changed", handleZoomChange);
}

initMap();
