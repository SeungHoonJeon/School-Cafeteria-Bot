from urllib import response
from flask import Flask, json, request, jsonify
import sys
from queue import Empty
import requests,re
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def kakao_data(information_data):
    data = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : information_data
                        }
                    }
                ]
            }
        }

    return data

def food():
    url = 'https://www.tu.ac.kr/tuhome/diet.do'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            list = soup.select_one("table").find_all(text=True)
        except:
            print('식단 업데이트가 되지 않는 날입니다.')
            return '식단 업데이트가 되지 않는 날입니다.(주말/공휴일)'

        while '\n' in list:
            list.remove('\n')

        title_list = []
        ul = soup.select_one("#cms-content > div > div > div.table-wrap > table > tbody")
        titles = ul.select('tr > th')

        for title in titles:
            title_list.append(title.get_text())

        for i in range(len(list)):
            list[i] = re.sub(':크림스프/야채샐러드/피클 김치', '', list[i])
            list[i] = re.sub('\r', ' ', list[i])
            for title in title_list:
                if(list[i] == title):
                    list[i] = '\n\n['+title+']'

        list[0] = re.sub('\n\n', '', list[0])

        str1 = ''
        for menu in list:
            str1 += menu +'\n'
        print(str1.strip())
        return str1.strip()

    else : 
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

def dorm_food():
    url = 'https://tu.ac.kr/dormitory/index.do'

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            alert = soup.select("li.item")
        except:
            print('식단 업데이트가 되지 않는 날입니다.')
            return '식단 업데이트가 되지 않는 날입니다.'

        string = ''
        for i in alert:
            string += i.get_text()

        return string.strip()

    else:
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

def notice():
    url = "https://www.tu.ac.kr/tuhome/sub07_01_01.do"
    response = requests.get(url, verify=False)
    

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        try:
            notices = soup.find_all("td", attrs={"class":"subject"})
        except:
            print('등록 페이지에 글이 없습니다.')
            return '등록 페이지에 글이 없습니다.'
    
        i = 1
        str1 = '[학교공지]\n\n'
        for notice in notices:
            title = notice.get_text().strip()
            link = notice.find("a")["href"]
            str1 += "["+str(i)+"] "+title+'\n'
            str1 += url+link+'\n\n'
            i = i+1
        
        print(str1.strip())
        return str1.strip()
    else:
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

def tu_cal():
    url = "https://www.tu.ac.kr/tuhome/scheduleTable.do"
    response = requests.get(url, verify=False)
    

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        try:
            notices = soup.find_all("tr", attrs={"class":"notice"})
        except:
            print('등록 페이지에 글이 없습니다.')
            return '등록 페이지에 글이 없습니다.'
    
        #print(notices)

        str1='학시일정 \n'
        for notice in notices:
            try:
                month = '\n'+'['+notice.find('th').get_text().strip()+'] \n'
                str1+=month
            except:
                pass
            finally:
                event = notice.select('td')[0].get_text()+' - '+notice.select('td')[1].get_text()+'\n'
                str1+=event

        print(str1.strip())
        return str1.strip()
    else:
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'
    
def cup_food():
    f = open("./menu/Cup_Rice.txt","r")
    menu = f.read()
    f.close()
    return menu

def china_food():
    f = open("./menu/Beijing_Story.txt","r")
    menu = f.read()
    f.close()
    return menu

def foursome_food(): 
    f = open("./menu/Four_Some.txt","r")
    menu = f.read()
    f.close()
    return menu

def meogbang_food():
    f = open("./menu/Mugbang_Lounge.txt","r")
    menu = f.read()
    f.close()
    return menu

def Caffeine_food():
    f = open("./menu/Cafe_In.txt","r")
    menu = f.read()
    f.close()
    return menu

def buger_coffee():
    f = open("./menu/Bugger_And_Coffee.txt","r")
    menu = f.read()
    f.close()
    return menu

def cafe_dream():
    f = open("./menu/Cafe_Dream.txt","r")
    menu = f.read()
    f.close()
    return menu

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content=content.replace("\n","")
    
    print(content)

    if content == "오늘의 학식":
        dataSend = kakao_data(food())
    elif content == "경대컵밥": #완
        dataSend = kakao_data(cup_food())
    elif content == "베이징스토리": #완
        dataSend = kakao_data(china_food())
    elif content == "포썸": #완
        dataSend = kakao_data(foursome_food())
    elif content == "먹방 라운지": #완
        dataSend = kakao_data(meogbang_food())
    elif content == "Cafe In": #완
        dataSend = kakao_data(Caffeine_food())
    elif content == "버거&커피": #완
        dataSend = kakao_data(buger_coffee())
    elif content == "Cafe Dream": #완
        dataSend = kakao_data(cafe_dream())
    elif content == "오늘의 기숙사 식단":
        dataSend == kakao_data(dorm_food())
    elif content == "학교공지":
        dataSend = kakao_data(notice())
    elif content == "학사일정":
        dataSend = kakao_data(tu_cal())
    else:
        dataSend = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : '없는 키워드 입니다.'
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)