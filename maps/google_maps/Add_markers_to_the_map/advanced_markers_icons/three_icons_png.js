async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const { Place } = await google.maps.importLibrary("places");
  const map = new Map(document.getElementById("map"), {
    // center: { lat: 37.42475, lng: -122.0845 },
    center: { lat: -34.901112, lng: -56.164532 },
    zoom: 13,
    mapId: "4504f8b37365c3d0",
  });
  const parser = new DOMParser();
  // A marker with a with a URL pointing to a PNG.
  const beachFlagImg = document.createElement("img");

  beachFlagImg.src =
    "https://github.com/cristian-encalada/Alquivago/blob/main/vite-project/src/assets/mercadolibre-logo.png?raw=true";

  // Set the width and height of the image to 32x32 pixels
  beachFlagImg.width = 32;
  beachFlagImg.height = 32;

  const beachFlagMarkerView = new AdvancedMarkerElement({
    map,
    // position: { lat: 37.434, lng: -122.082 },
    position: { lat: -34.9007063, lng: -56.1829068 },
    content: beachFlagImg,
    title: "A marker using a custom PNG Image",
  });
}

initMap();