from django.shortcuts import render
from .gemini_service import query_gemini, validate_and_execute_query, preprocess_prompt
from django.http import JsonResponse

def ask_gemini(request):
    prompt = request.GET.get("prompt", "Hola, ¿cómo estás?")
    response = query_gemini(prompt)
    return JsonResponse({"response": response})

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

    # Validar y ejecutar el código generado
    if query_code.startswith("Error") or query_code.startswith("No se pudo"):
        return JsonResponse({"error": query_code})

    # Ejecutar la consultaW
    result = validate_and_execute_query(query_code, keywords)
    return JsonResponse({"query_code": query_code, "result": result})