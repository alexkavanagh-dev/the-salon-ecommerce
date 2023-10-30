from django.contrib import admin
from .models import FAQ, CustomerTestimonial
# Register your models here.


class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'answer',
    )


class testimonialAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'body',
        'approved',
        'created_on',
    )


admin.site.register(FAQ, FAQAdmin)
admin.site.register(CustomerTestimonial, testimonialAdmin)
