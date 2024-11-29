from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import PostListView, PostCreateView, PostDetailView, PostEditView, ConfirmDeleteView, \
                        PostDeleteView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, \
                        DeleteReviewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='landing_page'),
    path('users/', include('users.urls')),
    path('posts', PostListView.as_view(), name='post-list'),
    path('posts/create', PostCreateView.as_view(), name='create'),
    path('posts/<int:id>', PostDetailView.as_view(), name='detail'),
    path('posts/<int:id>/edit', PostEditView.as_view(), name='post-edit'),
    path('posts/<int:id>/confirm', ConfirmDeleteView.as_view(), name='confirm-delete'),
    path('posts/<int:id>/delete', PostDeleteView.as_view(), name='delete'),
    path('posts/<int:id>/review', AddReviewView.as_view(), name='reviews'),
    path('posts/<int:post_id>/review/<int:review_id>/edit', EditReviewView.as_view(), name='review-edit'),
    path('posts/<int:post_id>/reviews/<int:review_id>/delete/confirm/', ConfirmDeleteReviewView.as_view(), name='confirm-delete-review'),
    path('posts/<int:post_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #media file lardi taba aliwi ushin