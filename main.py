from googlesearch import GoogleSearch
from dotenv import load_dotenv
import os
# Constantes para configurar la API de búsqueda personalizada de Google
load_dotenv()

API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
SERCH_ENGINE_ID = os.getenv("SERCH_ENGINE_ID")

# Configuración de la consulta y parámetros de búsqueda
query = 'Python curso'

gseaarch = GoogleSearch(API_KEY_GOOGLE, SERCH_ENGINE_ID)

results = gseaarch.search(query,pages=2)
print(results)