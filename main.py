import sys
import pickle
from bs4 import BeautifulSoup
import requests
import tqdm
import utils.info as info
sys.setrecursionlimit(10**6)


class Drug_scraper:
    def __init__(self):
        self.drug_id_list = self.get_id_list()
        self.url = 'http://idrblab.net/ttd/data/drm/details/'

        self.base_table_rows = self.base_table()
        self.mutation_table_rows = self.mutation_table()
        self.save_pickle()

    def get_id_list(self):
        drug_id_list = []

        for idx in range(10):
            url = f'http://idrblab.net/ttd/search/ttd/drm-drug?page={idx}'

            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                ul = soup.select(
                    '#fixed-width-page > div > main > div.col-md-12 > table > tbody > tr:nth-child(n) > th.h-center > a')
                for data in ul:
                    drug_id_list.append(data.text)
            else:
                break

        return drug_id_list

    def base_table(self):
        for drug_id in tqdm.tqdm(self.drug_id_list):
            url = 'http://idrblab.net/ttd/data/drm/details/' + drug_id
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = []
            for DRM in soup.find_all('tr', {'class': 'blue-bg'}):
                row = [None, None, None]
                for tr in soup.find_all('tr'):
                    row[0] = DRM.find('td').text
                    try:
                        if tr.find('th').text == 'Species':
                            row[1] = tr.find('td').text
                        elif tr.find('th').text == 'Targeted Disease':
                            row[2] = tr.find('td').text
                    except:
                        pass
                rows.append(row)
        return rows

    def mutation_table(self):
        for drug_id in tqdm(self.drug_id_list):
            rows = []
            url = 'http://idrblab.net/ttd/data/drm/details/' + drug_id
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            for DRM in soup.find_all('tr', {'class': 'blue-bg'}):
                for table in soup.find_all('table', {'class': 'table table-responsive table-bordered table-no-bottom-margin'}):
                    # print("Mutation_info:", table.find('td', {'class': 'td-blue-bg mutation-info'}).text)
                    row = [None, None, None, None, None, None]
                    for table_tr in table.find_all('tr'):
                        row[0] = drug_id
                        row[1] = DRM.find('td').text
                        if table_tr.find('th').text == 'Mutation info':
                            row[2] = table_tr.find('td').text[:8]
                            row[3] = table_tr.find('td').text[10:]
                        elif table_tr.find('th').text == 'Mutation Frequency':
                            row[4] = table_tr.find('td').text
                        elif table_tr.find('th').text == 'Level of Resistance':
                            row[5] = table_tr.find('td').text
                    rows.append(row)

        return rows

    def save_pickle(self):
        with open('./data/base_table.pickle', 'wb') as f:
            pickle.dump(self.base_table_rows, f)
        with open('./data/mutation_table.pickle', 'wb') as f:
            pickle.dump(self.mutation_table_rows, f)


if __name__ == "__main__":
    Drug_scraper()
