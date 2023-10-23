async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const map = new Map(document.getElementById("map"), {
    center: { lat: -32.875, lng: -56.081 }, // Centered on Uruguay
    // center: { lat: 40.76, lng: -101.64 },
    zoom: 5,
    // In the cloud console, configure this Map ID with a style that enables the
    // "Administrative Area Level 1" feature layer.
    mapId: "7ba16be0c9375fa7",
  });
  const featureLayer = map.getFeatureLayer(
    google.maps.FeatureType.ADMINISTRATIVE_AREA_LEVEL_1,
  );

  featureLayer.style = (featureStyleFunctionOptions) => {
    const placeFeature = featureStyleFunctionOptions.feature;
    const population = departments[placeFeature.placeId];
    let fillColor;

    // Specify colors using any of the following:
    // * Named ('green')
    // * Hexadecimal ('#FF0000')
    // * RGB ('rgb(0, 0, 255)')
    // * HSL ('hsl(60, 100%, 50%)')
    if (population < 2000000) {
      fillColor = "green";
    } else if (population < 5000000) {
      fillColor = "red";
    } else if (population < 10000000) {
      fillColor = "blue";
    } else if (population < 40000000) {
      fillColor = "yellow";
    }
    return {
      fillColor,
      fillOpacity: 0.5,
    };
  };


  // Department data for Uruguay.
  const departments = {
    "ChIJ4xEAY4cLq5URyYKJJ1aNuac": "Artigas",
    "ChIJqYIp4ifdrZURxzunjKwP_Gg": "Salto",
    "ChIJX4glQez-qZUReu2MveeVK_I": "Rivera",
    "ChIJX37kV0HJr5URRaOzXA4OSKk": "Paysandú",
    "ChIJUxK0lWJOqJURQyyxmO8ugto": "Tacuarembó",
    "ChIJ1ajbONsmCZURfaNP1AXV6MI": "Cerro Largo",
    "ChIJYTYkGrhNpZURyHdFlNFmd6Q": "Río Negro",
    "ChIJd-vjFK7BppURtHTyHeA_mDs": "Durazno",
    "ChIJRdNj2hvpC5URhum1z8Bd3ck": "Treinta y Tres",
    "ChIJg08GaQ_8pJUR2YV-JSBJj2E": "Soriano",
    "ChIJC1-BgIqgppUR8Aa40TGLxFY": "Flores",
    "ChIJ35i6oLUCoZUR5c2hLwP0LS0": "Florida",
    "ChIJZxOLmie6CpURAktzUL_v_NU": "Lavalleja",
    "ChIJNyVtSfW7dJURftp5rMyj_B0": "Rocha",
    "ChIJ36qbnmgSo5URCIfPPwK4Bdg": "Colonia",
    "ChIJR-EJTpdwoZURIYEwIBJtHwU": "San José",
    "ChIJY_0npR-0oZUR9TAjDie8rg4": "Canelones",
    "ChIJsfolyZcadZUR_RWXUZXlOkw": "Maldonado",
    "ChIJ0_c7xv-An5URmexbNS4bMms": "Montevideo",
  };
}

initMap();
