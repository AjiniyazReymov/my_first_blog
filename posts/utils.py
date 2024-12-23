from django.utils.timezone import now, timedelta
from .models import Post


def get_popular_posts(period='month'):
    if period == 'week':
        start_date = now() - timedelta(days=7)
    elif period == 'month':
        start_date = now() - timedelta(days=30)
    else:
        raise ValueError("Unsupported period. Use 'week' or 'month'.")


    return Post.objects.all().filter(created_at__gte=start_date, status='approved').order_by('-views')[:10]
