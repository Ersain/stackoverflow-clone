from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('questions', views.QuestionViewSet, basename='questions')
router.register('answers', views.AnswerViewSet, basename='answers')
router.register('tags', views.TagViewSet)

urlpatterns = router.urls
