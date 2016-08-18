import csv
with open('../src/url_args.csv', 'r') as csv_fp:
    csvReader = csv.DictReader(csv_fp)
    for row in csvReader:
        print row
