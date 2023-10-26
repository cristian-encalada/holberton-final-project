async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const map = new Map(document.getElementById("map"), {
    center: { lat: -32.875, lng: -56.081 }, // Centered on Uruguay
    // center: { lat: 40.76, lng: -101.64 },  // Centered on U.S.A.
    zoom: 7,
    // In the cloud console, configure this Map ID with a style that enables the
    // "Administrative Area Level 1" feature layer.
    mapId: "7ba16be0c9375fa7",
  });
  const featureLayer = map.getFeatureLayer(
    google.maps.FeatureType.ADMINISTRATIVE_AREA_LEVEL_1,
  );

  featureLayer.style = (featureStyleFunctionOptions) => {
    const placeFeature = featureStyleFunctionOptions.feature;
    const population = departamentos[placeFeature.placeId];
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

  // Population data by departments.
  const departamentos = {
    "ChIJAQrGD-ALq5URGiJ4JwEwfHg": 5039877,  // Artigas
    "ChIJqYIp4ifdrZURPwLSqN75meQ": 732673,  // Salto
    "ChIJGX5yn_ebB5URVDinSCrYVXc": 7276316,  // Rivera
    "ChIJ4SVCmDger5URu49wLO-7UNM": 5025891,  // Paysandú
    "ChIJtTam1oD2B5URXQz07SpL7h4": 39237836,  // Tacuarembó
    "ChIJ1ajbONsmCZURfaNP1AXV6MI": 581206,  // Cerro Largo
    "ChIJYTYkGrhNpZURyHdFlNFmd6Q": 3605597,  // Río Negro
    "ChIJd-vjFK7BppURqzdD1Y2Rcgk": 5039877,  // Durazno
    "ChIJbW656ReYCZURkgxYn9LpVLA": 3193079,  // Treinta y Tres
    "ChIJg08GaQ_8pJUR2YV-JSBJj2E": 10799566,  // Soriano
    "ChIJC1-BgIqgppUR8Aa40TGLxFY": 1441553,  // Flores
    "ChIJ_2f_hbzAoJURzlkiVuDLtGM": 12671469,  // Florida
    "ChIJZxOLmie6CpURAktzUL_v_NU": 1900923,  // Lavalleja
    "ChIJffMb7ZqmDJUR8G5RiV1Y84c": 5039877,  // Rocha
    "ChIJOXYdHPazpJURFB8kenSpdbA": 3193079,  // Colonia
    "ChIJR-EJTpdwoZURIYEwIBJtHwU": 5934582,  // San José
    "ChIJsfhxHBCSn5URykFCIfGFQno": 4509394,  // Canelones
    "ChIJmy_r7joHdZURKAxEmlmmpH0": 39237836,  // Maldonado
    "ChIJ0_c7xv-An5URZKZVcui9b2g": 1372247,  // Montevideo
  };
}

initMap();