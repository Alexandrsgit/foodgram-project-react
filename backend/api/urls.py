from rest_framework import routers
from django.urls import path, include

from api.views import TagViewSet, RecipeViewSet, FollowViewSet, FavoriteViewSet, ShoppingCartViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('follow', FollowViewSet)
router.register('favorite', FavoriteViewSet)
router.register('shoppingcart', ShoppingCartViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
