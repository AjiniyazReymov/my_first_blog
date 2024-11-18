from django.urls import path

from posts.views import PostCreateView, PostListView, PostDetailView, PostEditView, \
    ConfirmDeleteView, PostDeleteView, EditReviewView, AddReviewView, \
    ConfirmDeleteReviewView, DeleteReviewView, PopularPostView, MonthWeeksPopularPostView

app_name = 'posts'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create', PostCreateView.as_view(), name='create'),
    path('popular', PopularPostView.as_view(), name='popular'),
    path('popular/<str:period>/', MonthWeeksPopularPostView.as_view(), name='popular_posts'),
    path('<int:id>', PostDetailView.as_view(), name='detail'),
    path('<int:id>/edit', PostEditView.as_view(), name='post-edit'),
    path('<int:id>/confirm', ConfirmDeleteView.as_view(), name='confirm-delete'),
    path('<int:id>/delete', PostDeleteView.as_view(), name='delete'),
    path('<int:id>/review', AddReviewView.as_view(), name='reviews'),
    path('<int:post_id>/review/<int:review_id>/edit', EditReviewView.as_view(), name='review-edit'),
    path('<int:post_id>/reviews/<int:review_id>/delete/confirm/', ConfirmDeleteReviewView.as_view(), name='confirm-delete-review'),
    path('<int:post_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review')
]