from celery import shared_task
import csv
from .models import Csvfile
from time import sleep
from celery_progress.backend import ProgressRecorder


@shared_task(bind=True)
def csvfilegenerate(self, listDataCSV, fake_listData, filenameDate, numberRecord, now):
    sleep(1)
    progress_recorder = ProgressRecorder(self)

    for i in range(50):
        progress_recorder.set_progress(i + 1, numberRecord, f'Row {i} out of {numberRecord}')

    with open(f'media/csvfiles/{filenameDate}', 'w', encoding='UTF8', newline='') as f:
        writer2 = csv.writer(f)
        writer2.writerow(listDataCSV)
        for data in fake_listData:
            writer2.writerow(data)

    csvObject = Csvfile.objects.create(filename=filenameDate, file_created=now)
    csvObject.save()

    return f'"{filenameDate}" Has been successfully saved! ' \
           f'\nYou can see generated file from: https://csvfakedatagenerator.herokuapp.com//listfiles/' \
           f'\n OR By clicking the button bellow:'


