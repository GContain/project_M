import os, re, requests, time, base64

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main.models import Mountain

################## 수정 및 적용 부분!

mountainName = input('산 이름 입력: ')

global driver
driver = webdriver.Chrome("C:/projects/chromedriver.exe")

def crawl_info(mountainName) :
    res = requests.get(f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={mountainName}")
    soup = BeautifulSoup(res.text,"html.parser")
    time.sleep(1)
    info = []
    temp_a = soup.select_one(".y4sYp > .SF_Mq")        # 네이버 산정보
    temp_b = soup.select_one(".xHaT3 > .zPfVt")        # 네이버 산 설명글
    if temp_a == None:  # 산이 아닌걸 검색시 메세지 창이 뜸
        pass
    else:
        if temp_b == None:  # 산의 설명글 정보가 없을시
            info.append("등록된 산 정보가 없습니다.")
            # 설명글 추가 버튼 만들면 좋을 거 같음
        else:
            for i in soup.select(".xHaT3 > .zPfVt"):    # 네이버 설명글 저장
                info.append("설명글 : " + i.text)
    return info

def crawl_location(mountainName) :
    # 카카오맵에서 주소 크롤링
    driver.get("https://map.kakao.com/")

    search = driver.find_element(By.CSS_SELECTOR, ".box_searchbar > .query")
    search.send_keys(mountainName, Keys.ENTER) # 산 이름 + 엔터키
    time.sleep(1)

    addr = driver.find_element(By.CSS_SELECTOR, ".addr")
    address = addr.text


    # 위도, 경도 찾는 사이트
    driver.get("https://address.dawul.co.kr/")

    # 주소값 입력
    search = driver.find_element(By.CSS_SELECTOR, "div > #input_juso")
    search.send_keys(address)
    time.sleep(1)

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
    return address, latlng

def crawl_img(mountainName) :
    # google 접속
    driver.get(f"https://www.google.com/search?q={mountainName}")

    # 웹페이지 이동 ('이미지')
    br_me = driver.find_elements(By.CSS_SELECTOR,".hdtb-mitem > a")

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
    soup = BeautifulSoup(driver.page_source,"html.parser")
    br_img = soup.select('.islrc > .isv-r > .wXeWr > div > img')

    for i in br_img:
        if cnt < 6:

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

            if img_type == "data": # data형식은 base64로 처리            
                try:
                    x = img_path.split(",")[1]
                    f = open(f"C:/projects/project_M/static/images/{search}/{cnt}.jpeg","wb")
                    img = base64.b64decode(f"{x}")
                    f.write(img)
                    f.close()
                except:
                    pass

            elif img_type == "https": # https형식은 requests로 처리
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
        return img_url

print(crawl_info(mountainName))
print(crawl_location(mountainName))

mountain = Mountain()
mountain.name = mountainName
address, latlng = crawl_location(mountainName)
mountain.address = address
mountain.latitude = latlng[0]
mountain.longitude = latlng[1]
mountain.info = crawl_info(mountainName)
print(mountain.save())

