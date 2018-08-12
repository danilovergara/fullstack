from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.HyperlinkedModelSerializer):
	"""
	Serializes a Category Model
	"""
	name = serializers.CharField(required=False)
	class Meta:
		model = Category
		fields = (
			'id', 
			'name', 
			'active'
		)
	
	def create(self, validated_data):
		"""
		Create and return a new Category instance, given the validated data.
		"""
		return Category.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing Category instance, given the validated data.
		"""
		instance.name = validated_data.get('name', instance.name)
		instance.active = validated_data.get('active', instance.active) or True
		instance.save()
		return instance


class BookSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Serializes a Book Model
	"""
	category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(active__exact=True))
	class Meta:
		model = Book
		fields = (
			'id', 
			'category_id',
			'title', 
			'thumbnail_url', 
			'price', 
			'stock',
			'product_description',
			'upc',
			'tax',
			'updated_date',
			'rating',
			'reviews',
			'active'
		)
		depth = 1

	def create(self, validated_data):
		"""
		Create and return a new Book instance, given the validated data.
		"""
		return Book.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing Book instance, given the validated data.
		"""
		instance.title = validated_data.get('title', instance.title)
		instance.price = validated_data.get('price', instance.price)
		instance.tax = validated_data.get('tax', instance.tax)
		instance.thumbnail_url = validated_data.get('thumbnail_url', instance.thumbnail_url)
		instance.category_id = validated_data.get('category_id', instance.category_id)
		instance.stock = validated_data.get('stock', instance.stock)
		instance.product_description = validated_data.get('product_description', instance.product_description)
		instance.updated_date = validated_data.get('updated_date', instance.updated_date)
		instance.upc = validated_data.get('upc', instance.upc)
		instance.rating = validated_data.get('rating', instance.rating)
		instance.reviews = validated_data.get('reviews', instance.reviews)
		instance.active = validated_data.get('active', instance.active)
		instance.save()
		return instance