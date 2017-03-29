import os , sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csvpath = os.path.join(BASE_DIR , '/scripts/database.py')
sys.path.append(BASE_DIR)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

from doctor.models import MedReport

import csv
dataReader = csv.reader(open(csvpath), delimiter=',', quotechar='"')

count = 1
for row in dataReader:
    if row[0] != 'MedUrl' :
        med = MedReport()
        med.med_no = count
        med.medname = row[1]
        med.gname = row[2]
        med.details = row[4]
        med.side_effect = row[3]
        med.save()
        print(count + '.' + med.medname)
        count = count + 1
