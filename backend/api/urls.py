from django.urls import include, path
from rest_framework import routers


from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       UserSubscribeView, UserSubscriptionViewSet)

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('users/subscriptions/',
         UserSubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
