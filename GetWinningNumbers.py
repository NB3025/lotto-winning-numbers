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
    def __init__(self):
        
        self.URL = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
        self.html = ''
        self.status_code = ''
        self.drwtNos = []
        self.title = ''

        self.request_GET()
        self.parsing_html()
    
    def request_GET(self):
        response = requests.get(self.URL)
        if response.status_code == 200:
            self.html = response.text
            self.status_code = response.status_code
            return True
        else:
            return False

    def parsing_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.title = soup.select_one('#lottoDrwNo').get_text()
        for i in range(1,7):
            target_id = '#drwtNo'+str(i)
            num = soup.select_one(target_id).get_text()
            self.drwtNos.append(num)

    def __repr__(self):
        print (f'{self.title}')
        print (','.join(map(str,self.drwtNos)))
        return ''
        
mylotto=Lotto()
# mylotto.request_GET()
# mylotto.parsing_html()
print(mylotto)
# response = requests.get(URL)
# if response.status_code == 200:
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.select_one('#lottoDrwNo')
    
#     drwtNos = []
#     for i in range(1,7):
#         target_id = '#drwtNo'+str(i)
#         num = soup.select_one(target_id).get_text()
#         drwtNos.append(num)

#     print(title.get_text())
#     print (','.join(map(str,drwtNos)))

# else : 
#     print(response.status_code)


URL = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
# 987회차 값을 얻기 위해 각 값에 987을 할당
data = {'drwNo': 987, 'dwrNoList': 987}
res = requests.post(URL, data=data)

soup = BeautifulSoup(res.text, 'html.parser')

arr=[]

# 얻어온 selector값을 이용하여 당첨번호를 획득하고 배열에 저장
for i in range(1,7):
            target_id = "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span:nth-child("+str(i)+")"
            num = soup.select_one(target_id).get_text()
            arr.append(num)
# 당첨번호 출력
print (','.join(map(str,arr)))

