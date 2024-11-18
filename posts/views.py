from django.urls import reverse

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from posts.forms import PostCreateForm, PostReviewForm
from posts.models import Post, PostReview
from posts.utils import get_popular_posts


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostCreateForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.status = 'pending'
                post.save()
                return redirect('posts:post-list')
        else:
            form = PostCreateForm(request.POST)
            return render(request, 'posts/post_form.html', {'form': form})

class PostDetailView(View):
    def get(self, request, id):
        try:
            post = get_object_or_404(Post, id=id)
            post.views += 1
            post.save()
        except Post.DoesNotExist:
            return redirect('posts:post-list')

        review_form = PostReviewForm()
        return render(request, 'posts/detail.html', {'post':post, 'review_form':review_form})

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(status='approved').order_by('-created_at')
        return render(request, 'posts/post_list.html', {'posts': posts})

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id, status='approved')
        post_form = PostCreateForm(instance=post)  # Здесь не нужно передавать data=request.POST
        return render(request, 'posts/post_edit.html', {'post': post, 'post_form': post_form})

    def post (sel, request, id):
        post = get_object_or_404(Post, id=id, status='approved')
        post_form = PostCreateForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:detail', id=post.id)

class ConfirmDeleteView(View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id, status='approved')
        return render(request, 'posts/confirm_delete.html', {'post':post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = get_object_or_404(Post, id=id, status='approved')
        post.delete()
        messages.success(request, "You have successfully deleted this post")

        return redirect('posts:post-list')

class PopularPostView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-views')[:10]
        return render(request, 'posts/popular_post.html', {'posts':posts})

class MonthWeeksPopularPostView(View):
    def get(self, request, period='month'):
        posts = get_popular_posts(period=period)
        return render(request, 'posts/month_popular_post.html', {'posts':posts, 'period':period})

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return redirect('posts:detail', id=id)

        review_form = PostReviewForm(data=request.POST)
        if review_form.is_valid():
            PostReview.objects.create(
                post_id=post,
                user_id=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse("posts:detail", kwargs={"id": post.id}))


        return render(request, 'posts/detail.html', {'post':post, 'review_form':review_form})

class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = get_object_or_404(Post, id=post_id)
        review = get_object_or_404(post.postreview_set, id=review_id)
        review_form = PostReviewForm(instance=review)
        return render(request, 'posts/review_edit.html', {'post': post, 'review': review, 'review_form': review_form})

    def post(self, request, post_id, review_id):
        post = get_object_or_404(Post, id=post_id)
        review = get_object_or_404(post.postreview_set, id=review_id)
        review_form = PostReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('posts:detail', kwargs={"id": post_id}))
        return render(request, 'posts/review_edit.html', {'post': post, 'review': review, 'review_form': review_form})

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)
        return render(request, 'posts/confirm_delete_review.html', {'post':post, 'review':review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        review = post.postreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse('posts:detail', kwargs={'id':post_id}))