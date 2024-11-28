import google.generativeai as genai
from django.conf import settings
from .models import *


# Configurar la clave API
genai.configure(api_key=settings.OPENAI_API_KEY)

# def sum_of_two_numbers(first_number: int, second_number: int) -> int:
#     """ This function sums the two specified parameters.

#     Args:
#         first_number: It is an integer.
#         second_number: It is an integer.

#     Returns:
#         One number with the result of the sum 
#     """
    
#     print("Se ejecutó la función suma")
#     return first_number + second_number

# def sum_of_three_numbers(first_number: int, second_number: int, third_number: int) -> int:
#     """ This function sums the three specified parameters.

#     Args:
#         first_number: It is an integer.
#         second_number: It is an integer.
#         third_number: It is an integer.

#     Returns:
#         One number with the result of the sum of the three parameters
#     """
    
#     print("Se ejecutó la función suma")
#     return first_number + second_number + third_number

    

def query_gemini(prompt, model="gemini-1.5-flash"):
    personal_system_instruction = """El sistema debe interactuar con una base de datos de Django que contiene los modelos `RestaurantBranch`, `Menu`, 
    `Category` y `Dishes`. Estas tablas están relacionadas y organizadas de la siguiente forma:

    1. `RestaurantBranch` representa las sucursales de un restaurante, con información como nombre, logotipo, descripción, 
       número de teléfono, correo electrónico, dirección y enlace a Google Maps.

    2. `Menu` contiene los menús disponibles en las sucursales y está relacionado con `RestaurantBranch`. Tiene un campo 
       `name` que identifica el menú.

    3. `Category` organiza las categorías de un menú, como entradas o postres, y está relacionado con `Menu`. Incluye un 
       campo `slug` que identifica de manera única cada categoría.

    4. `Dishes` almacena información sobre los platillos dentro de una categoría. Incluye los campos `name`, `category`, 
       `description`, `img` (ruta a la imagen del platillo) y `price` (precio del platillo).

    Tu tarea es generar consultas para interactuar con esta base de datos según las preguntas o instrucciones del usuario. 
    Considera ejemplos como:
    - 'Muestra los platillos más caros.'
    - '¿Qué categorías tiene el menú de una sucursal específica?'
    - 'Obtén la información de contacto de una sucursal.'

    Para cada instrucción del usuario, devuelve el código de consulta Django ORM necesario para obtener la información 
    solicitada. Si no se puede resolver con los modelos proporcionados, indica al usuario qué datos faltan o qué ajustes 
    son necesarios en los modelos para realizar la consulta."""
    
    # Configurar el modelo con herramientas
    #model = genai.GenerativeModel(model_name=model, tools=[sum_of_two_numbers, sum_of_three_numbers])
    model = genai.GenerativeModel(
        model_name=model, 
        system_instruction=personal_system_instruction)

    #Podemos dejar que el chat ejecute funciones de manera automatica
    #chat = model.start_chat(enable_automatic_function_calling=True)
    
    #O hacerlo de manera manual
    chat = model.start_chat()

    # Enviar el mensaje
    response = chat.send_message(prompt)
    
    print(response)
    # Podemos obtener cierta memoria pero al estar en un servidor tendria que idear una forma de mantener la 
    # memoria
    # response = chat.send_message("I have 2 dogs in my house.")
    # print(response.text)
    # response = chat.send_message("How many paws are in my house?")
    # print(response.text)
    
    # Manejar la respuesta
    if hasattr(response, "text"):
        return response.text
    else:
        # Manejo de errores si 'text' no está presente
        print("La respuesta no contiene texto.")

