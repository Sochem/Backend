from django.urls import path, include
from rest_framework import routers
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .views import commentCount, get_family
from .authorization import auth
router = routers.DefaultRouter()

router.register('forum-post', ForumPostViewSet)
router.register('forum-comment', ForumCommentViewSet)
router.register('forum-reply', ForumReplyViewSet)
router.register('users', UserViewSet)
router.register('user-from-token', UserFromTokenViewSet)
router.register('events', EventsViewSet)
router.register('user-extension', UserExtensionViewSet)
router.register('family-list', FamilyViewSet)
router.register('notifi', NotificationViewSet)

urlpatterns = [
   path('total-comments', commentCount),
   path('family', get_family),
   path('conf', conf),
   path('onboarding', onboarding),
   path('home_carousel', home_carousel),
   path('logup', auth),
   path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
