from bs4 import BeautifulSoup
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

from time import sleep
import time

# create a new chrome session
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/share/chromedriver")

driver.implicitly_wait(3)
driver.maximize_window()

#로그인
driver.get("https://www.thecamp.or.kr/login/main.do")

login = driver.find_element_by_xpath('/html/body/header/div/div/div/a[3]')
login.click()

login_id = driver.find_element_by_xpath('//*[@id="userId"]')
login_id.send_keys('')

login_pw = driver.find_element_by_xpath('//*[@id="userPwd"]')
login_pw.send_keys('')


login_btn = driver.find_element_by_xpath('//*[@id="emailLoginBtn"]')
login_btn.send_keys(Keys.ENTER)

cafe_check = driver.find_element_by_css_selector('div.btn-main-center > a:nth-child(1)')
cafe_check.click()

sleep(3)

alert_result = driver.switch_to_alert()
alert_result.accept()

check = driver.find_element_by_css_selector('body > header > div > div > ul > li.g1 > a')
check.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
name = soup.select('#divSlide2 > div.swiper-wrapper > div.swiper-slide.swiper-slide-active.swiper-slide-duplicate-next.swiper-slide-duplicate-prev > div > div.flex > div.profile-wrap > div.id > span')
driver.save_screenshot('screen.png')

#편지 쓰기
if not name:
    send = driver.find_element_by_css_selector('#divSlide1 > div.swiper-wrapper > div.swiper-slide.swiper-slide-active.swiper-slide-duplicate-next.swiper-slide-duplicate-prev > div > div.btn-wrap > a.btn-green')
    send.click()

    #보안 뉴스 기사 크롤링
    boan_news_url = urlopen('http://www.boannews.com/media/t_list.asp?mkind=0')
    boan_news_soup = BeautifulSoup(boan_news_url, 'html.parser')
    boan_news_index = boan_news_soup.select('#news_area > div:nth-child(1) > a:nth-child(1)')
    
    for i in range(0, 10):
        send_btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[3]/button')
        send_btn.click()

        #입력
        iframe = driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="cke_1_contents"]/iframe'))
        # driver.switch_to.frame(iframe)
        body = driver.find_element_by_css_selector('body')
        # body.click()

        #기사 index
        index = int(boan_news_index[0]['href'][20:25]) - i

        boan_news_url = urlopen('http://www.boannews.com/media/view.asp?idx='+str(index))
        boan_news_soup = BeautifulSoup(boan_news_url, 'html.parser')

        boan_news_title = boan_news_soup.select('#news_title02')
        boan_news_content = boan_news_soup.select('#news_content')

        #전송되는 편지문
        body.send_keys(boan_news_title[0].text)
        body.send_keys(Keys.ENTER)
        if len(boan_news_content[0].text) < 1490:
            body.send_keys(boan_news_content[0].text)
            print(len(boan_news_content[0].text))
            
            driver.switch_to_default_content()

            #제목
            send_title = driver.find_element_by_xpath('//*[@id="sympathyLetterSubject"]')
            mon_day = time.localtime()
            now = [mon_day.tm_mon, mon_day.tm_mday]
            send_title.send_keys(str(now[0])+'월'+str(now[1])+'일'+' 보안뉴스'+' '+boan_news_title[0].text)
            send_title.send_keys(Keys.TAB)

            save = driver.find_element_by_css_selector('body > div.container > div.container-wrap > section > div.btn-b-area > a:nth-child(3)')
            save.click()

        else : 
            driver.switch_to_default_content()
            cancle = driver.find_element_by_css_selector('body > div.container > div.container-wrap > section > div.btn-b-area > a.gray')
            cancle.click()

        print(boan_news_title)

else :
    if '가입 하기' == name[0].text:
        join = driver.find_element_by_css_selector('#divSlide2 > div.swiper-wrapper > div.swiper-slide.swiper-slide-active.swiper-slide-duplicate-next.swiper-slide-duplicate-prev > div:nth-child(2) > div.btn-wrap > a')
        join.click()
    else :
        print('카페 없음.')
        driver.quit()

# sleep(5)
#driver.save_screenshot('screen.png')

driver.quit()
