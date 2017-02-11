def medinfo():
    infile = open('MedicineList.csv' , 'rb')
    for lines in infile.readlines() :
        gn = lines.split(',')[0]
        d = lines.split(',')[1]
        se = lines.split(',')[2]
