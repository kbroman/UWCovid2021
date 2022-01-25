#!/usr/bin/env python
# from Dan Fitch, https://gist.github.com/dgfitch/b6ca1cc61b4795e698cefdf672a90f23

import re
import requests
from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()

r = session.get('https://covidresponse.wisc.edu/dashboard/')


def extract_regex(pattern, value):
    m = re.search(pattern, value)
    if m:
        g = m.groups()
        return [int(g[0])]
    else:
        return [0]

def extract_numbers(s):
    # In the format: 'Students: 0 positive tests<br>7-day average: 4.9<br><br>Employees: 0 positive tests<br>7-day average: 1.0'
    # But may be missing employees
    students = extract_regex(r"Students: (\d+) ", s)
    employees = extract_regex(r"Employees: (\d+) ", s)
    return students + employees

def pad_with_zero(val):
    val = int(val)
    if val < 10:
        return "0" + str(val)
    else:
        return str(val)

def reform_date(s):
    m = re.search("^([A-Za-z]+) (\d+)$", s)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    if m:
        g = m.groups()
        month = pad_with_zero(months.index(g[0])+1)
        if int(month) < 8:
            year = '2022'
        else:
            year = '2021'
        day = pad_with_zero(g[1])
        return(year + "-" + month + "-" + day)
    else:
        return["NA"]

def extract_data(chart):
    # grab date (like "August 7")
    dates = chart.xpath('//g/@data-tooltip_label')
    dates = [reform_date(x) for x in dates]
    dates_data = pd.DataFrame(dates)
    dates_data.columns = ['date']

    tooltips = chart.xpath('//g/@data-tooltip_annotation')
    data = pd.DataFrame([extract_numbers(x) for x in tooltips])
    data.columns = ['students', 'employees']

    return pd.concat([dates_data, data], axis=1)

positive_chart = r.html.find('.svg-bar-chart', first=True)
tests_chart = r.html.find('#chart-covid-tests', first=True)

positive = extract_data(positive_chart)
tests = extract_data(tests_chart)

positive.columns = ['Date', 'Positive_students', 'Positive_employees']
tests.columns = ['date', 'Total_students', 'Total_employees']
tests = tests[['Total_students', 'Total_employees']]

data = pd.concat([positive, tests], axis=1)
data = data[["Date","Total_employees","Total_students","Positive_employees","Positive_students"]]
data.to_csv('uw_covid_2022.csv', index=False)
