from django.contrib import admin
from . models import *

# Register Django admin views for various models

# Register the PriceUnit model with the Django admin site.
admin.site.register(PriceUnit)

# Register the WeightUnit model with the Django admin site.
admin.site.register(WeightUnit)

# Register the TimeUnit model with the Django admin site.
admin.site.register(TimeUnit)

# Register the QuotationDocType model with the Django admin site.
admin.site.register(QuotationDocType)

# Register the Quotation model with the Django admin site.
admin.site.register(Quotation)