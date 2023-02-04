from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

v1_router = DefaultRouter()
v1_router.register('v1/posts', PostViewSet, basename='post')
v1_router.register('v1/groups', GroupViewSet, basename='group')
v1_router.register(
    r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)
v1_router.register('v1/follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
