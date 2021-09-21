import django_filters
from django.contrib.auth import models

from cadre_bud.models import Pos6


class pos_filter(django_filters.FilterSet):
    class Meta:
        model=Pos6
        fields=['scf']
        