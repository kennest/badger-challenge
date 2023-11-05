from django.urls import path, include

from . import views
from .routers import router
from .views import ModelDetailView, Model3DCreateView

urlpatterns = [
    path('api/', include(router.urls)),
    path('home/', views.home, name='home'),
    path('detail/<int:pk>', ModelDetailView.as_view(), name='detail'),
    path('create/', Model3DCreateView.as_view(), name='create'),
]
