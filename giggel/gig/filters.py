import django_filters

from .models import Gig

class GigFilter(django_filters.FilterSet):
    gig_artist = django_filters.CharFilter(lookup_expr='icontains')
    gig_venue = django_filters.CharFilter(lookup_expr='icontains')
    gig_date = django_filter.DateFromToRangeFilter()
    class Meta:
        model = Gig
        fields = ['gig_artist', 'gig_venue', 'gig_date']
        widgets = {
                'gig_artist': forms.TextInput(attrs={'class':'form-control'}),
        }
