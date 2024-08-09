from googlesearch import GoogleSearch
from dotenv import load_dotenv, set_key
import os
import argparse
import sys


def env_config():
    """Configura el archivo .env con las claves de la API de Google."""
    api_key = input("Introduce tu clave de API de Google: ")
    engine_id = input("Introduce tu ID de motor de búsqueda personalizado de Google: ")
    set_key(".env", "API_KEY_GOOGLE", api_key)
    set_key(".env", "SERCH_ENGINE_ID", engine_id)
    

def main(query, configure_env, start_page, pages, lang):
    # comprobar si se necesita configurar el archivo .env
    env_exists = os.path.exists(".env")

    if not env_exists or configure_env:
        # TODO: Implementar la configuración del archivo .env
        env_config()
        print("Archivo .env configurado correctamente.")
        sys.exit(1)
       

    
    # Constantes para configurar la API de búsqueda personalizada de Google
    load_dotenv()

    #tienen que estar en el archivo .env sus credenciales de google para poder hacer la busqueda
    API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
    SERCH_ENGINE_ID = os.getenv("SERCH_ENGINE_ID")

    # Configuración de la consulta y parámetros de búsqueda
    if not query:
        print("Debes especificar una consulta con el argumento -q. utiliza -h para obtener ayuda.")
        sys.exit(1)
    

    gseaarch = GoogleSearch(API_KEY_GOOGLE, SERCH_ENGINE_ID)

    results = gseaarch.search(query,pages=pages, start_page=start_page, lang=lang)
    print(results)

if __name__ == "__main__":
    #configuracion de argumentos de la linea de comandos
    parser = argparse.ArgumentParser(description="Herramienta para realizar búsquedas avanzadas en Google de forma automática.")
    parser.add_argument("-q", "--query", type=str, help="Especifica el dork que deseas buscar. Ejemplo: -q \"filetype:sql 'MySQL dump' (pass|password|passwd|pwd)\"")
    parser.add_argument("-c", "--configure", action="store_true", help="Configura o actualiza el archivo .env. Utiliza esta opción sin otros argumentos para configurar las claves.")
    parser.add_argument("--start-page", type=int, default=1, help="Página de inicio para los resultados de búsqueda. Por defecto es 1.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas de resultados a retornar. Por defecto es 1.")
    parser.add_argument("--lang", type=str, default="lang_es", help="Código de idioma para los resultados de búsqueda. Por defecto es 'lang_es' (español).")
    
    args = parser.parse_args()

    main(query=args.query, configure_env=args.configure, start_page=args.start_page, pages=args.pages, lang=args.lang)
