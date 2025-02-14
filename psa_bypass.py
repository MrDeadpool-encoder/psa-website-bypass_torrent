import time
import requests 
import re
import cloudscraper 
import concurrent.futures
from bs4  import BeautifulSoup


def try2link_bypass(url):
	client = cloudscraper.create_scraper(allow_brotli=False)
	
	url = url[:-1] if url[-1] == '/' else url
	
	params = (('d', int(time.time()) + (60 * 4)),)
	r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
	
	soup = BeautifulSoup(r.text, 'html.parser')
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }	
	time.sleep(7)
	
	headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
	
	bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
	return bypassed_url.json()["url"]
		

def try2link_scrape(url):
	client = cloudscraper.create_scraper(allow_brotli=False)	
	h = {
	'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	}
	res = client.get(url, cookies={}, headers=h)
	url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
	print(try2link_bypass(url))
    

def psa_bypasser(psa_url):
	client = cloudscraper.create_scraper(allow_brotli=False)
	r = client.get(psa_url)
	soup = BeautifulSoup(r.text, "html.parser")
	tag = soup.find_all("noindex", string=" TORRENT")
	with concurrent.futures.ThreadPoolExecutor() as executor:
		for link in tag:
			try:
				exit_gate = link.a.get("href")
				executor.submit(try2link_scrape, exit_gate)
			except: pass
 
psa_bypasser("https://psa.pm/movie/bubble-2022/")
