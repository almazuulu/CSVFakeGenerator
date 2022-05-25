from django import forms
from django.forms.models import inlineformset_factory
from .models import Column, Schema, Csvfile

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields=('column_name','type_column','order')

class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = "__all__"

class CsvFileForm(forms.Form):
    class Meta:
        model = Csvfile
        fields = "__all__"

class CsvInforForm(forms.ModelForm):
    numberOfRecord = forms.IntegerField()



ColumnFormSet  = inlineformset_factory(
    Schema,
    Column,
    ColumnForm,
    can_delete=True,
    min_num= 5,
    extra= 0
)
