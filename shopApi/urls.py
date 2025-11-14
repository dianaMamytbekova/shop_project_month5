from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Shop API",
        "endpoints": {
            "register": "POST /api/v1/users/register/",
            "login": "POST /api/v1/users/login/", 
            "confirm": "POST /api/v1/users/confirm/"
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
]