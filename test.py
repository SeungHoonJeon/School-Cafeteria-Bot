from urllib import response
from flask import Flask, json, request, jsonify
import sys
from queue import Empty
import requests,re
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

url = 'https://tu.ac.kr/dormitory/index.do'

response = requests.get(url, verify=False)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        alert = soup.select("li.item")
    except:
        print('식단 업데이트가 되지 않는 날입니다.')
    string = ''
    for i in alert:
        string += i.get_text()
    print(string.strip())
else:
    print('학교 홈페이지 문제 발생')