# Web scraping

instalar pip:
```
sudo apt update
sudo apt install python3-pip
```
instalar selenium:
```
pip install selenium
```

docker:
docker-compose -f .\docker-compose.yml up -d --build
```
PS C:\Users\martin\Desktop\SeleniumHub> docker-compose -f .\docker-compose.yml up -d --build 
[+] Running 4/4
 ✔ Network seleniumhub_default      Created                                                                                                                                                                                               0.6s 
 ✔ Container selenium-hub           Started                                                                                                                                                                                               0.0s 
 ✔ Container seleniumhub-chrome-1   Started                                                                                                                                                                                               0.0s 
 ✔ Container seleniumhub-firefox-1  Started                                                                                                                                                                                               0.0s
```
docker-compose down
```
PS C:\Users\martin\Desktop\SeleniumHub> docker-compose down
[+] Running 4/4
 ✔ Container seleniumhub-chrome-1   Removed                                                                                                                                                                                               4.3s 
 ✔ Container seleniumhub-firefox-1  Removed                                                                                                                                                                                               4.5s 
 ✔ Container selenium-hub           Removed                                                                                                                                                                                               1.9s 
 ✔ Network seleniumhub_default      Removed
```  

* visualizar Selenium Grid en local: 127.0.0.1:4444
