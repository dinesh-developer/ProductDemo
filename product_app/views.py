from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import *
from .serializers import *
from utils.utils_functions import validate_headers


class Home(View):
	def get(self, request, *args, **kwargs):
		context = {}
		products = Product.objects.values('id','brand__name', 'discount', 'name', 'price', 'color', 'rating').order_by('-updated_at')
		if 'search' in request.GET and request.GET['search'] != 'all':
			products = products.filter(Q(name__istartswith=request.GET['search'])|Q(brand__name__istartswith=request.GET['search'])|Q(color__istartswith=request.GET['search']))
		if not products.exists():
			products = []
		context['products'] = products
		context['colors'] = COLOR_CHOICES
		context['brands'] = Brand.objects.values_list('name', flat=True)
		return render(request, 'home.html', context)


class AddProductAPIView(APIView):
	'''
	Api for add product, default creation of new brand
	'''
	serializer_class = ProductAddSerializer
	permission_classes = [AllowAny]
	
	def post(self, request, *args, **kwargs):
		platform, app_version, device_id = validate_headers(request)
		data = request.data
		serializer = ProductAddSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			brand_obj = Brand.objects.filter(name=data['brand'])
			if brand_obj.exists():
				brand = brand_obj[0]
			else:
				brand = Brand.objects.create(name=data['brand'])
			data['brand'] = brand
			Product.objects.create(**data)
			response = {'status':status.HTTP_201_CREATED, 'message':'Successfuly added', 'success':True, 'data':{}}
		return Response(response)


class ProductListingAPIView(APIView):
	'''
	List & filter api
	'''
	permission_classes = [AllowAny]
	throttle_classes = [AnonRateThrottle]
	
	def get(self, request, *args, **kwargs):
		platform, app_version, device_id = validate_headers(request)
		products = Product.objects.values('id','brand__name', 'discount', 'name', 'price', 'color', 'rating').order_by('-updated_at')
		if not products.exists():
			products = []
		response = {'status':status.HTTP_200_OK, 'message':'All added Products', 'success':True, 'data':products}
		return Response(response)

	def post(self, request, *args, **kwargs):
		platform, app_version, device_id = validate_headers(request)
		data = request.data
		products = Product.objects.values('id','brand__name', 'discount', 'name', 'price', 'color', 'rating').filter(Q(price=data['price'])|Q(color=data['color'])|Q(brand__name=data['brand'])).order_by('-updated_at')
		if not products.exists():
			products = []
		response = {'status':status.HTTP_200_OK, 'message':'Filtered Products', 'success':True, 'data':products}
		return Response(response)