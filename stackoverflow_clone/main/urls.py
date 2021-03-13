from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('posts', views.QuestionViewSet)
router.register('post-answers', views.AnswerViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = router.urls
