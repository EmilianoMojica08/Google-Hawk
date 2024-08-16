import os
import sys
import argparse
from googlesearch import GoogleSearch
from results_parsey import ResultsProcessor
from file_downloader import FileDownloader
from ia_agent import OpenAIGenerator, GPT4AllGenerator, IAagent
from dotenv import load_dotenv, set_key


def env_config():
    """
    Solicita al usuario la API KEY de Google y el ID del buscador personalizado
    y actualiza o crea un archivo .env con estos valores.
    """
    api_key = input("Introduce tu API KEY de Google: ")
    engine_id = input("Introduce el ID del buscador personalizado de Google: ")
    set_key(".env", "API_KEY_GOOGLE", api_key)
    set_key(".env", "SEARCH_ENGINE_ID", engine_id)
    print("Archivo .env configurado satisfactoriamente.")

def openai_config():
    """
    Solicita al usuario su API KEY de OpenAI y guarda este valor en el archivo .env.
    """
    api_key = input("Introduce la API KEY de OpenAI: ")
    set_key(".env", "OPENAI_API_KEY", api_key)
    print("Archivo .env configurado satisfactoriamente.")

def main(query, configure_env, start_page, pages, lang, output_json, output_html, download, gen_dork):
    """
    Realiza una búsqueda en Google utilizando una API KEY y un SEARCH ENGINE ID almacenados en un archivo .env.

    Args:
        query (str): Consulta de búsqueda que se realizará en Google.
        configure_env (bool): Si es True, se solicita configurar el .env. 
        start_page (int): Página inicial de los resultados de búsqueda. 
        pages (int): Número de páginas de resultados a retornar.
        lang (str): Código de idioma para los resultados de búsqueda.
        output_json (str): Ruta del archivo para exportar los resultados en formato JSON.
        output_html (str): Ruta del archivo para exportar los resultados en formato HTML.
        download (str): Cadena con extensiones de archivo para descargar, separadas por comas.
        gen_dork (str): Descripción para generar un dork automáticamente usando IA.
    """
    # Verificar la existencia del archivo .env y configuración del entorno
    if configure_env or not os.path.exists(".env"):
        env_config()
        sys.exit(1)

    # Cargar las variables de entorno
    load_dotenv()

    # Extraer valores de las variables de entorno
    google_api_key = os.getenv("API_KEY_GOOGLE")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    # Si se solicita generar un dork utilizando inteligencia artificial
    if gen_dork:
        # Solicitar confirmación para usar OpenAI
        respuesta = ""
        while respuesta.lower() not in ("y", "yes", "n", "no"):
            respuesta = input("¿Quieres utilizar GPT-4 de OpenAI? (yes/no): ")

        if respuesta.lower() in ("y", "yes"):
            # Configurar OpenAI si no está ya configurado
            if "OPENAI_API_KEY" not in os.environ:
                openai_config()
                load_dotenv()  # Recargar variables de entorno
            openai_gen = OpenAIGenerator()
            ia_agent = IAagent(openai_gen)
        else:
            # Utilizar una generación local si el usuario prefiere no usar OpenAI
            print("Utilizando GPT4All y ejecutando la generación en local. Puede tardar varios minutos...")
            gpt4all_generator = GPT4AllGenerator()
            ia_agent = IAagent(gpt4all_generator)

        # Generar y mostrar el dork
        respuesta = ia_agent.generate_gdork(gen_dork)
        print(f"\nResultado:\n {respuesta}")
        sys.exit(1)  # Finaliza después de generar el dork

    # Verificar la disponibilidad de las claves de API
    if not google_api_key or not search_engine_id:
        print("ERROR: Falta la API_KEY o el SEARCH_ENGINE_ID. Por favor, ejecuta la opción --configure para configurar el archivo .env.")
        sys.exit(1)

    # Verificar la presencia de una consulta
    if not query:
        print("Indica una consulta con el comando -q. Utiliza el comando -h para mostrar la ayuda.")
        sys.exit(1)

    # Realizar la búsqueda en Google
    gsearch = GoogleSearch(google_api_key, search_engine_id)
    resultados = gsearch.search(query, start_page=start_page, pages=pages, lang=lang)

    rparser = ResultsProcessor(resultados)

    # Mostrar los resultados en la línea de comandos
    rparser.mostrar_pantalla()

    # Exportar resultados en formato HTML si se especifica
    if output_html:
        rparser.exportar_html(output_html)

    # Exportar resultados en formato JSON si se especifica
    if output_json:
        rparser.exportar_json(output_json)

    # Descarga los documentos especificados que se encuentren en los resultados
    if download:
        file_types = download.split(",")
        urls = [resultado['link'] for resultado in resultados]
        fdownloader = FileDownloader("Descargas")
        fdownloader.filtrar_descargar_archivos(urls, file_types)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Esta herramienta permite realizar Hacking con buscadores de manera automática.")
    parser.add_argument("-q", "--query", type=str, help="Especifica el dork que deseas buscar.")
    parser.add_argument("-c", "--configure", action="store_true", help="Inicia el proceso para configurar o actualizar el archivo .env.")
    parser.add_argument("--start-page", type=int, default=1, help="Define la página de inicio del buscador para obtener los resultados.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas de resultados a retornar.")
    parser.add_argument("--lang", type=str, default="lang_es", help="Código de idioma para los resultados de búsqueda.")
    parser.add_argument("--json", type=str, default=None, help="Exporta los resultados en formato JSON en el fichero especificado.")
    parser.add_argument("--html", type=str, default=None, help="Exporta los resultados en formato HTML en el fichero especificado.")
    parser.add_argument("--download", type=str, default=None, help="Especifica las extensiones de archivo a descargar.")
    parser.add_argument("-gd", "--generate-dork", type=str, default=None, help="Genera un dork automáticamente a partir de una descripción utilizando IA.")
    args = parser.parse_args()

    main(query=args.query,
         configure_env=args.configure,
         start_page=args.start_page,
         pages=args.pages,
         lang=args.lang,
         output_json=args.json,
         output_html=args.html,
         download=args.download,
         gen_dork=args.generate_dork)