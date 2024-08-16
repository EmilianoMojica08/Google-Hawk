import os
import argparse
import re
from dotenv import load_dotenv
from openai import OpenAI
from transformers import GPT2Tokenizer


class SmartSearch:
    """Clase para buscar información en ficheros utilizando expresiones regulares o modelos de IA.

    Attributes:
        dir_path (str): Ruta del directorio donde se encuentran los archivos a buscar.
        files (dict): Diccionario que almacena el contenido de los archivos leídos.
    """

    def __init__(self, dir_path):
        """Inicializa la clase con la ruta del directorio y lee los ficheros.

        Args:
            dir_path (str): Ruta del directorio con los ficheros.
        """
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        """Lee todos los ficheros en el directorio especificado y los almacena en un diccionario.

        Returns:
            dict: Diccionario con nombres de archivo como claves y contenidos como valores.
        """
        files = {}
        for archivo in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, archivo)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files[archivo] = f.read()
            except Exception as e:
                print(f"Error al leer el fichero {file_path}: {e}")
        return files

    def regex_search(self, regex):
        """Realiza una búsqueda en los archivos usando una expresión regular proporcionada.

        Args:
            regex (str): Expresión regular utilizada para la búsqueda.

        Returns:
            dict: Diccionario con nombres de archivo como claves y listas de coincidencias como valores.
        """
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            while respuesta not in ("y", "n", "yes", "no"):
                respuesta = input(f"El fichero {file} tiene una longitud de {len(text)} caracteres, seguro que deseas continuar? (y/n): ")
            if respuesta in ("n", "no"):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if matches:
                coincidencias[file] = matches
        return coincidencias

    def ia_search(self, prompt, model_name='gpt-3.5-turbo-0125', max_tokens=100):
        """Realiza una búsqueda en los archivos utilizando un modelo de IA.

        Args:
            prompt (str): Texto inicial que guía al modelo de IA.
            model_name (str): Nombre del modelo de IA a utilizar.
            max_tokens (int): Máximo número de tokens que el modelo puede generar.

        Returns:
            dict: Diccionario con nombres de archivo como claves y resultados de IA como valores.
        """
        coincidencias = {}
        for file, text in self.files.items():
            respuesta = ""
            tokens, coste = self._calcular_coste(text, prompt, model_name, max_tokens)
            while respuesta not in ("y", "n", "yes", "no"):
                respuesta = input(f"El fichero {file} tiene una longitud de {tokens} tokens (aprox. {coste}$), seguro que deseas continuar? (y/n): ")
            if respuesta in ("n", "no"):
                continue

            # Dividir el fichero en segmentos
            file_segments = self._split_file(text, model_name)

            client = OpenAI()
            resultados_segmentos = []

            for index, segment in enumerate(file_segments):
                print(f"Procesando el segmento {index + 1}/{len(file_segments)}...")
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": f"{prompt}\n\nTexto:\n{segment}"}
                    ],
                    model=model_name,
                    max_tokens=max_tokens,
                    n=1,
                )
                resultados_segmentos.append(chat_completion.choices[0].message.content)
            coincidencias[file] = resultados_segmentos

        return coincidencias

    def _calcular_coste(self, text, prompt, model_name, max_tokens):
        """Calcula el coste estimado de realizar una búsqueda con IA basado en el número de tokens.

        Args:
            text (str): Texto del fichero.
            prompt (str): Prompt utilizado para guiar al modelo de IA.
            model_name (str): Modelo de IA utilizado.
            max_tokens (int): Máximo número de tokens que el modelo puede generar.

        Returns:
            tuple: Total de tokens y costo estimado.
        """
        precios = {
            "gpt-4-0125-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo-0125": {"input_cost": 0.0005, "output_cost": 0.0015},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002}            
        }
        # Tokenizar el texto para obtener el numero de tokens
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        len_tokens_prompt = len(tokenizer.tokenize(prompt))
        len_tokens_text = len(tokenizer.tokenize(text))

        # Calcular el coste de la generacion
        input_cost = ((len_tokens_prompt + len_tokens_text) / 1000) * precios[model_name]["input_cost"]
        output_cost = (max_tokens / 1000) * precios[model_name]["output_cost"]
        return (len_tokens_prompt + len_tokens_text, input_cost + output_cost)

    def _split_file(self, file_text, model_name):
        """Divide el texto de un fichero en segmentos según el modelo de IA utilizado.

        Args:
            file_text (str): Texto del fichero.
            model_name (str): Modelo de IA para determinar el tamaño del contexto.

        Returns:
            list: Lista de segmentos de texto.
        """
        context_window_sizes = {
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 16000,
            "gpt-4-32k": 32000,
            "gpt-3.5-turbo-0125": 16000,
            "gpt-3.5-turbo-instruct": 4000
        }
        return [file_text[i:i + context_window_sizes[model_name]] 
                for i in range(0, len(file_text), context_window_sizes[model_name])]


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Herramienta para realizar búsquedas en ficheros utilizando expresiones regulares o modelos de IA.")
    parser.add_argument("file", type=str, help="Ruta del fichero en el que realizar la búsqueda.")
    parser.add_argument("-p", "--prompt", type=str, help="Prompt para la búsqueda con IA.")
    parser.add_argument("-r", "--regex", type=str, help="Expresión regular para la búsqueda.")
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo-0125", help="Modelo de IA a utilizar.")
    parser.add_argument("--max-tokens", type=int, default=100, help="Número máximo de tokens que el modelo puede generar.")
    args = parser.parse_args()

    searcher = SmartSearch(args.file)
    if args.regex:
        resultados = searcher.regex_search(args.regex)
        print("\nResultados de la búsqueda por expresión regular:")
        for file, results in resultados.items():
            print(f"{file}:")
            for r in results:
                print(f"\t- {r}")
    elif args.prompt:
        resultados = searcher.ia_search(args.prompt, args.model, args.max_tokens)
        print("\nResultados de la búsqueda con IA:")
        for file, results in resultados.items():
            print(f"{file}:")
            for r in results:
                print(f"\t- {r}")