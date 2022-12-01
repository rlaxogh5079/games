from django.urls import include, path

urlpatterns = [
    path('', include('config_app.urls'))
]