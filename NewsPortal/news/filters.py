from django_filters import FilterSet, DateFromToRangeFilter, ModelChoiceFilter, CharFilter, ChoiceFilter
from django_filters.widgets import DateRangeWidget
from .models import Post, Category


class PostFilter(FilterSet):
    position = ChoiceFilter(
        field_name='position',
        choices=Post.POSITIONS,
        label='Type',
    )

    name = CharFilter(
        field_name='name',
        label='Name',
        lookup_expr='icontains'
    )

    category = ModelChoiceFilter(
        field_name='category',
        required=False,
        queryset=Category.objects.all(),
        label='Category'
    )

    date = DateFromToRangeFilter(
        field_name='post_time',
        widget=DateRangeWidget(attrs={'type': 'date'}),
        label='Date'
    )

    class Meta:
        model = Post
        fields = [
            'position',
            'name',
            'category',
            'date'
        ]
