import requests
from bs4 import BeautifulSoup as bs
from difflib import SequenceMatcher

class Scraper():
	def __init__(self):
		self.egov_services_url = "https://www.e-gov.az/az/services/"
		self.dxr_services_url = "http://dxr.az/dovlet-xidmetleri?page={}"
		self.egov_services = []
		self.dxr_services = []
		self.egov_dxr = []
		self.not_in_egov = []
		self.not_in_dxr = []
		self.egov_dxr_with_percent = []

	def egov(self):
		r = requests.get(self.egov_services_url, verify=False)
		b = bs(r.content, 'html.parser')
		services = b.find('ul', {"class":"menu-accordion"})
		links = services.find_all('a', text=True)
		for link in links:
			self.egov_services.append(link.getText())

	def dxr(self):
		for n in range(1, 50):
			print(self.dxr_services_url.format(str(n)))
			r = requests.get(self.dxr_services_url.format(str(n)))
			b = bs(r.content, 'html.parser')
			check_page = b.find('h3', {"class":"center"})
			if check_page:
				break
			services_ul = b.find("ul", {"id":"search_list"})
			services_texts = services_ul.find_all("a", {"class":"name"})
			for i in services_texts:
				clear_sentence = i.getText().replace("  ", "").replace("\t", "").replace("\n", "") 
				if clear_sentence[0] == " ":
					clear_sentence = clear_sentence[1:]
				if clear_sentence[-1] == " ":
					clear_sentence = clear_sentence[:-1]
				self.dxr_services.append(clear_sentence)

	def compare(self):
		for egov_service in self.egov_services:
			if egov_service in self.dxr_services:
				if egov_service not in self.egov_dxr:
					self.egov_dxr.append(egov_service)

	def compare_with_percent(self):
		for egov_service in self.egov_services:
			for dxr_service in self.dxr_services:
				match_percent = SequenceMatcher(None, egov_service, dxr_service).ratio()*100
				if match_percent>97:
					if egov_service not in self.egov_dxr_with_percent:
						self.egov_dxr_with_percent.append(egov_service) 
						break

	def not_in_dxr_func(self):
		for egov_service in self.egov_services:
			if egov_service not in self.dxr_services:
				self.not_in_dxr.append(egov_service)

	def not_in_egov_func(self):
		for dxr_service in self.dxr_services:
			if dxr_service not in self.egov_services:
				self.not_in_egov.append(dxr_service)


