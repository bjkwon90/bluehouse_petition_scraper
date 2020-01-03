from bs4 import BeautifulSoup
from selenium import webdriver
from typing import Union, List
from tqdm import tqdm
import pickle

class Scraper:
    def __init__(self, idx: Union[List, int]):
        self.idx = idx
        self.res = dict()

    def _req(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome('chromedriver', chrome_options=options)
        self.driver.get(url)
        #r = requests.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.driver.quit()
        return self._parse_res(soup)

    def _make_url(self, idx):
        return 'https://www1.president.go.kr/petitions/{}'.format(idx)

    def _parse_res(self, soup):
        try:
            category = soup.find('ul', {'class': 'petitionsView_info_list'}).select('li')[0].text[4:]
        except:
            return None
        title = soup.find('h3', {'class': 'petitionsView_title'}).text
        body = soup.find('div', {'class': 'View_write'}).text.strip()
        counter = soup.find('span', {'class': 'counter'}).text
        try:
            response = soup.find_all('div', {'class': 'pr_tk25'})[-1].text.strip()
        except:
            response = None

        return {'category': category, 'counter': counter, 'title': title, 'body': body, 'response': response}

    def req(self):
        if type(self.idx) == int:
            self.res[self.idx] = self._req(self._make_url(self.idx))
        elif type(self.idx) == list:
            for idx in tqdm(self.idx):
                self.res[idx] = self._req(self._make_url(idx))

    def write(self, fn, pkl=True):
        if pkl:
            with open(fn, 'wb') as f:
                pickle.dump(self.res, f)
        else:
            with open(fn, 'w') as f:
                f.write('{}'.format(self.res))