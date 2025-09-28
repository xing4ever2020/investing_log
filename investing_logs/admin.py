from django.contrib import admin

# Register your models here.

from .models import Instrument, Entry


admin.site.register(Instrument)
admin.site.register(Entry)
