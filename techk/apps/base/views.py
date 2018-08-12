from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from apps.base.models import Category, Book
from apps.base.serializers import CategorySerializer, BookSerializer

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def book_list(request):
	"""
	List all books, or create a new one.
	"""
	if request.method == 'GET':
		books = Book.objects.filter(active__exact=True)
		serializer = BookSerializer(books, many=True)
		return JSONResponse(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = BookSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def book_detail(request, id):
	"""
	Return, update or delete a book.
	"""
	try:
		book = Book.objects.get(pk=id, active__exact=True)
	except Book.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = BookSerializer(book)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = BookSerializer(book, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		book.delete()
		return HttpResponse(status=204)

@csrf_exempt
def category_list(request):
	"""
	List all categories, or create a new one.
	"""
	if request.method == 'GET':
		categories = Category.objects.filter(active__exact=True)
		serializer = CategorySerializer(categories, many=True)
		return JSONResponse(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CategorySerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def category_detail(request, id):
	"""
	Returns, update or delete a book.
	"""
	try:
		category = Category.objects.get(pk=id, active__exact=True)
	except Category.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CategorySerializer(category)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CategorySerializer(category, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		category.delete()
		return HttpResponse(status=204)

def index(request):
    return HttpResponse()