# Alquivago - Flask API v1

## Local environment

## Pre-requisites

Install [flasgger](https://pypi.org/project/flasgger/0.5.4/) python library (Ubuntu):

```
pip install flasgger
```

Execute this command fron the directory `/api/v1`:

```sh
flask run
```

### Output:

```sh
[cristian@Arch v1]$ flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Local URLs:

__Flasgger UI__

```sh
http://127.0.0.1:5000/apidocs/#/
```

![Flasgger UI](/api/handlers/documentation/readme_screenshots/Flassger_URL.png)

__Request API example:__


![API endpoit request](/api/handlers/documentation/readme_screenshots/Rents_get_all_request.png)


Response sample data:

```JSON
{
  "entries_per_page": 10,
  "filters": {},
  "page": 1,
  "rents": [
    {
      "bathrooms": 75,
      "bedrooms": 1,
      "currency": "UYU",
      "id": "gallito_24480704",
      "images": [
        "https://imagenes.gallito.com/1024x768/231012125348810.jpg",
        "https://imagenes.gallito.com/1024x768/231012125353020.jpg",
        "https://imagenes.gallito.com/1024x768/231012125356860.jpg",
        "https://imagenes.gallito.com/1024x768/231012125401440.jpg",
        "https://imagenes.gallito.com/1024x768/231012125407170.jpg",
        "https://imagenes.gallito.com/1024x768/231012125413910.jpg",
        "https://imagenes.gallito.com/1024x768/231012125421440.jpg",
        "https://imagenes.gallito.com/1024x768/231012125429360.jpg"
      ],
      "location": {
        "latitude": -34.8554022,
        "longitude": -56.2212867
      },
      "operation_type": "Alquiler",
      "origin": "gallito",
      "price": 32000,
      "property_type": "Local",
      "state_name": "Montevideo",
      "title": "ZONA COMERCIAL",
      "total_area": 0,
      "url_link": "https://www.gallito.com.uy/zona-comercial-inmuebles-24480704",
      "zone_name": "Paso Molino"
    },
    {
      "bathrooms": 1,
      "bedrooms": 2,
      "currency": "UYU",
      "id": "gallito_24480929",
      "images": [
        "https://imagenes.gallito.com/1024x768/231012142621270.jpg",
        "https://imagenes.gallito.com/1024x768/231012142621550.jpg",
        "https://imagenes.gallito.com/1024x768/231012142621110.jpg",
        "https://imagenes.gallito.com/1024x768/231012142622660.jpg",
        "https://imagenes.gallito.com/1024x768/231012142622130.jpg",
        "https://imagenes.gallito.com/1024x768/231012142623170.jpg",
        "https://imagenes.gallito.com/1024x768/231012142622890.jpg",
        "https://imagenes.gallito.com/1024x768/231012142622300.jpg",
        "https://imagenes.gallito.com/1024x768/231012142622500.jpg",
        "https://imagenes.gallito.com/1024x768/231012142621770.jpg",
        "https://imagenes.gallito.com/1024x768/231012142621950.jpg",
        "https://imagenes.gallito.com/1024x768/231012142623450.jpg"
      ],
      ...
        "total_results": 145
}
```

__Direct API endpoints__

http://127.0.0.1:5000/api/v1/

http://127.0.0.1:5000/api/v1/filtro


## Live URLs (Vercel deployment)

API endpoints available in v1:

* https://alquivago-flask-apis.vercel.app/api/v1/

* https://alquivago-flask-apis.vercel.app/api/v1/filtro