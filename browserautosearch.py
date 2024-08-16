from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BrowserAutoSearch:
    """Clase que automatiza la búsqueda en navegadores utilizando Selenium.

    Atributos:
        browser (webdriver): Instancia del navegador automatizado.
    """

    def __init__(self):
        """Inicializa la instancia de BrowserAutoSearch configurando el navegador."""
        self.browser = self._initialize_browser()

    def _initialize_browser(self):
        """Inicializa el navegador basado en los navegadores instalados (Firefox o Chrome).

        Returns:
            webdriver: Instancia de WebDriver para el navegador correspondiente.

        Raises:
            Exception: Si no se puede inicializar ningún navegador.
        """
        browsers = {
            "firefox": {
                "manager": GeckoDriverManager,
                "service": FirefoxService,
                "options": webdriver.FirefoxOptions(),
                "driver": webdriver.Firefox
            },
            "chrome": {
                "manager": ChromeDriverManager,
                "service": ChromeService,
                "options": webdriver.ChromeOptions(),
                "driver": webdriver.Chrome
            }
        }
        
        for browser_name, browser_info in browsers.items():
            try:
                return browser_info["driver"](service=browser_info["service"](browser_info["manager"]().install()), 
                                              options=browser_info["options"])
            except Exception as e:
                print(f"Error al iniciar el {browser_name}: {e}")

        raise Exception("No se pudo iniciar ningun navegador. Asegúrate de tener Firefox o Chrome instalados.")

    def accept_cookies(self, button_selector):
        """Acepta el anuncio de cookies en una página web.

        Args:
            button_selector (str): Selector del botón para aceptar cookies.
        """
        try:
            accept_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, button_selector))
            )
            accept_button.click()
        except Exception as e:
            print(f"Error al encontrar o hacer clic en el botón de aceptar cookies: {e}")

    def search_google(self, query):
        """Realiza una búsqueda en Google.

        Args:
            query (str): Texto de la consulta para realizar la búsqueda.
        """
        self.browser.get('http://www.google.com')
        self.accept_cookies(button_selector='L2AGLb')
        search_box = self.browser.find_element(By.NAME, 'q')
        search_box.send_keys(query + Keys.ENTER)
        time.sleep(5)

    def google_search_results(self):
        """Extrae los resultados de una búsqueda en Google.

        Returns:
            list: Lista de diccionarios con los resultados de la búsqueda, incluyendo título, enlace y descripción.
        """
        results = self.browser.find_elements(By.CSS_SELECTOR, 'div.g')
        custom_results = []
        for result in results:
            try:
                cresult = {
                    "title": result.find_element(By.CSS_SELECTOR, 'h3').text,
                    "link": result.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                    "description": result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
                }
                custom_results.append(cresult)
            except Exception as e:
                print(f"Un elemento no pudo ser extraído: {e}")
                continue
        return custom_results

    def quit(self):
        """Cierra el navegador y finaliza la instancia del WebDriver."""
        self.browser.quit()