from django.db import models
import uuid

# Create your models here.
class Schema(models.Model):
    COLUMN_SEPERATOR = (
        (',', 'Comma(,)'),
        (';', 'Semicolon(;)'),
        ('"', 'Quotes (")'),
    )

    STRING_CHARACTER = (
        ('"','Double-quote(")'),
        ("'", "Single-quote(')")
    )

    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False, max_length=36)
    name  = models.CharField(max_length=200, blank=True, null=True)
    column_separator = models.CharField(max_length=20, null=True, choices=COLUMN_SEPERATOR)
    string_charachter = models.CharField(max_length=50, null=True, choices=STRING_CHARACTER)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']

class Column(models.Model):
    TYPE_COLUMN = (
        ('Full name', 'Full name'),
        ('Job', 'Job'),
        ('Email', 'Email'),
        ('Domain name', 'Domain name'),
        ('Phone number', 'Phone number'),
        ('Company name', 'Company name'),
        ('Text', 'Text'),
        ('Integer', 'Integer'),
        ('Address', 'Address'),
        ('Date', 'Date')
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, max_length=36)
    schema_name = models.ForeignKey(Schema,on_delete=models.CASCADE)
    column_name = models.CharField(max_length=200, blank=True, null=True)
    type_column = models.CharField(max_length=200, null=True, choices=TYPE_COLUMN)
    order = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return self.column_name


class Csvfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, max_length=36)
    file_created = models.DateTimeField(auto_now_add=True, editable=False)
    filename = models.CharField(max_length=200, blank=True, null=True)

    #status = models.CharField(max_length=100, default='processing', blank=True, null=True)
   # csvFile = models.FileField(upload_to="csvfiles/", null=True, blank=True)
    def __str__(self):
        return f'{self.filename}'

    class Meta:
        ordering = ['-file_created']