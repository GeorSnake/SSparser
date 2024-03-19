from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .scrapers import get_source_html

def start_parsing(request):
    url = "https://home.ss.ge/ru/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/l/%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0/%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F?cityIdList=96&subdistrictIds=57%2C58%2C59%2C60%2C61%2C62%2C63%2C64%2C65%2C66%2C90&currencyId=1&page=1"
    get_source_html(url)
    return HttpResponse("Parsing completed successfully!")