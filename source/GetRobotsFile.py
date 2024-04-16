import urllib.robotparser


class GetRobotsFile:
    """
    Clase que realiza la petición al servivdor del archivo robots.txt
    """
    def __init__(self):
        """
        Inicializa la variable url
        """
        self.url = "https://www.ine.es/robots.txt"

    def get_robots_file(self):
        """
        Lee y analiza el archivo robots.txt para la URL proporcionada.

        Este método utiliza la biblioteca RobotFileParser de la librería urllib para leer
        y analizar el archivo robots.txt de la URL especificada. Imprime el resultado
        del análisis en la consola.

        :return:
        - None
        """
        print("Reading robots.txt")
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self.url)
        rp.read()
        print(rp)
