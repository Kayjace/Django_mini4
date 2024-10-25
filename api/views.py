from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("홈 페이지입니다.")


# Create your views here.
