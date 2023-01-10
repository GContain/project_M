from django.shortcuts import render, HttpResponse, redirect
from .models import Mountain, Mountain_img
# Create your views here.

def index(request):
    return render(request,'main/index.html')


from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, re, base64, requests
from selenium.webdriver.common.keys import Keys


def getMessage(url, msg) :
    msg = "<script>alert('" + msg + "');"
    msg += "location.href='" + url + "';</script>"
    return msg

@api_view(['GET'])
def search(req):
    crawl = mountain_crawling()
    mountainName = req.GET.get('search_data')
    print(mountainName)

    mountain_img = Mountain_img()
    mountain = Mountain()
    
    mountain.name = req.GET.get('search_data')
    print(mountain.name)
    
    mountain.info = crawl.crawl_info(req)
    address, latlng = crawl.crawl_latlng(mountainName)  # 주소, 위/경도 값 저장
    mountain.address = address
    mountain.latitude = latlng[0]
    mountain.longitude = latlng[1]
    
    for i in range(5) :
        mountain_img.img_url = crawl.crawl_img(mountainName)[i]

    mountain.save()
    mountain_img.save()

    # return Response(crawl.crawl_info(mountainName))
    return redirect('main:index')


class mountain_crawling :
    def crawl_info(req) :
        res = requests.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={req.GET.get('search_data')}")
        soup = BeautifulSoup(res.text,"html.parser")
        time.sleep(1)
        info = []
        temp_a = soup.select_one(".y4sYp > .SF_Mq")        # 네이버 산정보
        temp_b = soup.select_one(".xHaT3 > .zPfVt")        # 네이버 산 설명글
        if temp_a == None:  # 산이 아닌걸 검색시 메세지 창이 뜸
            msg = '정확한 산 이름을 검색해주세요'
            url = ''    
            return HttpResponse(getMessage(url, msg))
        else:
            if temp_b == None:  # 산의 설명글 정보가 없을시
                info.append("등록된 산 정보가 없습니다.")
                # 설명글 추가 버튼 만들면 좋을 거 같음
            else:
                for i in soup.select(".xHaT3 > .zPfVt"):    # 네이버 설명글 저장
                    info.append("설명글 : " + i.text)
        return info

    def crawl_latlng(mountain_name) :
        driver = webdriver.Chrome("C:/projects/chromedriver.exe")

        # 카카오맵에서 주소 크롤링
        driver.get("https://map.kakao.com/")

        search = driver.find_element(By.CSS_SELECTOR, ".box_searchbar > .query")
        search.send_keys(mountain_name, Keys.ENTER) # 산 이름 + 엔터키
        time.sleep(2)

        addr = driver.find_element(By.CSS_SELECTOR, ".addr")
        address = addr.text


        # 위도, 경도 찾는 사이트
        driver.get("https://address.dawul.co.kr/")

        # 주소값 입력
        search = driver.find_element(By.CSS_SELECTOR, "div > #input_juso")
        search.send_keys(address)
        time.sleep(2)

        # 검색버튼 클릭
        btnSearch = driver.find_element(By.CSS_SELECTOR, "#btnSch")
        btnSearch.click()
        time.sleep(1)

        # 위도, 경도 부분만 추출
        bring_location = driver.find_element(By.CSS_SELECTOR, "tr > #insert_data_5").text
        splitComma = bring_location.split(',')
        latlng = [splitComma[0].split(':')[1], splitComma[1].split(':')[1]]
        latlng.reverse()

        print('='*50)
        print('[주소] :', address, '\n[위도, 경도] :', latlng)
        print('='*50)

        return address, latlng   # 튜플 형식으로 값 반환

    def mount_img_download(search) :
        # google 접속
        browser = webdriver.Chrome("C:/projects/chromedriver.exe")
        # browser.get(f"https://www.google.com/search?q={u_input}")
        browser.get(f"https://www.google.com/search?q={search}")


        # 웹페이지 이동 ('이미지')
        br_me = browser.find_elements(By.CSS_SELECTOR,".hdtb-mitem > a")

        for i in br_me:
            # print(i.text) # 리스트 확인용

            if i.text == "이미지":
                i.click()
                break

        # 폴더 생성
        try:
            os.mkdir('C:/projects/project_M/static/images/'+str(search))
        except:
            pass

        #이미지 다운 순번
        cnt = 1;
            
        # 이미지 추출 >> BeautifulSoup사용시 select()의 값 꼭 확인해 볼 것! 
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source,"html.parser")
        br_img = soup.select('.islrc > .isv-r > .wXeWr > div > img')

        # 확인용
        # br_img = soup.select_one('.islrc > .isv-r > .wXeWr > div > img')
        # print(br_img.get('src'))
        # print(br_img.get('data-src'))
        # print(type(br_img.get('src')))
        # print(type(br_img.get('data-src')))
        for i in br_img:
        # print(i) # 리스트 확인용

        # 확인 결과 
        # 방식 : src, data-src 2개 혼용
        # src >> "data"형식, "http"형식 혼용
            if cnt < 6:

        # 구글에서 새로운 형식 도입시 에러가 발생 할 수 있으므로 try:except으로 처리
                try:
                    img_path = i.get('src')
                    
                    if type(img_path) != str:
                        img_path = i.get('data-src')

                    # 이미지 이름 추출 및 정규표현식
                    img_name = i.get('alt')
                    img_name = re.sub('[\/:*?"<>|]',"_",img_name)  
                    img_type = img_path.split(":")[0]

                except:
                    pass

                # 확인용
                # print(img_path)
                # print(img_type)

                # 구글에서 새로운 형식 도입시 에러가 발생 할 수 있으므로 else문 추가
                if img_type == "data": # data형식은 base64로 처리
                    
                    # 같은 파일 생성시 오류 발생 해결을 위해 try:except문 사용
                    try:
                        x = img_path.split(",")[1]
                        f = open(f"C:/projects/project_M/static/images/{search}/{cnt}.jpeg","wb")
                        img = base64.b64decode(f"{x}")
                        f.write(img)
                        f.close()
                    except:
                        pass

                elif img_type == "https": # https형식은 requests로 처리
                    # 확인용
                    # 같은 파일 생성시 오류 발생 해결을 위해 try:except문 사용
                    try:
                        res = requests.get(img_path)
                        f = open(f"C:/projects/project_M/static/images/{search}/{cnt}.jpeg","wb")
                        f.write(res.content)
                        f.close()
                    except:
                        pass

                else:
                    continue
            
            else : break;
            cnt += 1;

            temp_split = f.name.split("/")
            img_url = temp_split[4]+"/"+temp_split[5]+"/"+temp_split[6]
            print(img_url)

        # new_height = browser.execute_script("return document.documentElement.scrollHeight")
        # browser.execute_script(f"window.scrollTo(0,{new_height});")
        
        # # 멈춰!
        # if before_height == new_height:
        #     break
        # before_height = new_height

        # print(before_height) # 확인용
        return img_url