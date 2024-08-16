from gpt4all import GPT4All
from openai import OpenAI

class IAGeneratorInterface:
    """Define la interfaz común para los generadores de IA.
    
    Esta interfaz establece el método que todas las clases generadoras de IA deben implementar.
    """
    
    def generate(self, prompt):
        """Genera una salida basada en un mensaje de entrada.
        
        Args:
            prompt (str): Mensaje de entrada para el generador.
        
        Returns:
            str: La salida generada por el modelo de IA.
        
        Raises:
            NotImplementedError: Si el método no ha sido implementado por la subclase.
        """
        raise NotImplementedError("Este método debe ser implementado por la subclase.")
    

class GPT4AllGenerator(IAGeneratorInterface):
    """Implementación de la interfaz para el generador GPT4All."""
    
    def __init__(self, model_name="orca-mini-3b-gguf2-q4_0.gguf"):
        """Inicializa el generador GPT4All con un modelo específico.
        
        Args:
            model_name (str): Nombre del modelo de GPT4All a utilizar.
        """
        self.model = GPT4All(model_name)

    def generate(self, prompt):
        """Genera una salida utilizando el modelo de GPT4All especificado.
        
        Args:
            prompt (str): Mensaje de entrada para el generador.
        
        Returns:
            str: La salida generada por el modelo.
        """
        return self.model.generate(prompt)

    
class OpenAIGenerator(IAGeneratorInterface):
    """Implementación de la interfaz para el generador de la API de OpenAI."""
    
    def __init__(self, model_name='gpt-4'):
        """Inicializa el generador de OpenAI con un modelo específico.
        
        Args:
            model_name (str): Nombre del modelo de OpenAI a utilizar.
        """
        self.model_name = model_name
        self.client = OpenAI()
    
    def generate(self, prompt):
        """Genera una salida utilizando el modelo de OpenAI especificado.
        
        Args:
            prompt (str): Mensaje de entrada para el generador.
        
        Returns:
            str: La salida generada por el modelo.
        """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=self.model_name,
        )
        return chat_completion.choices[0].message.content

    
class IAagent:
    """Agente que utiliza un generador de IA para producir salidas específicas."""
    
    def __init__(self, generator):
        """Inicializa el agente con un generador de IA específico.
        
        Args:
            generator (IAGeneratorInterface): Una instancia de un generador de IA.
        """
        self.generator = generator

    def generate_gdork(self, description):
        """Genera un Google Dork basado en una descripción proporcionada.
        
        Args:
            description (str): Descripción para la cual generar el Google Dork.
        
        Returns:
            str: El Google Dork generado o None si ocurre una excepción.
        """
        prompt = self._build_prompt(description)
        try:
            output = self.generator.generate(prompt)
            return output
        except Exception as e:
            print(f"Error al generar el Google Dork: {e}")
            return None
    
    def _build_prompt(self, description):
        """Construye el mensaje de entrada para el generador basado en la descripción proporcionada.
        
        Args:
            description (str): Descripción de entrada para construir el mensaje.
        
        Returns:
            str: Mensaje completo para el generador.
        """
        return f"""
        Genera un Google Dork específico basado en la descripción del usuario. Un Google Dork utiliza operadores avanzados en motores de búsqueda para encontrar información específica que es difícil de encontrar mediante una búsqueda normal. Tu tarea es convertir la descripción del usuario en un Google Dork preciso. A continuación, se presentan algunos ejemplos de cómo deberías formular los Google Dorks basándote en diferentes descripciones:

        Descripción: Documentos PDF relacionados con la seguridad informática publicados en el último año.
        Google Dork: filetype:pdf "seguridad informática" after:2023-01-01

        Descripción: Presentaciones de Powerpoint sobre cambio climático disponibles en sitios .edu.
        Google Dork: site:.edu filetype:ppt "cambio climático"

        Descripción: Listas de correos electrónicos en archivos de texto dentro de dominios gubernamentales.
        Google Dork: site:.gov filetype:txt "email" | "correo electrónico"

        Ahora, basado en la siguiente descripción proporcionada por el usuario, genera el Google Dork correspondiente:

        Descripción: {description}
        """

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    openai_generator = OpenAIGenerator('gpt-4')
    ia_agent = IAagent(openai_generator)
    print(ia_agent.generate_gdork("Lista de usuarios y contraseñas en archivos sql y volcados de bases de datos. Busca por diferentes variaciones de la palabra password."))