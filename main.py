from dotenv import load_dotenv
import os
from googlesearch import GoogleSearch

# Load environment variables from the .env file to ensure security and configurability.
load_dotenv()

# Get configuration keys from the environment variables.
API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Define the search query to find specific information on Google.
query = 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'

# Create an instance of GoogleSearch with the provided API key and search engine ID.
gsearch = GoogleSearch(API_KEY_GOOGLE, SEARCH_ENGINE_ID)

# Perform the search with the defined query, specifying the number of pages to retrieve.
results = gsearch.search(query, pages=2)

# Print the obtained search results.
print(results)
