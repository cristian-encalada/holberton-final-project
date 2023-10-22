async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const { Place } = await google.maps.importLibrary("places");
  const map = new Map(document.getElementById("map"), {
    center: { lat: 37.42475, lng: -122.0845 },
    zoom: 13,
    mapId: "4504f8b37365c3d0",
  });
  const parser = new DOMParser();
  // A marker with a with a URL pointing to a PNG.
  const beachFlagImg = document.createElement("img");

  beachFlagImg.src =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

  const beachFlagMarkerView = new AdvancedMarkerElement({
    map,
    position: { lat: 37.434, lng: -122.082 },
    content: beachFlagImg,
    title: "A marker using a custom PNG Image",
  });
  // A marker with a custom SVG glyph.
  const glyphImg = document.createElement("img");

  glyphImg.src =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/google_logo_g.svg";

  const glyphSvgPinElement = new PinElement({
    glyph: glyphImg,
  });
  const glyphSvgMarkerView = new AdvancedMarkerElement({
    map,
    position: { lat: 37.425, lng: -122.07 },
    content: glyphSvgPinElement.element,
    title: "A marker using a custom SVG for the glyph.",
  });
  // A marker customized using a place icon and color, name, and geometry.
  const place = new Place({
    id: "ChIJN5Nz71W3j4ARhx5bwpTQEGg",
  });

  // Call fetchFields, passing the desired data fields.
  await place.fetchFields({
    fields: [
      "location",
      "displayName",
      "svgIconMaskURI",
      "iconBackgroundColor",
    ],
  });

  const pinElement = new PinElement({
    background: place.iconBackgroundColor,
    glyph: new URL(String(place.svgIconMaskURI)),
  });
  const placeIconMarkerView = new AdvancedMarkerElement({
    map,
    position: place.location,
    content: pinElement.element,
    title: place.displayName,
  });
  // A marker using a Font Awesome icon for the glyph.
  const icon = document.createElement("div");

  icon.innerHTML = '<i class="fa fa-pizza-slice fa-lg"></i>';

  const faPin = new PinElement({
    glyph: icon,
    glyphColor: "#ff8300",
    background: "#FFD514",
    borderColor: "#ff8300",
  });
  const faMarker = new AdvancedMarkerElement({
    map,
    position: { lat: 37.412, lng: -122.095829650878 },
    content: faPin.element,
    title: "A marker using a FontAwesome icon for the glyph.",
  });
}

initMap();