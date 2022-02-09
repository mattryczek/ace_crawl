# ACE Data Export
Parse and export US CBP Official Notice of Extension, Suspension and Liquidation entries. While the data is available, there is no API to request large (any?) number of records, consecutive or otherwise. This tool aims to fill that deficiency.

## Usage
+ Install `requests` if you have not already
`py -m pip install requests`

Run `main.py`

```
py main.py
```
The tool will ask you for the starting page and will fetch records in batches of 100 (max available from API at once). You will also need to enter a valid port of entry. Currently supported ports are listed below; new mappings can be added to expand this list.

```
{1001: 'New York', 2809: 'San Francisco', 3901: 'Chicago', 5301: 'Houston'}
```

## Output
The tool outputs CSV files with naming scheme `portname date_of_run.csv`
