# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from math import ceil
from urllib.parse import urljoin

from apps.base.configs import scraper_url

class BookScraper:
	"""
	Modelates the parsing methods to 
	get the Books and Category objects
	"""
	request = None
	parser = None
	ratings = {
		'One': 1,
		'Two': 2,
		'Three': 3,
		'Four': 4,
		'Five': 5
	}

	def __init__(self):
		self.request = requests.get(scraper_url)
		self.parser = BeautifulSoup(self.request.content, 'html.parser')

	def get_categories(self):
		"""
		Get the categories from the main page
		"""

		categories = []

		# Get the <aside> element where the categories are
		menu = self.parser.find('aside').find('ul').find('li').find('ul')
		categories_tag = menu.find_all('li')
		for index, element in enumerate(categories_tag):
			category = element.find('a')
			categories.append({
				'id': index + 1,
				'name': category.string.string.strip(),
				'link': category['href'].replace('index.html', '')
			})
		
		return categories

	def _book_generator(self, category):
		"""
		Returns a generator of all the books
		of a certain category
		"""
		category_request = requests.get(scraper_url + category['link'])
		category_parser = BeautifulSoup(category_request.content, 'html.parser')

		# Get the total number of books in the category
		result_numbers = category_parser.find('form', attrs={'method':'get'}).find_all('strong')
		total = int(result_numbers[0].string)
		if(len(result_numbers) > 1):
			maximum = int(result_numbers[2].string)
			page = ceil(total/maximum)
		else:
			page = 1
		
		# For every page it must return all the books
		for current_page in range(page):
			link = scraper_url + category['link'] + 'page-{}.html'.format(current_page + 1) if page > 1 else scraper_url + category['link'] + 'index.html'

			category_request = requests.get(link)
			category_parser = BeautifulSoup(category_request.content, 'html.parser')

			books_block = category_parser.find_all('article', attrs={'class': 'product_pod'})
			yield from self._book_block_generator(books_block, category)


	def _book_block_generator(self, books_block, category):
		"""
		Returns a generator of all the books of a 
		category, based on their information block.
		A information block is the preview of the book
		inside a category, that includes the 
		thumbnail, price, stock availability and 
		its short title.
		"""
		for book_block in books_block:
			image = book_block.find('div', attrs={'class': 'image_container'}).find('img')
			rating = book_block.find('p', attrs={'class': 'star-rating'})
			if(len(rating['class']) == 2):
				rating = rating['class'][1]

			yield {
				'title': image['alt'], 
				'price': book_block.find('div', attrs={'class': 'product_price'}).find('p', attrs={'class': 'price_color'}).string, 
				'thumbnail_url': urljoin(scraper_url, image['src']), 
				'category_id': category['id'],
				'stock': book_block.find('div', attrs={"class": "product_price"}).find('p', attrs={"class": "instock"}).find('i', attrs={"class": "icon-ok"}) is not None or False,
				'rating': self.ratings[rating]
			}