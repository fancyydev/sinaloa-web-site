import google.generativeai as genai
from django.conf import settings
from .models import RestaurantBranch
from restaurant_menus.models import Menu, Category, Dishes
from django.forms.models import model_to_dict


# Configurar clave API
genai.configure(api_key=settings.OPENAI_API_KEY)

def query_gemini(prompt, model="gemini-1.5-flash"):
    """
    Procesa un prompt utilizando Gemini para generar consultas dinámicas en Django ORM.
    """
    system_instruction = """
    Eres un asistente para gestionar una base de datos de un restaurante usando Django ORM. 
    La base de datos contiene los modelos:
    - `RestaurantBranch` representa las sucursales de un restaurante, con información como nombre, logotipo, descripción, 
       número de teléfono, correo electrónico, dirección y enlace a Google Maps.
    - `Menu` contiene los menús disponibles en las sucursales y está relacionado con `RestaurantBranch`. Tiene un campo 
       `name` que identifica el menú.
    - `Category` organiza las categorías de un menú, como entradas o postres, y está relacionado con `Menu`. Incluye un 
       campo `slug` que identifica de manera única cada categoría.
    - `Dishes` almacena información sobre los platillos dentro de una categoría. Incluye los campos `name`, `category`, 
       `description`, `img` (ruta a la imagen del platillo) y `price` (precio del platillo).


    Tu tarea es interpretar preguntas y generar el código Django ORM necesario para obtener la información solicitada asignando lo que obtenga a una variable llamada result mandando el resultado como un diccionario.
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
          category_list = list(category)
          return category_list
      else:
          result = {'error': 'No se encontró ningúna categoria.'}
      ```
    

    Devuelve solo el código Django ORM dentro de un bloque de código, sin texto adicional.
    """

    # Crear modelo generativo y chat
    model = genai.GenerativeModel(model_name=model, system_instruction=system_instruction)
    chat = model.start_chat()

    # Generar respuesta
    response = chat.send_message(prompt)

    # Validar y extraer código
    if hasattr(response, "text") and "```python" in response.text:
        try:
            # Extraer el código dentro del bloque ```python
            code_block = response.text.split("```python")[1].split("```")[0].strip()
            return code_block
        except IndexError:
            return "No se pudo procesar correctamente la respuesta del modelo."
    return "No se pudo interpretar la solicitud. Por favor, intenta de nuevo."


def validate_and_execute_query(query_code):
    """
    Valida y ejecuta el código Django ORM generado dinámicamente.
    """
    try:
        # Verificar si contiene palabras clave inseguras
        UNSAFE_KEYWORDS = ["delete", "drop", "truncate", "raw"]
        if any(keyword in query_code.lower() for keyword in UNSAFE_KEYWORDS):
            return "Consulta rechazada por razones de seguridad."

        # Crear un entorno seguro para ejecutar el código
        local_env = {}
        exec(query_code, globals(), local_env)

        # Obtener el resultado esperado si se define una variable 'result'
        result = local_env.get('result', None)
        return result or "Consulta ejecutada correctamente, pero no devolvió resultados."
    except Exception as e:
        return f"Error al ejecutar la consulta: {str(e)}"