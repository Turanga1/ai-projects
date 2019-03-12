"""
From:
https://davidroodman.com/blog/2017/11/14/python-program-to-scrape-solar-panel-production-data-from-enphase-website/
"""

# queries Enphase Enlighten username and password
# then downloads panel-level production data for all panels, between dates hard-coded below
# time stamps expressed in Unix epoch time
# inverter ID numbers are not serial numbers; to determine those,
#   go to Devices tab on Enphase Enlighten site, hover mouse over hotlinked
#   serial numbers, and examine associated links
# saves to "Panelproduction.csv"
# prints each date for which data is scraped, along with number of inverters

import requests, csv, os, getpass
from datetime import timedelta, date
from bs4 import BeautifulSoup

start_date = date(2015, 1, 20)
end_date = date(2019, 3, 1)
user_name = input('User name: ')
password = getpass.getpass('Password: ') # this is only working for me in debug mode

os.chdir('C:\\users\\rujjn\\projects')

with open('Panelproduction4.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['time','inverter','power'])

  with requests.Session() as s:
    # log in
    html = s.get('https://enlighten.enphaseenergy.com')
    soup = BeautifulSoup(html.text, 'html.parser')
    token = soup.find('input', attrs={'name': 'authenticity_token'})['value']
    payload = {'user[email]':user_name, 'user[password]':password, 'utf8':'✓', 'authenticity_token': token}
    html = s.post('https://enlighten.enphaseenergy.com/login/login', data=payload)

    for date in (end_date-timedelta(n) for n in range(int((end_date - start_date).days))):
      payload = {'date': str(date)}
      data = s.get('https://enlighten.enphaseenergy.com/systems/173888/inverter_data_x/time_series.json', params=payload).json()
      print (date, len(data))
      for inverter, inverter_data in data.items():
        if inverter != 'date' and inverter != 'haiku':
          for datapoint in inverter_data['POWR']:
            writer.writerow([datapoint[0], inverter, datapoint[1]])
