from datetime import date
from django.conf import settings

def default_variables(request):
    return {
        'is_authenticated': request.user.is_authenticated,
        'title': settings.BLOG_TITLE,
        'date': str(date.today())
    }