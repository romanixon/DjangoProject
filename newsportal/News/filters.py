import django_filters
from django.forms import DateInput
from django_filters import DateFilter

from .models import *


class NewsFilter(django_filters.FilterSet):
    post_in = DateFilter(field_name='post_in', widget=DateInput(attrs={'type': 'date'}),
                         label='Поиск по дате',
                         lookup_expr='gt')

    class Meta:
        model = Post
        fields = {
            'post_header': ['iregex'],
            'author': ['exact'],

        }
