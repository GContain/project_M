from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Board,BoardAdmin)