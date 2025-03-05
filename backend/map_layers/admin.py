from django.contrib import admin

from commons.admin import GisModelAdmin

from .models import (
    BaseLayers,
    VectorLayerConfig,
    VectorLayerData,
    VectorLayerTheming,
)


class VectorLayerDataAdmin(GisModelAdmin):
    list_display = (
        "config",
        "data",
    )
    list_filter = ("config",)


class VectorLayerThemingAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "min",
        "max",
        "numeric_value",
        "string_value",
        "style",
        "condition_path",
    )
    list_filter = ("config",)


class VectorLayerConfigAdmin(admin.ModelAdmin):
    list_display = ("category", "layer_name")
    list_filter = ("category",)


class BaseLayerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "attribution", "default", "layer_type")


admin.site.register(VectorLayerTheming, VectorLayerThemingAdmin)
admin.site.register(VectorLayerConfig, VectorLayerConfigAdmin)
admin.site.register(VectorLayerData, VectorLayerDataAdmin)
admin.site.register(BaseLayers, BaseLayerAdmin)
