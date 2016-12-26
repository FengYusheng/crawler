import os
import json
import csv
import multiprocessing

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as c:
        csvReader = csv.DictReader(c)
        comments = [c for c in csvReader]
        with open(json_file, 'w') as j:
            json.dump(comments, j)


if __name__ == '__main__':
    # with open('youku_comments/episode22.csv', 'r') as csv_file:
    #     csvReader = csv.DictReader(csv_file)
    #     j = [c for c in csvReader]
    #     with open('youku_comments/episode22.json', 'w') as json_file:
    #         json.dump(j, json_file)

    if not os.path.exists('./json_files'):
        os.mkdir('./json_files')

    process_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(process_count)
    csv_files = ['youku_comments/episode{0}.csv'.format(i) for i in range(1, 43)]
    for csv_file in csv_files:
        json_file = 'json_files/' + csv_file.split('/')[1].split('.')[0] + '.json'

        pool.apply_async(csv_to_json, args=(csv_file, json_file))

    pool.close()
    pool.join()
    print 'End.'
