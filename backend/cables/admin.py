from commons.admin import GisModelAdmin
from django.contrib import admin

from .models import Diagnosis, Line, LineOperation, Operation, Point, PointOperation

admin.site.register(Point, GisModelAdmin)
admin.site.register(Line, GisModelAdmin)
admin.site.register(Diagnosis)
# admin.site.register(Operation)
admin.site.register(PointOperation, GisModelAdmin)
admin.site.register(LineOperation, GisModelAdmin)
