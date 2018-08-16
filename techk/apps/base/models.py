from django.db import models

class Category(models.Model):
	"""
	This class modelates a book category
	"""
	name = models.CharField(max_length=255) # The name of the category
	active = models.BooleanField(default=True) # A boolean indicating if the category is active

	def delete(self):
		self.active = False
		self.save()

class Book(models.Model):
	"""
	This class modelates a book
	"""
	title = models.CharField(max_length=255) # The title of the book
	price = models.CharField(max_length=10) # The price of the book without taxes
	tax = models.CharField(max_length=10) # The tax this book is affected
	thumbnail_url = models.CharField(max_length=255) # An URL directing to an image of the book
	added_date = models.DateTimeField(auto_now_add=True) # The datetime where the book was found for the first time
	updated_date = models.DateTimeField(auto_now=True) # The last datetime which the book information has been updated
	product_description = models.TextField(blank=True) # A synopsis for the book
	active = models.BooleanField(default=True) # A boolean indicating if the book is active
	upc = models.CharField(max_length=16) # The Universal Product Code of the book.
	stock = models.BooleanField(default=False) # The remaining quantity of books
	rating = models.IntegerField(default=0) # The rating given by users for the book
	reviews = models.IntegerField(default=0) # The number of reviews given to this book
	category_id = models.ForeignKey(Category, on_delete = 'restrict') # An identification of the main category for the book

	def delete(self):
		self.active = False
		self.save()
