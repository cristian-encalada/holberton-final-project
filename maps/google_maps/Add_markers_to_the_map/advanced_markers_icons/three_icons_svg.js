async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const { Place } = await google.maps.importLibrary("places");
  const map = new Map(document.getElementById("map"), {
    center: { lat: -34.901112, lng: -56.164532 },
    // center: { lat: 37.42475, lng: -122.0845 },
    zoom: 13,
    mapId: "4504f8b37365c3d0",
  });
  const parser = new DOMParser();
  // A marker with a custom SVG glyph.
  const glyphImg = document.createElement("img");

  glyphImg.src =
    "https://raw.githubusercontent.com/cristian-encalada/Alquivago/maps/maps/google_maps/assets/MELI_24px.svg";

  const glyphSvgPinElement = new PinElement({
    glyph: glyphImg,
  });
  const glyphSvgMarkerView = new AdvancedMarkerElement({
    map,
    position: { lat: -34.9007063, lng: -56.1829068 },
    content: glyphSvgPinElement.element,
    title: "Apartment in rent. Montevideo.",
  });
}

initMap();