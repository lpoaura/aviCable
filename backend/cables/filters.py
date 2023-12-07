from functools import reduce

from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework_gis.filters import InBBoxFilter

from .models import Diagnosis, Operation


class DiagnosisFilter(filters.FilterSet):
    """Filter for Diagnosis instances:

    Allow to filter on object type (refer django_rest_polymorphique)
    - by infrastructure type id (type) => filter based on polymorphic_ctype_id field of Infrastructure
    - by type model name (type_model) => filter based on model from django content_type table field matching polymorphic_ctype_id in Infrastructure
    """

    type = filters.NumberFilter(
        field_name="infrastructure__polymorphic_ctype_id"
    )
    type_model = filters.CharFilter(
        field_name="infrastructure__polymorphic_ctype__model"
    )

    class Meta:
        model = Diagnosis
        fields = ["type", "type_model"]


class OperationFilter(filters.FilterSet):
    """Filter for Operation instances:

    Allow to filter on object type (refer django_rest_polymorphique)
    - by infrastructure type id (type) => filter based on polymorphic_ctype_id field of Infrastructure
    - by type model name (type_model) => filter based on model from django content_type table field matching polymorphic_ctype_id in Infrastructure
    """

    type = filters.NumberFilter(
        field_name="infrastructure__polymorphic_ctype_id"
    )
    type_model = filters.CharFilter(
        field_name="infrastructure__polymorphic_ctype__model"
    )

    class Meta:
        model = Operation
        fields = ["type", "type_model"]


class InfrstrInBboxFilter(InBBoxFilter):
    def filter_queryset(self, request, queryset, view):
        filter_fields = getattr(view, "bbox_filter_fields", None)
        include_overlapping = getattr(
            view, "bbox_filter_include_overlapping", False
        )
        if include_overlapping:
            geoDjango_filter = "bboverlaps"
        else:
            geoDjango_filter = "contained"

        if not filter_fields:
            return queryset

        bbox = self.get_filter_bbox(request)
        if not bbox:
            return queryset
        q_objects = [
            Q(**{"%s__%s" % (filter_field, geoDjango_filter): bbox})
            for filter_field in filter_fields
        ]
        combined_q_objects = reduce(lambda x, y: x | y, q_objects)
        print(combined_q_objects)
        return queryset.filter(combined_q_objects)
