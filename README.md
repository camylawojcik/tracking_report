# :chart_with_upwards_trend: Tracking Pixels Report

This application is a command-line tool that receives a website visitor activity log and outputs a simple report with Unique Visitors and Page View metrics.

## :game_die: Setting up the environment
Before starting, you have to execute some simple steps:

#### Clone the repository:
```bash
git clone https://github.com/camylawojcik/tracking_report.git
```
#### Go to the application folder:
```bash 
cd tracking_report/
```
#### Install the required libs:
```bash 
pip install -r requirements.txt
```

## :rocket: Running the Application
```bash 
python report/tracking_pixels.py "2013-09-01 09:00:00UTC" "2013-09-01 12:00:00UTC" "./samples/example1.log"
```

The application requires 3 positional parameters:
1. Start date for time range filter;
  - Example: 2013-09-01 09:00:00UTC
2. End date for time range filter;
  - Example: 2013-09-01 11:00:00UTC
3. Path to the input log of website visitors.

Optionally, it's possible to save the output in a CSV file using the parameter *-o*:
``` bash
python report/tracking_pixels.py "2013-09-01 09:00:00UTC" "2013-09-01 12:00:00UTC" "./samples/example1.log" -o report.csv
```

A helper is also available by the *-h* option:
``` bash
python report/tracking_pixels.py -h
```

#### :warning: Format of input log
- File must be in txt, csv or log formats; 
- Accepted delimiters: ```| ; , ```
- Mandatory Columns: 
  - timestamp
  - url
  - userid

Layout example:
```bash
|timestamp              |url           |userid|
|2013-09-01 09:00:00UTC |/contact.html |12345 |
```

#### Output Example
```bash
+---------------+-------------+------------+
| url           |   pageviews |   visitors |
|---------------+-------------+------------|
| /contact.html |           6 |          4 |
| /xx.html      |           1 |          1 |
| /xxx.html     |           1 |          1 |
| /xxxx.html    |           6 |          2 |
+---------------+-------------+------------+
```

## :hammer_and_wrench: Technologies
- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Unittest - Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [Tabulate](https://pypi.org/project/tabulate/)

## :female_detective: Testing

The unit tests were built using **UnitTest Framework**, a Python _standard library_, and **Pandas testing functions**.
It can be found in the ```tracking_report/test``` folder.

To run the tests, you have to execute from the application root folder:
```bash
python -m unittest test/test_tracking_pixels.py
```