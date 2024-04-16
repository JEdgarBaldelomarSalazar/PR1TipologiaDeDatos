import sys
from ProcessPage import ProcessPage
from GetRobotsFile import GetRobotsFile


def main() -> int:
    robot_files = GetRobotsFile()
    robot_files.get_robots_file()
    process_page = ProcessPage()
    process_page.process_page()
    return 0

if __name__ == "__main__":
    sys.exit(main())
