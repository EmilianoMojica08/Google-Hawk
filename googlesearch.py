import requests

class GoogleSearch:
    """Class to perform searches using Google's Custom Search API.
    
    This class allows users to execute Google searches using the custom API,
    handling result pagination and allowing configuration of the results' language.

    Attributes:
        api_key (str): API key to access the Google API.
        engine_id (str): Identifier of the Google custom search engine.
    """

    def __init__(self, api_key, engine_id):
        """Initializes a new instance of GoogleSearch with the API key and search engine ID.

        Args:
            api_key (str): The API key to access the Google API.
            engine_id (str): The identifier of the Google custom search engine.
        """
        self.api_key = api_key
        self.engine_id = engine_id

    def search(self, query, start_page=1, pages=1, lang="lang_es"):
        """Performs a Google search using the API.

        The function manages pagination and retrieves search results,
        processing each page as specified.

        Args:
            query (str): Query text for the search.
            start_page (int): Initial page to start the search from.
            pages (int): Number of result pages to retrieve.
            lang (str): Language of the results, in language code format.

        Returns:
            list[dict]: List of custom search results, each as a dictionary.

        Raises:
            Exception: If the API response has a non-200 HTTP status.
        """
        final_results = []
        results_per_page = 10  # Google displays 10 results per page
        for page in range(pages):
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={start_index}&lr={lang}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                resu
