from numpy import mat
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


import os
import datetime
import time
import pickle

""" 동행복권 사이트에서 로또 당첨번호를 파싱할 수 있는 클래스
def __init__(self):
 - 동행복권사이트를 GET요청하고 응답 상태를 확인. --> 함수를 통해 요청하고
 - 만약 응답코드가 200이라면 self.html에 requests를 통해 받아온 데이터 저장

def get_html(self):


def parsing_html(self):


 - 저장된 데이터가 있으면 bs를 통해 파싱
 - 만약 저장된 데이터가 없다면 최대 5번까지 재 요청 후 파싱 
"""

class Lotto:
    def __init__(self,drwTitle=0):
        
        self.URL = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'

        self.html = ''
        self.status_code = 0        

        self.DRWTITLE_HTML_ID = '#dwrNoList > option:nth-child(1)'
        self.DRWNO_HTML_IDS = "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span:nth-child("
        self.drwno_ids = [ self.DRWNO_HTML_IDS+str(i)+")" for i in range(1,7)]
        
        self.file_name = ''

        # 기본으로 제일 최근회차 가져옴
        self.drwTitle = self.get_latest_lottoDrwtitle()

        # 생성값으로 받은 drwTitle이 제일 최근보다 작은데 0이 아니면
        if self.drwTitle >= drwTitle and drwTitle != 0:
            self.drwTitle = drwTitle

        # self.dwrNoList = self.drwTitle
        self.post_data = {'drwNo': self.drwTitle, 'dwrNoList': self.drwTitle}

        self.drwtNos = {}
        self.get_latest_lottoDrwNum(self.drwTitle)

        # self.get_html('POST')
        # self.parsing_html()


    def get_drwtNos(self):
        return self.drwtNos


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
               
        
    # 특정 회차 호출하기
    # title을 지정하면 해당 회차를 호출
    # title이 0일때  제일 최근회차
    def get_latest_lottoDrwNum(self, title=0):

        if title < 0:
            print (f'error : title is negative -> {title=}')
            return False
        
        elif title != 0:
            self.drwTitle = title
            
        elif title == 0:
            self.drwTitle = self.get_latest_lottoDrwtitle()
        
        self.drwtNos = {}
        
        self.post_data = {'drwNo': self.drwTitle, 'drwNoList': self.drwTitle}
        self.get_html('POST')
        self.parsing_html()        


    # 최근 회차 가져오는 함수
    def get_latest_lottoDrwtitle(self):

        if self.get_html('GET'):

            soup = BeautifulSoup(self.html, 'html.parser')
            drwTitle = soup.select_one(self.DRWTITLE_HTML_ID).get_text()

            return int(drwTitle)
        else:
            print (f'error {self.status_code=}')
            return False


    def get_range_lottoDrwNum(self, start=0, end=0, count=0):

        if start < 0 and end < 0 and count < 0:
            print (f'error : value is negative -> {start=}, {end=}, {count=}')
            return False
        
        # if start*end*count != 0 :
        #     print (f'error : range is wrong -> {start=}, {end=}, {count=}')
        self.drwtNos = {}

        # start, end 없고 count만 있을때
        if start == 0 and end == 0 and count != 0:
            # 최근회차 range 갯수만큼
            end = self.get_latest_lottoDrwtitle()
            end +=1
            start = end - count

        elif start !=0 and end == 0 and count != 0:
            # start부터 count 갯수만큼
            end = start+count

        elif start !=0 and end == 0 and count == 0:
            # start 부터 제일 마지막까지
            end = self.get_latest_lottoDrwtitle()
            end +=1

        elif start !=0 and end !=0 and count == 0:
            # start부터 end까지
            end +=1
        
        elif start==0 and end==0 and count==0:
            print (f'error : all value is zero {start=}, {end=}, {count=}. Use get_latest_lottoDrwNum()')
            return False
      
        
        self.drwtNos = {}

        with open("tmp/data.pickle","rb") as f: # rb : 바이트 형식으로 읽어오기
            _data = pickle.load(f) # (파일)
        
        _data_list = list(_data.keys())
        _range_list = list(range(start,end))

        _tmp_arr=[]
        for r in _range_list:
            if r in _data_list:
                self.drwtNos[r] = _data[r] 
            else:
                _tmp_arr.append(r)

        for i in tqdm(_tmp_arr):
            if i%30==0:
                time.sleep(2)
            self.drwTitle = i
            self.post_data = {'drwNo': self.drwTitle, 'drwNoList': self.drwTitle}
            self.get_html('POST')
            self.parsing_html()

        # cache처럼 사용하기 위해 항상 저장        
        
        # 저장
        with open("tmp/data.pickle","wb") as f: # wb : 바이트 형식으로 쓰기
            pickle.dump(self.drwtNos, f) #(저장하고자 하는 객체, 파일)
        
        # # 호출
        # with open("tmp/data.pickle","rb") as f: # rb : 바이트 형식으로 읽어오기
        #     data = pickle.load(f) # (파일)
            
 

    # TODO return으로 파일경로. 파일명 회차이용해서 만들어야함
    # name을 인수로 받아서 원하는 파일명으로 생성
    # 파일명 중복인 경우 어떻게 출력할까? 날짜/시간붙여서 생성하면 중복처리 안해도됨
    # 근데 파일명을 직접입력받는경우
    def make_csv(self, file_name='lotto-winning-numbers.csv'):
        
        self.file_name = file_name

        if len(self.drwtNos) == 0:
            return False

        df = pd.DataFrame(self.drwtNos)
        df = df.T
        df.columns = ['drwtNo1', 'drwtNo2', 'drwtNo3', 'drwtNo4', 'drwtNo5', 'drwtNo6']
        df.index.name = 'title'
        df = df.sort_index(ascending=False)
        
        file_list = os.listdir(os.getcwd())

        if file_name in file_list:
            now = datetime.datetime.now()
            nowDatetime = now.strftime('%Y%m%d_%H%M%S_')
            self.file_name = nowDatetime+file_name
        
        df.to_csv(self.file_name)

        return True
    
    def update_csv(self, file_name='lotto-winning-numbers.csv'):
        self.file_name = file_name
        
        _file_list = os.listdir(os.getcwd())

        if self.file_name not in _file_list:
            print ('파일 없음')
            self.make_csv(self.file_name)
            return True

        df_1 = pd.read_csv(self.file_name, index_col='title')
        
        _drwtNo_start = list(self.drwtNos.keys())[0]
        _drwtNo_end = list(self.drwtNos.keys())[-1]

        _df_start = int(df_1.index[-1])
        _df_end = int(df_1.index[0])


        # 사용자가 range요청하고 업데이트 요청한경우
        # range가 기존 파일보다 길이가 긴경우.
        # 0. 같은 경우
        # if _drwtNo_start == _df_start and _drwtNo_end == _df_end:
        #     print (f'There is nothing to update.')
        #     return False

        # # 1. range 요청한 것이 1~10 / 파일 내용 4~6
        # elif _drwtNo_start < _df_start and _drwtNo_end > _df_end:
        #     pass

        # # 1. range 요청한 것이 1~10 / 파일 내용 11~12
        # elif _drwtNo_start < _df_start and _drwtNo_end < _df_end:
        #     print (f'There is nothing to update.')
        #     return False
        
        # # 2. range 1~10 / 파일 내용 9~12
        # if _drwtNo_start == _df_start and _drwtNo_end == _df_end:
        #     print (f'There is nothing to update.')
        #     return False

        # # 3. range 1~10 / 파일 내용 12~15
        # if _drwtNo_start == _df_start and _drwtNo_end == _df_end:
        #     print (f'There is nothing to update.')
        #     return False

        # # 4. range 요청한 것이 1~10 / 파일 내용 1~12

        df_2 = pd.DataFrame(self.drwtNos)
        df_2 = df_2.T
        df_2.columns = ['drwtNo1', 'drwtNo2', 'drwtNo3', 'drwtNo4', 'drwtNo5', 'drwtNo6']
        df_2.index.name = 'title'

        # df = pd.concat([df_1,df_2])
        df = df_2.sort_index(ascending=False)

        df.to_csv(self.file_name)
        print (f'Updated.')
        return True


    def __repr__(self):
        for key in self.drwtNos.keys():
            print (f'{key}회 당첨번호: {self.drwtNos[key]}')
        return ''


# 최근 회차 당첨번호 조회
# mylotto=Lotto()
# print (mylotto)

# 특정 회차 당첨번호 조회
# mylotto=Lotto(13)
# print (mylotto)

# 최근 10개 당첨번호 조회 
# mylotto.get_range_lottoDrwNum(count=200)

# mylotto.get_range_lottoDrwNum(start=900, count=10)
# print (mylotto)

# mylotto.get_range_lottoDrwNum(start=980)
# print (mylotto)

# mylotto.get_range_lottoDrwNum(start=900, end=910)
# print (mylotto)

# mylotto.get_range_lottoDrwNum(start=900, end=910)

# mylotto.make_csv()
# mylotto.update_csv()
