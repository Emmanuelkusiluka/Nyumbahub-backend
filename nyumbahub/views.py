from django.http import JsonResponse


def test(request):
    return JsonResponse({'message': 'Welcome Back Trickshot API is working'})