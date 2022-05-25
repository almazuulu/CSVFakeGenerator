from django.contrib import admin
from .models import Schema, Column, Csvfile

class ColumnInlineAdmin(admin.TabularInline):
    model = Column
    extra = 5

class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInlineAdmin]

class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('file_created', 'filename')
admin.site.register(Schema, SchemaAdmin)
admin.site.register(Csvfile, CSVFileAdmin)
