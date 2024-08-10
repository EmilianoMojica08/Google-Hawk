import os
import sys
import argparse
from googlesearch import GoogleSearch
from results_parsey import ResultsProcessor
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


def main(query, configure_env, start_page, pages, lang, output_json, output_html):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta para realizar búsquedas avanzadas en Google de forma automática.")
    parser.add_argument("-q", "--query", type=str, help="Especifica el dork que deseas buscar. Ejemplo: -q \"filetype:sql 'MySQL dump' (pass|password|passwd|pwd)\"")
    parser.add_argument("-c", "--configure", action="store_true", help="Configura o actualiza el archivo .env. Utiliza esta opción sin otros argumentos para configurar las claves.")
    parser.add_argument("--start-page", type=int, default=1, help="Página de inicio para los resultados de búsqueda. Por defecto es 1.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas de resultados a retornar. Por defecto es 1.")
    parser.add_argument("--lang", type=str, default="lang_es", help="Código de idioma para los resultados de búsqueda. Por defecto es 'lang_es' (español).")
    parser.add_argument("--json", type=str, help="Exporta los resultados en formato JSON en el fichero especificado.")
    parser.add_argument("--html", type=str, help="Exporta los resultados en formato HTML en el fichero especificado.")

    args = parser.parse_args()

    main(query=args.query, 
         configure_env=args.configure, 
         start_page=args.start_page, 
         pages=args.pages, 
         lang=args.lang,
         output_html=args.html,
         output_json=args.json)