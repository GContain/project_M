from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from .models import Mountain, Mountain_img

# Create your views here.

def index(request):
    return render(request,'main/index.html')

@api_view(['GET'])
def search(req):
    data = req.GET.get('search_data')
    print(data)
    return redirect('index')
