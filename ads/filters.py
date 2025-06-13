import django_filters
from .models import Ad


class AdFilter(django_filters.FilterSet):
    "Фильтр для модели Ad, позволяющий искать объявления по частичному совпадению в заголовке (без учета регистра)."
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['title']
