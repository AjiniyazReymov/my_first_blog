from django.shortcuts import render
from django.views import View

from posts.models import Post
from posts.utils import get_popular_posts

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(status='approved').order_by('-created_at')
        return render(request, 'landing.html', {'posts': posts})

class PopularPostView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-views')[:10]
        return render(request, 'landing.html', {'posts':posts})

class MonthWeeksPopularPostView(View):
    def get(self, request, period='month'):
        posts = get_popular_posts(period=period)
        return render(request, 'landing.html', {'posts':posts, 'period':period})