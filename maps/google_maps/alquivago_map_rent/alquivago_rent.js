async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const { Place } = await google.maps.importLibrary("places");
  const map = new Map(document.getElementById("map"), {
    center: { lat: -34.901112, lng: -56.164532 },
    zoom: 13,
    mapId: "4504f8b37365c3d0",
  });

  // Fetch data from the API endpoint
  const response = await fetch("https://alquivago-flask-apis.vercel.app/api/v1/rent/inmuebles");
  const data = await response.json();

  if (data && data.rents && Array.isArray(data.rents)) {
    // Filter data for "origin" equal to "gallito"
    const gallitoData = data.rents.filter((rent) => rent.origin === "gallito");

    // Create markers for each location
    gallitoData.forEach((rent) => {
      if (rent.location && rent.location.latitude && rent.location.longitude) {
        // Create an SVG icon
        const glyphImg = document.createElement("img");
        glyphImg.src = "https://raw.githubusercontent.com/cristian-encalada/Alquivago/maps/maps/google_maps/assets/MELI_24px.svg";
        const glyphSvgPinElement = new PinElement({
          glyph: glyphImg,
        });

        // Create a marker
        new AdvancedMarkerElement({
          map,
          position: {
            lat: rent.location.latitude,
            lng: rent.location.longitude,
          },
          content: glyphSvgPinElement.element,
          title: rent.title,
        });
      }
    });
  }
}

initMap();
