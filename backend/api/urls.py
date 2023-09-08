from django.urls import include, path
from rest_framework import routers


from api.views import IngredientViewSet, TagViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
