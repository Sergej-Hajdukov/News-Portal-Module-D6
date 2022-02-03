from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from django.forms import DateInput
from .models import Post, Author, Category


class NewsFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        lookup_expr='exact',
        queryset=Author.objects.all(),
        label='Автор:'
    )

    datetime = DateFilter(
        field_name='release_date',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Поcле даты:'
    )

    class Meta:
        model = Post
        fields = []
