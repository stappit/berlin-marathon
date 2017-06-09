import requests
import logging
import json
import csv
import time
import os
from collections import namedtuple


logging.basicConfig(filename='scrape.log', level=logging.DEBUG)


def get_json(year, page):
    """
    Return the json data for the given year.
    """

    url = "http://www.bmw-berlin-marathon.com/files/addons/scc_events_data/ajax.results.php"
    params =  {'t': 'BM_{}'.format(year), 'ci': 'MAL', 'page': str(page)}
    response = requests.get(url, params=params)
    logging.debug('fetched year {0} page {1}'.format(year, page))
    response.raise_for_status()
    time.sleep(1)

    return response.json()


Meta = namedtuple('Meta', ('page', 'n_pages', 'n_rows'))


def get_metadata(j):
    """
    Return metadata about the records for the given year.
    """
    page = int(j.get('page', 1))
    n_pages = int(j.get('total', 1))
    n_rows = int(j.get('records', 0))
    return Meta(page, n_pages, n_rows)


Row = namedtuple('Row', ( 
    'id',
    'place',
    'bib',
    'surname',
    'forename',
    'team',
    'nationality',
    'yob',
    'sex',
    'age_class',
    'age_class_place',
    'net_time',
    'clock_time',
))


def get_rows(j):
    """
    Return a generator of rows.
    """
    for entry in j.get('rows', []):
        cell = entry.get('cell', [])
        yield Row(*cell)


def get_data(j):
    return get_metadata(j), get_rows(j)


def get_jsons(year):
    """
    Return a generator of all json pages for given year.
    """
    j = get_json(year, 1)
    yield j
    meta = get_metadata(j)
    for page in range(2, meta.n_pages + 1):
        try:
            j = get_json(year, page)
        except Exception as e:
            logging.exception(e)
            logging.critical('retry:{0}:{1}'.format(year, page))
        else:
            yield j



def main(years, directory='data'):
    """
    Get json data from Berlin marathon API and write it to a file in csv format.
    """

    filename = os.path.join(directory, 'berlin_marathon_times_dirty.csv')
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(Row._fields + ('year',))
        for year in years:
            for j in get_jsons(year):
                try:
                    meta, rows = get_data(j)
                    jname = os.path.join(directory, 
                                         '{0}-{1}.json'.format(year, meta.page))
                    with open(jname, 'w') as f:
                        json.dump(j, f)
                    [writer.writerow(row + (year,)) for row in rows]
                    logging.debug('Success: year {0} page {1}'.format(year,
                                                                      meta.page))
                except Exception as e:
                    logging.exception(e)


if __name__ == '__main__':
    # years = range(2015, 2017)
    # main(years)

    ###

    for year, page in [(2015, 334), (2015, 245), (2016, 61)]:
        j = get_json(year, page)
        meta, rows = get_data(j)
        jname = os.path.join('data', 
                             '{0}-{1}.json'.format(year, meta.page))
        with open(jname, 'w') as f:
            json.dump(j, f)

        with open('data/berlin_marathon_times_dirty.csv', 'a') as f:
            writer = csv.writer(f)
            [writer.writerow(row + (year,)) for row in rows]
