import json
import os
from datetime import datetime
from urllib.request import urlopen, Request

from pyunpack import Archive

from shutil import copyfile

parent_dir = "../DemoManager"
temp_dir = os.path.join(parent_dir, "temp")


class Data:
    def __init__(self, demo, date, id, team1, team2, maps):
        self.demo = demo
        self.date = date
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.maps = maps


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
    Archive(filename).extractall(temp_dir)
    os.remove(filename)
    print("Demos were unarchived!")


def buildHierarchy(dt: Data):
    date_path = os.path.join(parent_dir, str(datetime.fromtimestamp(int(dt.date)).strftime("%d %m %Y")))

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

    with open("data.json", "r") as read_file:
        data_dict = json.load(read_file)

    count = 1
    for dt in data_dict:
        print("Processing match " + str(count) + " out of " + str(len(data_dict)))
        buildHierarchy(Data(**dt))
        count += 1

#ok dude


if __name__ == "__main__":
    main()
