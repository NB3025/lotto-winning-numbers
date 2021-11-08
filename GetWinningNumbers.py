import requests
from bs4 import BeautifulSoup


""" 동행복권 사이트에서 로또 당첨번호를 파싱할 수 있는 클래스
def __init__(self):
 - 동행복권사이트를 GET요청하고 응답 상태를 확인. --> 함수를 통해 요청하고
 - 만약 응답코드가 200이라면 self.html에 requests를 통해 받아온 데이터 저장

def request_GET(self):


def parsing_html(self):


 - 저장된 데이터가 있으면 bs를 통해 파싱
 - 만약 저장된 데이터가 없다면 최대 5번까지 재 요청 후 파싱 
"""

class Lotto():
    def __init__(self,drwNo=0):
        
        self.URL = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
        self.html = ''
        self.status_code = 0        

        self.drwNo = drwNo
        if drwNo == 0:
            self.get_latest_lottoDrwNo()
        self.dwrNoList = drwNo
        self.post_data = {'drwNo': self.drwNo, 'dwrNoList': self.dwrNoList}
        
        self.drwtNos = []


    def get_html_data(self,method,data=None):

        if method == 'GET':
            response = requests.get(self.URL)
        else:
            self.post_data = data
            response = requests.post(self.URL, self.post_data)

        self.status_code = response.status_code
        if self.status_code == 200:
            self.html = response.text
            return True
        else:
            return False
            

    def parsing_html(self):

        soup = BeautifulSoup(self.html, 'html.parser')
        for i in range(1,7):
            target_id = "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span:nth-child("+str(i)+")"
            num = soup.select_one(target_id).get_text()
            self.drwtNos.append(num)
        
        if len(self.drwtNos) == 6:
            return True
        else:
            print (f'error {len(self.drwtNos)=}')
            return False



    def get_latest_lottoDrwNo(self):

        if self.get_html_data('GET'):
            soup = BeautifulSoup(self.html, 'html.parser')

            target_id = '#dwrNoList > option:nth-child(1)'
            self.title = soup.select_one(target_id).get_text()
            
            return True
        else:
            print (f'error {self.status_code=}')
            return False

    def __repr__(self):
        print (f'{self.title}')
        print (','.join(map(str,self.drwtNos)))
        return ''
        
mylotto=Lotto()

print (mylotto)
mylotto.get_html_data('POST')
mylotto.parsing_html()
print (mylotto)