import json
import os
from datetime import datetime

from urllib.request import urlopen, Request

import requests

import patoolib

from shutil import copyfile

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parent_dir = "../DemoManager"
temp_dir = os.path.join(parent_dir, "temp")

class Data:
    def __init__(self, id, date, demo, maps, team1, team2):
        self.maps = []
        self.id = id
        self.date = date
        self.demo = "https://hltv.org" + demo
        self.team1 = team1
        self.team2 = team2
        for map in maps:
            if(map == "ovp"):
                self.maps.append("Overpass")
            elif (map == "nuke"):
                self.maps.append("Nuke")
            elif (map == "inf"):
                self.maps.append("Inferno")
            elif (map == "mrg"):
                self.maps.append("Mirage")
            elif (map == "vertigo"):
                self.maps.append("Vertigo")
            elif (map == "trn"):
                self.maps.append("Train")
            elif (map == "d2"):
                self.maps.append("Dust2")


def download(url):
    """
    Download demos archive via link.
    """
    try:
        print("Downloading demo: " + url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                          'Safari/537.3'}
        req = Request(url=url, headers=headers)
        file = urlopen(req).read()
        open(os.path.join(temp_dir, "demo.rar"), 'wb').write(file)
        print("Demo: " + url + "was downloaded!")
    except():
        print('Error occurred!')


def unarchive(filename):
    try:
        patoolib.extract_archive(archive=filename, outdir=temp_dir, program="/bin/7z")
    except:
        pass
    os.remove(filename)
    print("Demos were unarchived!")


def buildHierarchy(dt: Data):
    date_path = os.path.join(parent_dir, str(datetime.fromtimestamp(int(dt.date)/1000).strftime("%d %m %Y")))

    if not os.path.exists(date_path):
        os.mkdir(date_path)

    team1_path = os.path.join(date_path, dt.team1)
    team2_path = os.path.join(date_path, dt.team2)

    if not os.path.exists(team1_path):
        os.mkdir(team1_path)
    if not os.path.exists(team2_path):
        os.mkdir(team2_path)

    for map in dt.maps:
        team1_map_path = os.path.join(team1_path, map)
        team2_map_path = os.path.join(team2_path, map)
        if not os.path.exists(team1_map_path):
            os.mkdir(team1_map_path)
        if not os.path.exists(team2_map_path):
            os.mkdir(team2_map_path)

    download(dt.demo)
    unarchive(os.path.join(temp_dir, "demo.rar"))

    for dem in os.listdir(temp_dir):
        team1_map_path = os.path.join(team1_path, dem.split('-')[len(dem.split('-')) - 1].split('.')[0].capitalize())
        team2_map_path = os.path.join(team2_path, dem.split('-')[len(dem.split('-')) - 1].split('.')[0].capitalize())
        if not os.path.exists(os.path.join(team1_map_path, dem)) or not os.path.exists(
                os.path.join(team2_map_path, dem)):
            copyfile(os.path.join(temp_dir, dem), os.path.join(team1_map_path, dem))
            copyfile(os.path.join(temp_dir, dem), os.path.join(team2_map_path, dem))
        os.remove(os.path.join(temp_dir, dem))

    print("Demo was saved successfully!")


def main():
    if not os.path.exists("temp"):
        os.mkdir("temp")

    data_dict = requests.get("http://localhost:8000/api/team/Astralis").json()

    count = 1
    for dt in data_dict:
        print("Processing match " + str(count) + " out of " + str(len(data_dict)))
        maps = []
        for map in dt["maps"]:
            maps.append(map["map"])
        buildHierarchy(Data(int(dt["id"]), dt["date"], dt["demo"], maps, dt["team1"]["name"], dt["team2"]["name"]))
        count += 1

if __name__ == "__main__":
    main()
