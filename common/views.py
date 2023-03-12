from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})

import pymysql
def all_mark(request):
    con = pymysql.connect(host='mountain.ct0ysj5bxpal.ap-northeast-2.rds.amazonaws.com',
                        user='admin', password='kg3whghkdlxld!!', db='mydb', charset='utf8')
    cur = con.cursor()

    sql = f'select latitude, longitude from mydb.main_mountain;'
    cur.execute(sql)

    latlng_rows = cur.fetchall()

    sql = f'select name from mydb.main_mountain;'
    cur.execute(sql)

    name_rows = cur.fetchall()

    context = {'mountain_latlng':latlng_rows, 'mountain_name':name_rows}

    # print(rows[0][0])
    # print(type(rows))
    
    return render(request, 'main/whole_map.html', context)