from bs4 import BeautifulSoup
import requests
import datetime
from flask import Flask, render_template

# Flask - 파이썬의 데이터를 추출하는 코드들의 일련의 작업을 웹브라우저 상에 나타내도록 해주는 라이브러리의 개념
app = Flask(__name__)

# 국내주식 정보 웹 크롤링
def financialData(page):
    res = requests.get(page)
    soup = BeautifulSoup(res.text, 'html.parser')

    body = soup.find('tbody')
    items = body.find_all('tr', {'onmouseover' : 'mouseOver(this)'})

    data = []
    for item in items:
        information = item.text
        info = information.split('\n')
        data.append([info[1], info[2], info[3], info[11].strip(),
                     info[14], info[15], info[16], info[17], info[18]])
    return data

financeKOSPIAddress = 'https://finance.naver.com/sise/sise_market_sum.naver?page='
financeKOSDAQAddress = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page='

# 국내주식 정보 웹 크롤링 - 코스피(상장되어 있는 코스피 회사 수 만큼(페이지))
financial_data_kospi = []
for i in range(1, 42) :
    financial_data_kospi += financialData(financeKOSPIAddress + str(i))

# 국내주식 정보 웹 크롤링 - 코스닥(상장되어 있는 코스닥 회수 수 만큼(페이지))
financial_data_kosdaq = []
for i in range(1, 34) :
    financial_data_kosdaq += financialData(financeKOSDAQAddress + str(i))

# 시간 정보를 나타내는 함수
# 네이버 날씨정보 웹 르롤링
def get_now_date_string():
    now = datetime.datetime.now()
    return now.strftime('%Y년 %m월 %d일 %H시 %M분')

html = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%B6%80%EC%82%B0+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=ia9%2Fqlprvh8sshu%2BeVZssssstlK-186606')
soup = BeautifulSoup(html.text, 'html.parser')

address = soup.find('div', {'class' : 'title_area _area_panel'}).find('h2', {'class' : 'title'}).text

temperature = soup.find('div', {'class': 'temperature_text'}).text.strip()[5:]

weatherStatus = soup.find('span', {'class': 'weather before_slash'}).text

air = soup.find('ul', {'class': 'today_chart_list'}).text.strip()

# 가상 서버 방식으로 구현 - 해당 서브 라우터 링크 설정
@app.route('/')
def router():
    now_date_str = get_now_date_string()
    return render_template('test.html', financial_data_kospi=financial_data_kospi, financial_data_kosdaq=financial_data_kosdaq, now_date=now_date_str, address=address, temperature=temperature, weatherStatus=weatherStatus, air=air)

@app.route('/kospi')
def kospi():
    data = ""
    for row in financial_data_kospi:
        data += "<tr>"
        for item in row:
            data += f"<td>{item}</td>"
        data += "</tr>"
    return data

@app.route('/kosdaq')
def kosdaq():
    data = ""
    for row in financial_data_kosdaq:
        data += "<tr>"
        for item in row:
            data += f"<td>{item}</td>"
        data += "</tr>"
    return data

if __name__ == '__main__':
    app.run()
