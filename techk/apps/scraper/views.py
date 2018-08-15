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

		# For every item in the menu, push it to a response array
		for index, element in enumerate(categories_tag):
			category = element.find('a')
			categories.append({
				'id': index + 1,
				'name': category.string.string.strip(),
				'link': category['href'].replace('index.html', '')
			})
		
		return categories

	def get_books(self):
		"""
		Return a generator for the books
		using the categories
		"""
		categories = self.get_categories()
		for category in categories:
			yield from self._book_generator(category)

	def _book_generator(self, category):
		"""
		Returns a generator of all the books
		of a certain category
		"""
		self.request = requests.get(scraper_url + category['link'])
		self.parser = BeautifulSoup(self.request.content, 'html.parser')

		# Get the total number of books in the category
		result_numbers = self.parser.find('form', attrs={'method':'get'}).find_all('strong')
		total = int(result_numbers[0].string)
		if(len(result_numbers) > 1):
			maximum = int(result_numbers[2].string)
			page = ceil(total/maximum)
		else:
			page = 1
		
		# For every page it must return all the books
		for current_page in range(page):
			link = scraper_url + category['link']
			if(page > 1):
				link += 'page-{}.html'.format(current_page + 1)
			else:
				link += 'index.html'

			self.request = requests.get(link)
			self.parser = BeautifulSoup(self.request.content, 'html.parser')

			books_block = self.parser.find_all('article', attrs={'class': 'product_pod'})
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
			image_block = book_block.find('div', attrs={'class': 'image_container'})
			image = image_block.find('img')
			category_url = scraper_url + category['link']
			book_url = urljoin(category_url, image_block.a['href'])

			# Prints the current book being processed
			print(book_url)

			rating = book_block.find('p', attrs={'class': 'star-rating'})
			if(len(rating['class']) == 2):
				rating = rating['class'][1]

			response = self._get_book_details(book_url)
			response.update({
				'title': image['alt'], 
				'price': book_block.find('div', attrs={'class': 'product_price'}).find('p', attrs={'class': 'price_color'}).string, 
				'thumbnail_url': urljoin(category_url, image['src']), 
				'category_id': category['id'],
				'stock': book_block.find('div', attrs={"class": "product_price"}).find('p', attrs={"class": "instock"}).find('i', attrs={"class": "icon-ok"}) is not None or False,
				'rating': self.ratings[rating]
			})

			yield response

	def _get_book_details(self, link):
		"""
		Returns a dictionary with the specific 
		information about a book
		"""
		self.request = requests.get(link)
		self.parser = BeautifulSoup(self.request.content, 'html.parser')

		product_description = self.parser.find('div', attrs={'id': 'product_description'})
		if product_description is not None:
			product_description = product_description.find_next_sibling('p').string
		table = self.parser.find('table').find_all('tr')

		return {
			'product_description': product_description,
			'upc': table[0].find('td').string,
			'tax': table[4].find('td').string,
			'reviews': int(table[6].find('td').string)
		}
		