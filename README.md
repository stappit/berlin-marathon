# Berlin Marathon

The official results from the Berlin marathons.
I use the API offered by the [Berlin marathon website](http://www.bmw-berlin-marathon.com/files/addons/scc_events_data/ajax.results.php?) to collect all available results.
Although data exists for every year since 1974, the API only offers the data since 2005.

## Data

* The raw JSON files returned by the API are named `<year>-<page>.json` where `<year>` is the year of the race and `<page>` is the page as numbered by the API.  Each page should have 100 records (except the last pages).
* The dirty CSV file is also created during scraping -- see the [scrape file](scripts/scrape.py).
* The clean CSV file is generated from the dirty CSV file using the [clean notebook](notebooks/clean.ipynb).
* The cleaning process makes use of [country abbreviations](data/countries.csv).  The abbreviation `RKS` has not yet been identified.
* The md5 checksums of csv files can be found in [hashes](hashes).
