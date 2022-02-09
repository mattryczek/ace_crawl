import requests
import json, datetime, csv, time

ports = {1001: 'New York', 2809: 'San Francisco', 3901: 'Chicago', 5301: 'Houston'}
keys = ['postedDate', 'eventDate', 'voidedDate', 'event', 'basis', 'action', 'entryNumber', 'portOfEntry', 'entryDate', 'entryType', 'teamNumber']
ace_url = 'https://aceservices.cbp.dhs.gov/LBNotice/search'

f = open('body.json',)
body = json.load(f)

start = int(input('Enter start page: '))
port = int(input('Enter port of entry: '))

filename = f'{ports.get(port)} {str(time.strftime("%m.%d.%Y."))}csv'

(body['dtPageVars']['start']) = int(start) * 100
(body['searchFields']['portOfEntry']) = port

record_start = int(body['dtPageVars']['start'])

print()
print(f'Creating file: {filename}')
print(f'Starting index >>{str(record_start)}<< (Page {int((record_start+100)/100)})')
print('Using page size ' + str(body['dtPageVars']['length']))
print()
print('Requested keys (in respective order):')
print(*keys, sep=',')
print()
print('Fetching search info...', end='')

data = requests.post(ace_url, json=body)
resp = json.loads(data.text)

print(' ✔️' if data.status_code == 200 else f'Error {data.status_code}')

num_records = resp['data']['recordsFiltered']
num_pages = int(num_records/100) + 1

print(f'Received {num_records} records ({num_pages} pages)\n')

resp_data = resp['data']['data']

with open(filename, "w", newline='') as fp:
    wr = csv.writer(fp, dialect='excel')

    print('Writing requested keys to header...', end='')
    wr.writerow(keys)
    print(' ✔️')

    print('Writing first page to CSV...', end='')
    for i in resp_data:
        csv_row = [i[j] for j in keys]

        try:
            csv_row[0] = datetime.date.fromtimestamp(csv_row[0]/1000)
        
        except TypeError:
            csv_row[0] = ''

        try:
            csv_row[1] = datetime.date.fromtimestamp(csv_row[1]/1000)

        except TypeError:
            csv_row[1] = ''

        try:
            csv_row[8] = datetime.date.fromtimestamp(csv_row[8]/1000)

        except TypeError:
            csv_row[8] = ''

        wr.writerow(csv_row)

    print(' ✔️')

    for i in range (start,num_pages):
        body['dtPageVars']['start'] = i * 100

        print(f'({((i - start + 1) / (num_pages - start))*100:.2f}%) Fetching page {i+1}', end='', flush=True)

        # for _ in range(1,0,-1):
        #     print('.', end='', flush=True)
        #     time.sleep(1)

        data = requests.post(ace_url, json=body)

        print(' ✔️' if data.status_code == 200 else f'Error {data.status_code}')

        resp = json.loads(data.text)
        resp_data = resp['data']['data']

        for j in resp_data:
            csv_row = [j[k] for k in keys]

            try:
                csv_row[0] = datetime.date.fromtimestamp(csv_row[0]/1000)
            
            except TypeError:
                csv_row[0] = ''

            try:
                csv_row[1] = datetime.date.fromtimestamp(csv_row[1]/1000)

            except TypeError:
                csv_row[1] = ''

            try:
                csv_row[8] = datetime.date.fromtimestamp(csv_row[8]/1000)

            except TypeError:
                csv_row[8] = ''

            wr.writerow(csv_row)

