from django import template
from src.app.models import FavPosts
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import intcomma
#is_liked_by_user
register = template.Library()

@register.simple_tag
def check_for_like(user_id, post_id):
    return FavPosts.objects.filter(Q(creator_id = user_id)&Q(post_id = post_id)).exists()

@register.filter(name='to_int')
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # или None, или любое другое значение по умолчанию
def currency(dollars):
    dollars = round(float(dollars), 2)
    return "%s" % (intcomma(int(dollars)))
register.filter('currency', currency)