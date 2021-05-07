try:

    import requests
    from bs4 import BeautifulSoup
    import random
    import pandas as pd

except:
    print(" Library Not Found !")


class Random_Proxy(object):

    def __init__(self):
        self.__url = 'https://www.sslproxies.org/'
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }
        self.random_ip = []
        self.random_port = []

    def __random_proxy(self):
        """
        This is Private Function Client Should not have accesss
        :return: Dictionary object of Random proxy and port number
        """

        r = requests.get(url=self.__url, headers=self.__headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Get the Random IP Address
        for x in soup.findAll('td')[::8]:
            self.random_ip.append(x.get_text())

        # Get Their Port
        for y in soup.findAll('td')[1::8]:
            self.random_port.append(y.get_text())

        # Zip together
        z = list(zip(self.random_ip, self.random_port))

        # This will Fetch Random IP Address and corresponding PORT Number
        number = random.randint(0, len(z)-50)
        ip_random = z[number]

        # convert Tuple into String and formart IP and PORT Address
        ip_random_string = "{}:{}".format(ip_random[0], ip_random[1])

        # Create a Proxy
        proxy = {'https': ip_random_string}

        # return Proxy
        return proxy

    def Proxy_Request(self, request_type='get', url='', **kwargs):
        """

        :param request_type: GET, POST, PUT
        :param url: URL from which you want to do webscrapping
        :param kwargs: any other parameter you pass
        :return: Return Response
        """
        while True:
            try:
                proxy = self.__random_proxy()
                print("Using Proxy {}".format(proxy))
                r = requests.request(
                    request_type, url, proxies=proxy, headers=self.__headers, timeout=8, **kwargs)
                return r
                break
            except:
                pass


def Extract(URL):
    proxy = Random_Proxy()
    r = proxy.Proxy_Request(url=URL, request_type='get')
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find_all('div', class_='top_space')
    for div in divs:
        company_name = div.find('a').text
        Eligibility = div.find('span', class_='qualifications').text
        job_desc = div.find('span', {'class': 'desc'}).text.replace('\n', '')
        try:
            experience = div.find(
                'div', {'class': 'col-md-3 col-xs-3 col-lg-3 padding-none'}).text
        except:
            experience = ' '
        Location = div.find(
            'div', {'class': 'col-md-5 col-xs-5 col-lg-5 padding-none'}).text
        Last_date = div.find(
            'div', {'class': 'col-md-4 col-xs-4 col-lg-4 padding-none'}).text

        jobs = {
            'company_name': company_name,
            'Eligibility': Eligibility,
            'job_description': job_desc,
            'experience': experience,
            'location': Location,
            'Last_date': Last_date
        }
        job_list.append(jobs)


job_list = []


# extracting data from each page of the website
def page(Pno):
    URL = f"https://www.freshersworld.com/jobs/jobsearch/python-developer-jobs-for-be-btech-in-bangalore?{Pno}"
    return URL


for i in range(1, 51, 10):
    c = page(i)
    Extract(c)

dataframe = pd.DataFrame(job_list)
dataframe.to_csv('jobs.csv')
data = pd.read_csv('jobs.csv')
data.drop_duplicates(subset=None, keep='first', inplace=True)
data.to_csv('jobs1.csv')
