# Web scraping de infocasas

instalar:
```
pip install tqdm
pip install selenium
```

* antes que nada iniciar docker desktop
* docker-compose es un archivo .yml para correr selenium-chrome.
* por ejemplo tengo un archivo docker-compose.yml en mi escritorio (que tiene el codigo que se ve abajo)

```
version: '3.3'
services:
  chrome:
      image: selenium/standalone-chrome:latest
      shm_size: 2gb
      container_name: selenium-chrome
      environment:
        - SE_NODE_MAX_SESSIONS=5
        - SE_NODE_SESSION_TIMEOUT=30
        - SE_VNC_NO_PASSWORD=1
      restart: always
      ports:
        - "4444:4444"
```

* para crear la imagen tengo que ejecutar este comando: docker-compose up -d --build
* (docker-compose sin la extension .yml)
* usar -d para modo demonio

```
PS C:\Users\martin\Desktop> docker-compose up -d --build
[+] Running 35/1
 ✔ chrome 34 layers [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled                      23.1s
[+] Running 2/2
 ✔ Network desktop_default    Created                                                                              0.5s
 ✔ Container selenium-chrome  Started                                                                              1.4s
```

* una vez creado el container veo que el servicio esta arriba en la ruta " http://localhost:4444/ " ahora puedo ejecutar mi script de automatizacion (usar a partir de la version "S_infocasas_d00.py")