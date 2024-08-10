import os
import requests


class FileDownloader:
    """Clase para descargar archivos desde URLs y guardarlos localmente.

    Attributes:
        directorio (str): Directorio de destino donde se guardarán los archivos descargados.
    """

    def __init__(self, directorio_destino):
        """Inicializa el FileDownloader con un directorio de destino.

        Args:
            directorio_destino (str): Ruta del directorio donde se almacenarán los archivos descargados.
        """
        self.directorio = directorio_destino
        self._crear_directorio()

    def _crear_directorio(self):
        """Crea el directorio de destino si no existe."""
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)

    def descargar_archivo(self, url):
        """Descarga un único archivo desde una URL especificada y lo guarda en el directorio de destino.

        Args:
            url (str): La URL del archivo que se desea descargar.

        Raises:
            Exception: Captura cualquier excepción durante la solicitud HTTP o la escritura del archivo e
                        informa del error.
        """
        try:
            respuesta = requests.get(url)
            nombre_archivo = url.split('/')[-1]
            ruta_completa = os.path.join(self.directorio, nombre_archivo)
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"Archivo {nombre_archivo} descargado en {ruta_completa}.")
        except Exception as e:
            print(f"Error al descargar el archivo {url}: {e}")

    def filtrar_descargar_archivos(self, urls, tipos_archivos=["all"]):
        """Filtra y descarga archivos de una lista de URLs según la extensión especificada.

        Args:
            urls (list): Lista de URLs de archivos a descargar.
            tipos_archivos (list): Tipos de archivos a descargar, una lista de extensiones o
                                    "all" para descargar todos los archivos.
        """
        if tipos_archivos == ["all"]:
            for url in urls:
                self.descargar_archivo(url)
        else:
            for url in urls:
                if any(url.endswith(f".{tipo}") for tipo in tipos_archivos):
                    self.descargar_archivo(url)