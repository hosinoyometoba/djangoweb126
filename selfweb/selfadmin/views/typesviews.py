from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Users

def list(request):
    return render(request,'selfadmin/public/base2.html')