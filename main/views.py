from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from .models import Mountain, Mountain_img

import os.path

# Create your views here.

def index(request):
    return render(request,'main/index.html')

@api_view(['GET'])
def search(req):
    data = req.GET.get('search_data'); # print(data) # 확인용
    file = "C:/projects/project_M/crawling/search_data.txt"
    
    if os.path.isfile(file):
        f = open(file,'a',encoding='utf8')
        f.write(f"{data}\n")
        f.close()

    else:
        f = open(file,'w',encoding='utf8')
        f.write(f"{data}\n")
        f.close()

    return redirect('index')
