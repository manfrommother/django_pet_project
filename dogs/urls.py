from rest_framework import routers
from .views import DogViewSet, BreedViewSet

router = routers.DefaultRouter()
router.register(r'dogs', DogViewSet, basename='dog')
router.register(r'breeds', BreedViewSet, basename='breed')

urlpatterns = router.urls