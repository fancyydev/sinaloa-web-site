from django.shortcuts import render, get_object_or_404
from .gemini_service import query_gemini, validate_and_execute_query, preprocess_prompt
from .models import RestaurantBranch
from restaurant_menus.models import Menu, Category, Dishes
from itertools import groupby
from operator import attrgetter
from django.http import JsonResponse

# def ask_gemini(request):
#     prompt = request.GET.get("prompt", "Hola, ¿cómo estás?")
#     response = query_gemini(prompt)
#     return JsonResponse({"response": response})

# def handle_user_query(request):
#     """
#         Maneja las consultas del usuario con el chatbot
#     """
#     prompt = request.GET.get("prompt", "")  # Obtener el prompt del usuario desde los parámetros GET
#     if not prompt:
#         return {"error": "No se proporcionó una consulta válida."}

#     # Generar código Django ORM
#     query_code = query_gemini(prompt)

#     # Validar y ejecutar el código generado
#     if query_code.startswith("Error") or query_code.startswith("No se pudo"):
#         return {"error": query_code}

#     # Ejecutar la consulta
#     result = validate_and_execute_query(query_code)
#     return JsonResponse({"query_code": query_code, "result": result})


def home(request):
    #Mandamos todos los restaurantes
    restaurants = RestaurantBranch.objects.all()
    return render(request, 'restaurant_branches/principal.html', {'restaurants': restaurants})

# Nos permite devolver las categorias agrupadas por tipo
# def menus(request, slug):
    
#     restaurant = get_object_or_404(RestaurantBranch, slug=slug)
#     menu = Menu.objects.get(restaurant_branch=restaurant)
#     categories = Category.objects.filter(menu=menu)
    
#     # Organizar categorías por tipo
#     grouped_categories = {
#         type_key: list(group)
#         for type_key, group in groupby(categories, key=lambda x: x.type)
#     }
    
#     return render(request, 'restaurant_branches/menus.html', {'grouped_categories': grouped_categories})

def menus(request, slug):
    restaurant = get_object_or_404(RestaurantBranch, slug=slug)
    menu = Menu.objects.get(restaurant_branch=restaurant)
    #categories = Category.objects.filter(menu=menu)
    #Ordenamos primero las categorias en base a su type
    categories = sorted(
        Category.objects.filter(menu=menu),
        key=lambda cat: [t[0] for t in Category.CATEGORIES_TYPES].index(cat.type)
    )

    print(categories)
    # Agrupar platillos por categoría
    dishes_by_category = {
        category: Dishes.objects.filter(category=category)
        for category in categories
    }

    # Ordenar las categorías por 'type' antes de agrupar
    #ategories_sorted = sorted(categories, key=attrgetter('type'))

    # Agrupar categorías por tipo
    grouped_categories = {
        type_key: list(group)
        #for type_key, group in groupby(categories_sorted, key=attrgetter('type'))
        for type_key, group in groupby(categories, key=attrgetter('type'))
    }

    
    print(grouped_categories)

    return render(
        request,
        'restaurant_branches/menus.html',
        {
            'grouped_categories': grouped_categories,
            'dishes_by_category': dishes_by_category,
        }
    )

    

def handle_user_query(request):
    """
    Maneja las consultas del usuario con el chatbot
    """
    prompt = request.GET.get("prompt", "")  # Obtener el prompt del usuario desde los parámetros GET
    if not prompt:
        return JsonResponse({"error": "No se proporcionó una consulta válida."})

    # Procesar el prompt para extraer palabras clave
    keywords = preprocess_prompt(prompt)

    # Generar código Django ORM
    query_code = query_gemini(prompt)

    # Validar el codigo generado
    if query_code.startswith("Error") or query_code.startswith("No se pudo"):
        return JsonResponse({"error": query_code})

    # Ejecutar la consulta en la cual en caso de no obtener nada dara recomendaciones a partir de las keywords
    result = validate_and_execute_query(query_code, keywords)
    
    return JsonResponse({"query_code": query_code, "result": result})