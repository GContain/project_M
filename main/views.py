from django.shortcuts import render, redirect, get_object_or_404
from .models import Mountain, Mountain_img

import os.path

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def search(request):
    data = request.GET.get('search'); #print(data) # 확인용
    file = "C:/projects/mountain_crawling/search_data.txt"

    if os.path.isfile(file):
        f = open(file,'a',encoding='utf8')
        f.write(f"{data}\n")
        f.close()

    else:
        f = open(file,'w',encoding='utf8')
        f.write(f"{data}\n")
        f.close()

    m = get_object_or_404(Mountain, pk=data); #print(m,type(m)) # 확인용

    context = {'mountain':m}
    return render(request,'main/search.html',context)
