import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import ElasticDemo
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
    OrderingFilterBackend
)
from .serializers import NewsDocumentSerializer
from .documents import NewsDocument
# Create your views here.
def generate_random_data():
    url = 'https://newsapi.org/v2/everything?q=apple&from=2023-06-23&to=2023-07-23&sortBy=popularity&apiKey=827705eea42e455cba8bf4afafc7da90'
    r = requests.get(url)
    payload = json.loads(r.text)
    count = 1
    print(payload)
    import pdb; pdb.set_trace()
    for data in payload.get('articles'):
        print(count)
        ElasticDemo.objects.create(
            title = data.get('title'),
            content = data.get('description')
        )

def index(request):
    generate_random_data()
    return JsonResponse({'status' : 200})


class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    lookup_field = 'first_name'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
   
    search_fields = (
        'title',
        'content',
    )
    multi_match_search_fields = (
       'title',
        'content',
    )
    filter_fields = {
       'title' : 'title',
        'content' : 'content',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)

