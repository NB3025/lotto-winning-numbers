import requests
from bs4 import BeautifulSoup


""" 동행복권 사이트에서 로또 당첨번호를 파싱할 수 있는 클래스
def __init__(self):
 - 동행복권사이트를 GET요청하고 응답 상태를 확인. --> 함수를 통해 요청하고
 - 만약 응답코드가 200이라면 self.html에 requests를 통해 받아온 데이터 저장

def get_html(self):


def parsing_html(self):


 - 저장된 데이터가 있으면 bs를 통해 파싱
 - 만약 저장된 데이터가 없다면 최대 5번까지 재 요청 후 파싱 
"""

class Lotto():
    def __init__(self,drwTitle=0):
        
        self.URL = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
        self.html = ''
        self.status_code = 0        

        self.DRWTITLE_HTML_ID = '#dwrNoList > option:nth-child(1)'
        self.DRWNO_HTML_IDS = "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span:nth-child("
        self.drwno_ids = [ self.DRWNO_HTML_IDS+str(i)+")" for i in range(1,7)]
        
        self.drwTitle = self.get_latest_lottoDrwtitle()

        if self.drwTitle >= drwTitle and drwTitle != 0:
            self.drwTitle = drwTitle

        self.dwrNoList = self.drwTitle
        self.post_data = {'drwNo': self.drwTitle, 'dwrNoList': self.drwTitle}

        self.drwtNos = {}

        self.get_html('POST')
        self.parsing_html()


    def get_html(self,method):

        if method == 'GET':
            response = requests.get(self.URL)
        else:
            response = requests.post(self.URL, self.post_data)

        self.status_code = response.status_code
        if self.status_code == 200:
            self.html = response.text
            return True
        else:
            return False
            

    def parsing_html(self):

        soup = BeautifulSoup(self.html, 'html.parser')
        
        arr = []
        for drwno_id in self.drwno_ids:
            num = soup.select_one(drwno_id).get_text()
            arr.append(num)
        
        if len(arr) == 6:
            self.drwtNos[self.drwTitle]=arr
            return True
        else:
            print (f'error {len(self.drwtNos)=}')
            return False



    def get_latest_lottoDrwtitle(self):

        if self.get_html('GET'):

            soup = BeautifulSoup(self.html, 'html.parser')
            drwTitle = soup.select_one(self.DRWTITLE_HTML_ID).get_text()

            return int(drwTitle)
        else:
            print (f'error {self.status_code=}')
            return False


    def get_latest_lottoDrwNum(self, count=1):

        if count < 0:
            print (f'error : count is zero')
            return False     
        self.drwTitle = self.get_latest_lottoDrwtitle()
        for _ in range(count):
            self.get_html('POST')
            self.parsing_html()
            self.drwTitle -=1
            self.post_data = {'drwNo': self.drwTitle, 'dwrNoList': self.drwTitle}
            

    def __repr__(self):
        for key in self.drwtNos.keys():
            print (f'{key}회 당첨번호: {self.drwtNos[key]}')
        return ''


# 최근 회차 당첨번호 조회
mylotto=Lotto()
print (mylotto)

# 특정 회차 당첨번호 조회
mylotto=Lotto(13)
print (mylotto)

# 최근 10개 당첨번호 조회 
mylotto.get_latest_lottoDrwNum(10)
print (mylotto)




