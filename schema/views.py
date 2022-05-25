import os
from io import StringIO
from itertools import cycle
from random import randint
from django.core.files.base import ContentFile
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from faker import Faker
import csv
from datetime import datetime
import mimetypes
from .tasks import csvfilegenerate

from .models import *
from .forms import ColumnForm, ColumnFormSet, SchemaForm

def create_schema(request):
    schemaform = SchemaForm(request.POST or None)
    formset = ColumnFormSet(request.POST or None)
    form = ColumnForm(request.POST or None)
    # columns = Column.objects.filter(schema_name=schemaform)
    if request.method == "POST":
        if all([formset.is_valid(), schemaform.is_valid()]):
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save(commit=False)
                column.schema_name = schema
                column.save()
            return redirect("listschema")
        else:
            return render(request, "partials/column_form.html", context={
                "form": form
            })
    # else:
    context = {
        "schemaform": schemaform,
        "formset": formset,
        "form": form
    }
    return render(request, 'create_schema.html', context)

def create_column(request, pk):
    schema = Schema.objects.get(id=pk)
    columns = Column.objects.filter(schema_name=schema)
    form = ColumnForm(request.POST or None)
    formset = ColumnFormSet(request.POST or None)

    if request.method == "POST":
        if (form.is_valid()) and (form.is_valid()):
            formset.instance = schema
            formset.save()

            column = form.save(commit=False)
            column.schema_name = schema
            column.save()

            return redirect("detail-column", pk=column.id)


    context = {
        "form": form,
        "formset": formset,
        "schema": schema,
        "columns": columns
    }

    return render(request, "create_column.html", context)

def create_column_form(request):

    form = ColumnForm(request.POST or None)
    context = {
              "form": form
             }
    return render(request, "partials/column_form.html", context)

def list_schema(request):
    schemas = Schema.objects.all()
    context = {
        "schemas":schemas
    }



    return render(request, 'list_schema.html', context)


def detail_column(request, pk):
    column = get_object_or_404(Column, id=pk)
    context = {
        "column": column
    }
    return render(request, "partials/detail_column.html", context)

def delete_scheme(request, pk):
    schema = Schema.objects.get(pk = pk)
    schema.delete()

    return HttpResponse('')

def edit_scheme(request, pk):
    scheme = Schema.objects.get(pk=pk)
    schemaform = SchemaForm(request.POST or None, instance=scheme)
    formset = ColumnFormSet(request.POST or None, instance=scheme)
    form = ColumnForm(request.POST or None, instance=scheme)
    # columns = Column.objects.filter(schema_name=schemaform)

    context = {
        "schemaform": schemaform,
        "formset": formset,
        "scheme": scheme
    }
    if request.method == "POST":
        if all([formset.is_valid(), schemaform.is_valid()]):
            schema = schemaform.save()
            formset.instance = schema
            formset.save()

            if form.is_valid():
                column = form.save(commit=False)
                column.schema_name = schema
                column.save()
            # return redirect("listschema")
            return HttpResponseRedirect(reverse('listschema'))

        if request.htmx:
            return HttpResponseRedirect(reverse('listschema'))

    return render(request,"create_schema.html", context)

def generate_csv(request, pk=None):


    schema = Schema.objects.get(pk=pk)
    delimiter = schema.column_separator
    string_char_symbol = schema.string_charachter

    now = datetime.now()
    dateTimeString = now.strftime("%Y-%m-%d-%H:%M:%S")

    filenameDate = f"{dateTimeString}.csv"

    filename = filenameDate
    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response, delimiter=delimiter)

    listData = []

    for i in schema.column_set.all():
        listData.append([i.column_name, i.order, i.type_column])

    listData.sort(key=lambda x: x[1])
    listDataCSV = [i[0] for i in listData]
    #print(listDataCSV)

    fake = Faker()
    name_person = cycle([fake.name(), fake.name()])
    rows = []

    #actual names from schemas, not type
    full_name_person = " "
    job_name = " "
    email_address = " "
    domain_name = " "
    tel_number = " "
    company_name = " "
    text_content = " "
    integerValue = 0
    address_value = " "
    date_value = " "

    for i in listData:
        if i[2] == 'Full name':
            full_name_person = i[0]
        elif i[2] == 'Job':
            job_name = i[0]
        elif i[2] == 'Email':
            email_address = i[0]
        elif i[2] == 'Domain name':
            domain_name = i[0]
        elif i[2] == 'Phone number':
            tel_number = i[0]
        elif i[2] == 'Company name':
            company_name = i[0]
        elif i[2] == 'Text':
            text_content = i[0]
        elif i[2] == 'Integer':
            integerValue = i[0]
        elif i[2] == 'Address':
            address_value = i[0]
        elif i[2] == 'Date':
            date_value = i[0]

    listOfTupleDict = []
    #numberRecord = int(request.POST.get('numberOfRecord'))
    numberRecord = 10

    for i in range(numberRecord):
        for i in listDataCSV:
            if i == full_name_person:
                person_name_data = string_char_symbol+fake.name()+string_char_symbol
                listOfTupleDict.append((full_name_person, person_name_data ))
            elif i == job_name:
                job_data_content = string_char_symbol + fake.job() + string_char_symbol
                listOfTupleDict.append((job_name,job_data_content ))
            elif i == domain_name:
                domain_name_data = string_char_symbol + fake.url() + string_char_symbol
                listOfTupleDict.append((domain_name, domain_name_data))
            elif i == email_address:
                if domain_name:
                    email_address_data = string_char_symbol + fake.company_email() + string_char_symbol
                    listOfTupleDict.append((email_address, email_address_data ))
                else:
                    email_address_data = string_char_symbol + fake.company_email() + string_char_symbol
                    listOfTupleDict.append((email_address, email_address_data))
            elif i == tel_number:
                listOfTupleDict.append((tel_number, fake.phone_number()))
            elif i == company_name:
                company_name_data = string_char_symbol + fake.company() + string_char_symbol
                listOfTupleDict.append((company_name,company_name_data))
            elif i == text_content:
                text_content_data = string_char_symbol + fake.sentence(nb_words=10) + string_char_symbol
                listOfTupleDict.append((text_content,text_content_data ))
            elif i == integerValue:
                listOfTupleDict.append((text_content, randint(1, 1000)))
            elif i == address_value:
                address_data = fake.country()+ " "+fake.city()+" " + fake.street_address()
                address_string_data = string_char_symbol + address_data + string_char_symbol
                listOfTupleDict.append((address_value, address_string_data))
            elif i == date_value:
                listOfTupleDict.append((date_value, fake.date()))

        someDict = dict(listOfTupleDict)
        rows.append(someDict)

    # csv_buffer = StringIO()
    # writer = csv.writer(csv_buffer)

    fake_listData = [list(rows[i].values()) for i in range(len(rows))]
    writer.writerow(listDataCSV)
    for data in fake_listData:
        writer.writerow(data)

    now = datetime.now()
    dateTimeString = now.strftime("%Y-%m-%d-%H:%M:%S")

    filenameDate = f"{dateTimeString}.csv"

    # with open(f'media/csvfiles/{filenameDate}', 'w', encoding='UTF8', newline='') as f:
    #     writer2 = csv.writer(f)
    #     writer2.writerow(listDataCSV)
    #     for data in fake_listData:
    #         writer2.writerow(data)
    #
    # csvObject = Csvfile.objects.create(filename=filenameDate,file_created=now)
    # csvObject.save()

    task = csvfilegenerate.delay(listDataCSV, fake_listData, filenameDate, numberRecord, now)
    context = {
        'task_id':task.id,
    }

    return render(request, 'generateFile.html', context)

def listFilesAndDownload(request):
    csvObject = Csvfile.objects.all()

    context = {
        "csvObject":csvObject
    }
    return render(request, 'filetable.html',context)

def downloadFileCsv(request, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + f'/media/csvfiles/{filename}'

    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


def generatefilecsv(request, pk):
    schema = Schema.objects.get(pk=pk)

    context = {
        "schema": schema
    }
    return render(request,'generateFile.html', context)