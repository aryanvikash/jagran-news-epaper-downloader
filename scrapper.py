import requests
import re
import os
import threading


url = "https://epaper.jagran.com/epaper/04-Feb-2022-84-Patna-Nagar-edition-Patna-Nagar.html"


def writeToPng(image,  city):
    pageno = re.findall(r"-pg(\d*)", image)[-1]
    with open(f"images/{city}/{pageno}.png", "wb") as file:
        response = requests.get(image)
        file.write(response.content)


def extarctImageUrls():
    response = requests.get(url)
    html = response.text

    matcheWithotCity = re.findall(r'http.*/M-.*-pg\d.*\.png', html)
    city = re.search(r"http.*EpaperImages\/\d*\/(.*)\/M",
                     matcheWithotCity[0]).group(1)

    regex = fr'http.*{str(city)}.*/M-.*-pg\d.*\.png'

    matches = set(re.findall(regex, html))

    os.makedirs(f"images/{city}", exist_ok=True)
    print(f"Total {len(matches)} page Found for city {city}")
    print(f"Please wait Trying To download all images...")
    for image in matches:
        threading.Thread(target=writeToPng, args=(image,  city)).start()
    print("Download Complete !!")


extarctImageUrls()
