import urllib.robotparser


class GetRobotsFile:

    def __init__(self):
        self.url = "https://www.ine.es/robots.txt"

    def get_robots_file(self):
        print("Reading robots.txt")
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self.url)
        rp.read()
        print(rp)
