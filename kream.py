from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip

import requests

def kream_login():
    
    driver = webdriver.Chrome('chromedriver.exe') 
    ##사용할 변수 선언 #네이버 로그인 주소 
    url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com' 
    # url = 'https://kream.co.kr/login'
    
    driver.get(url)
    time.sleep(2) #로딩 대기 #아이디 입력폼 
    
    tag_id = driver.find_element_by_name('id') 
    #패스워드 입력폼 
    tag_pw = driver.find_element_by_name('pw') 
    
    # id 입력 # 입력폼 클릭 -> paperclip에 선언한 uid 내용 복사 -> 붙여넣기 
    tag_id.click()
    pyperclip.copy(uid)
    tag_id.send_keys(Keys.CONTROL, 'v') 
    time.sleep(1) 
    # pw 입력 # 입력폼 클릭 -> paperclip에 선언한 upw 내용 복사 -> 붙여넣기 
    tag_pw.click()
    pyperclip.copy(upw)
    tag_pw.send_keys(Keys.CONTROL, 'v') 
    time.sleep(1) #로그인 버튼 클릭
    
    login_btn = driver.find_element_by_id('log.login') 
    login_btn.click() 
    time.sleep(2) #로그인이 실패했을 경우 - 예: 아이디나 패스워드 불일치 
    try: #로그인 실패창 
        login_error = driver.find_element_by_css_selector('#err_common > div > p') 
        print('로그인 실패 > ', login_error.text)
    except: print('로그인 성공')
    
    driver.find_element_by_xpath('//*[@id="new.save"]').click()
    time.sleep(10)
    
    # url = 'https://kream.co.kr/login'
    # driver.get(url)
    # time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[4]/button[1]').click()

    

# kream_login()
driver = webdriver.Chrome('chromedriver.exe') 
    ##사용할 변수 선언 #네이버 로그인 주소 
url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com' 
# url = 'https://kream.co.kr/login'
uid = ''
upw = '' #네이버 로그인 페이지로 이동 
driver.get(url)
time.sleep(2) #로딩 대기 #아이디 입력폼 

tag_id = driver.find_element_by_name('id') 
#패스워드 입력폼 
tag_pw = driver.find_element_by_name('pw') 

# id 입력 # 입력폼 클릭 -> paperclip에 선언한 uid 내용 복사 -> 붙여넣기 
tag_id.click()
pyperclip.copy(uid)
tag_id.send_keys(Keys.CONTROL, 'v') 
time.sleep(1) 
# pw 입력 # 입력폼 클릭 -> paperclip에 선언한 upw 내용 복사 -> 붙여넣기 
tag_pw.click()
pyperclip.copy(upw)
tag_pw.send_keys(Keys.CONTROL, 'v') 
time.sleep(1) #로그인 버튼 클릭

login_btn = driver.find_element_by_id('log.login') 
login_btn.click() 
time.sleep(2) #로그인이 실패했을 경우 - 예: 아이디나 패스워드 불일치 
try: #로그인 실패창 
    login_error = driver.find_element_by_css_selector('#err_common > div > p') 
    print('로그인 실패 > ', login_error.text)
except: print('로그인 성공')

driver.find_element_by_xpath('//*[@id="new.save"]').click()


url = 'https://kream.co.kr/login'

driver.get(url)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[4]/button[1]').click()
time.sleep(3)

url = 'https://kream.co.kr/search?tag_id[brand]=27&sort=popular&per_page=40'
driver.get(url)
time.sleep(1)

import requests
res = requests.get(url)
print (res)


# def clipboard_input(user_xpath, user_input):
#         temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

#         pyperclip.copy(user_input)
#         driver.find_element_by_xpath(user_xpath).click()
#         ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

#         pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
#         time.sleep(1)
        
# url = 'https://kream.co.kr/login'

# driver = webdriver.Chrome('chromedriver.exe')
# time.sleep(1)
# driver.get(url)
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[4]/button[1]').click()

# iframes = driver.find_elements('iframe')
# for iframe in iframes:
#     print('------------------')
#     print(iframe.get_attribute('name'))

# login = {
# }
# time.sleep(0.5)

# temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

# pyperclip.copy(login.get("id"))
# driver.find_element_by_xpath('//*[@id="id"]').click()
# ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

# pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
# time.sleep(1)

# # clipboard_input('//*[@id="id"]', login.get("id"))

# temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

# pyperclip.copy(login.get("pw"))
# driver.find_element_by_xpath('//*[@id="pw"]').click()
# ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

# pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
# time.sleep(1)
# # clipboard_input('//*[@id="pw"]', login.get("pw"))
# # time.sleep(0.5)
# driver.find_element_by_xpath('//*[@id="log.login"]').click()
