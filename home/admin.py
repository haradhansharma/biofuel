from django.contrib import admin
from . models import *

admin.site.register(PriceUnit)
admin.site.register(WeightUnit)
admin.site.register(TimeUnit)
admin.site.register(QuotationDocType)

admin.site.register(Quotation)


