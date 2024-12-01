import re
from django.db.models import Q
import google.generativeai as genai
from django.conf import settings
from .models import RestaurantBranch
from restaurant_menus.models import Menu, Category, Dishes
from django.forms.models import model_to_dict


# Configurar clave API
genai.configure(api_key=settings.OPENAI_API_KEY)

def preprocess_prompt(prompt):
    """
    Procesa el prompt para extraer palabras clave.
    """
    STOPWORDS = {'cual', 'es', 'el', 'de', 'en', 'un', 'una', 'la', 'los', 'las', 'que', 'cómo', 'con', 'para'}
    prompt = re.sub(r'[^\w\s]', '', prompt.lower())
    keywords = [word for word in prompt.split() if word not in STOPWORDS]
    return keywords


def query_gemini(prompt, model="gemini-1.5-flash"):
    """
    Procesa un prompt utilizando Gemini para generar consultas dinámicas en Django ORM.
    """
    
    # Son las instrucciones dadas a gemini para que construya el codigo que nos permitira extraer datos de la base de datos
    # FALTA ACTUALIZAR EL MODELO DE CATEGORIA
    
    system_instruction = """
    Eres un asistente para gestionar una base de datos de un restaurante usando Django ORM. 
    La base de datos contiene los modelos:
    La base de datos contiene los siguientes modelos:

    - `RestaurantBranch`: Representa las sucursales de un restaurante. Los campos de este modelo incluyen:
        - `name` (CharField): El nombre de la sucursal.
        - `logo` (ImageField): Una imagen del logotipo de la sucursal, almacenada en la ruta `restaurant/images/`.
        - `slug` (CharField): Un identificador único para la sucursal.
        - `description` (TextField): Una descripción de la sucursal.
        - `phone_number` (CharField): El número de teléfono de la sucursal, con un máximo de 15 caracteres.
        - `email` (CharField): El correo electrónico de la sucursal, con un máximo de 255 caracteres.
        - `address` (CharField): La dirección física de la sucursal, con un máximo de 255 caracteres.
        - `google_link` (TextField): Un enlace a la ubicación de la sucursal en Google Maps.

        El método `__str__` devuelve el nombre de la sucursal.

    - `Menu`: Representa los menús disponibles en las sucursales. Los campos de este modelo incluyen:
        - `name` (CharField): El nombre del menú.
        - `restaurant_branch` (ForeignKey): Relación con una sucursal (`RestaurantBranch`), con eliminación en cascada si se elimina la sucursal.

        El método `__str__` devuelve una cadena con el formato `<nombre del menú>-<nombre de la sucursal>`.

    - `Category`: Organiza los platillos dentro de un menú en categorías específicas. Los campos de este modelo incluyen:
        - `name` (CharField): El nombre de la categoría.
        - `menu` (ForeignKey): Relación con un menú (`Menu`), con eliminación en cascada si se elimina el menú.
        - `slug` (CharField): Un identificador único para la categoría.

        El método `__str__` devuelve una cadena con el formato `<nombre de la categoría>-<nombre del menú>`.

    - `Dishes`: Representa los platillos disponibles dentro de una categoría. Los campos de este modelo incluyen:
        - `name` (CharField): El nombre del platillo.
        - `category` (ForeignKey): Relación con una categoría (`Category`), con eliminación en cascada si se elimina la categoría.
        - `description` (TextField): Una descripción del platillo.
        - `img` (ImageField): Una imagen del platillo, almacenada en la ruta `dishes/images/`.
        - `price` (DecimalField): El precio del platillo, con un máximo de 5 dígitos y 2 decimales.

        El método `__str__` devuelve una cadena con el formato `<nombre del platillo>-<nombre de la categoría>-<precio del platillo>`.

    Puedes importar los modelos de la siguiente manera:
    - `from .models import RestaurantBranch`
    - `from restaurant_menus.models import Menu, Category, Dishes`  

    Tu tarea es interpretar preguntas y generar el código Django ORM necesario para obtener la información solicitada asignando lo que obtenga a una variable llamada result mandando el resultado como un diccionario donde se ignoren los campos que hagan referencias a imágenes.
    Si una consulta no genera resultados, intenta buscar coincidencias más amplias y proporciona sugerencias a su vez puedes usar el nombre de la categoria en caso de que pregunten por platillos en general.
    Como recomendacion al realizar busquedas utiliza icontains.
     
    Ejemplos:
    - Pregunta: '¿Cuál es el platillo más caro?'
      Respuesta: 
      ```python
      from django.forms.models import model_to_dict
      most_expensive_dish = Dishes.objects.order_by('-price').first()
      if most_expensive_dish:
          dish_dict = model_to_dict(most_expensive_dish)
          dish_dict.pop('img', None)
          result = dish_dict
      else:
          result = {'error': 'No se encontró ningún platillo.'}
      ```
    - Pregunta: '¿Qué categorías tiene el menú de una sucursal específica?'
      Respuesta:
      ```python
      category = Category.objects.filter(menu__restaurant_branch__name__icontains='nombre_sucursal')
      if category:
          result = list(category)
      else:
          result = {'error': 'No se encontró ningúna categoria.'}
      ```
    - Pregunta: 'Que aguachiles hay'
      Respuesta:
      ```python
      dishes = Dishes.objects.filter(category__name__icontains='aguachiles')
      if dishes:
          dish_dict = list(dishes)
          dish_dict.pop('img', None)
          result = dish_dict
      else:
          result = {'error': 'No se encontró ningúna categoria.'}
      ```
    """
    
    #Dishes.objects.filter(category__name__icontains='aguachiles')

    # Crear modelo generativo y chat
    model = genai.GenerativeModel(model_name=model, system_instruction=system_instruction)
    chat = model.start_chat()

    # Generar respuesta
    response = chat.send_message(prompt)

    # Validar y extraer código generado por gemini
    if hasattr(response, "text") and "```python" in response.text:
        try:
            code_block = response.text.split("```python")[1].split("```")[0].strip()
            return code_block
        except IndexError:
            return "No se pudo procesar correctamente la respuesta del modelo."
    return "No se pudo interpretar la solicitud. Por favor, intenta de nuevo."


def validate_and_execute_query(query_code, keywords=None):
    """
    Valida y ejecuta el código Django ORM generado dinámicamente.
    """
    try:
        UNSAFE_KEYWORDS = ["delete", "drop", "truncate", "raw", "save"]
        if any(keyword in query_code.lower() for keyword in UNSAFE_KEYWORDS):
            return {"error": "Consulta rechazada por razones de seguridad."}

        # Crear un entorno seguro para ejecutar el código
        local_env = {}
        exec(query_code, globals(), local_env)

        # Obtener el resultado esperado si se define una variable 'result'
        result = local_env.get('result', None)
        print(result)
        

        # Si no hay resultados, busca coincidencias parciales usando palabras clave
        if isinstance(result, dict) and "error" in result and keywords:
            query = Q()
            for keyword in keywords:
                query |= Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(category__name__icontains=keyword) 
            suggestions = Dishes.objects.filter(query).values("name", "description", "price")
            if suggestions.exists():
                return {"error": "No se encontró ningún platillo exacto. Quizás te interesen estos:", "suggestions": list(suggestions)}
        
        return result
        #return {"error": "Consulta ejecutada correctamente, pero no devolvió resultados."}
    except Exception as e:
        return {"error": f"Error al ejecutar la consulta: {str(e)}"}


