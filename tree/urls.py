from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


tree_router = DefaultRouter()
tree_router.register(r'', TreeView, basename='tree')


urlpatterns = [
    path('null/', NoneView.as_view(), name='tree'),

    path('tree/', include(tree_router.urls)),
    path('child/<int:id>/', ChildrenView.as_view({"get": 'list'}), name='children'),

    path('drevo/<int:id>/', DrevoView.as_view({"get": "list"}), name='drevo'),
]