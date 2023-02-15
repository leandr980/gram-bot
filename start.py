# ┌────────────────────────────────────────────────────────────────────────┐
# │ InstaBot - Python Selenium Bot                                         │
# ├────────────────────────────────────────────────────────────────────────┤
# │ Copyright © 2019 Joseph Pereniguez                                     |
# | (https://github.com/Estayparadox/InstaBot)                             │
# ├────────────────────────────────────────────────────────────────────────┤
# │ Licensed under the MIT                                                 |
# | (https://github.com/Estayparadox/InstaBot/blob/master/LICENSE) license.│
# └────────────────────────────────────────────────────────────────────────┘


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')

chromedriver_path ='your_path_to_your_chrome_driver' # Change this to your own chromedriver path!

webdriver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
webdriver.implicitly_wait(5)
sleep(1)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(2)

username = webdriver.find_element('name', 'username')
username.send_keys('your_username') # Change this to your own Instagram username
password = webdriver.find_element('name', 'password')
password.send_keys('your_password') # Change this to your own Instagram password

print('login start')
button_login = webdriver.find_element('xpath', '//*[@id="loginForm"]/div/div[3]')
button_login.click()
print('login complete')
sleep(10)

print('notification button start')
try:
    notnow = webdriver.find_element('xpath', '//html//body//div[1]//section//main//div//div//div//div//button')
    notnow.click()  # Comment these last 2 lines out, if you don't get a pop up asking about notifications
except:
    print('yeah')

sleep(5)
try:
    notnow = webdriver.find_element('xpath', '//*[@id="mount_0_0_f5"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
    notnow.click() # Comment these last 2 lines out, if you don't get a pop up asking about notifications
except :
    pass
hashtag_list = ['technology', 'trip', 'photography'] # Change this to your own tags

prev_user_list = [] # If it's the first time you run it, use this line and comment the two below
# prev_user_list = pd.read_csv('20190604-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
# prev_user_list = list(prev_user_list['0'])
print('notifaction buttons complete')
new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(randint(5, 7))
    # ActionChains(webdriver).send_keys(Keys.END).perform()

    recent_row = webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]/div[1]/a')
    print(recent_row.get_attribute('href'), hashtag + 'posts start---------------------------------------')
    recent_row.click()

    # first_thumbnail.click()
    sleep(randint(1, 2))
    try:
        for x in range(1, 5):
            #print('post ', x, ' start')
            #sleep(randint(5, 9))
            try:
                username = webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div/div/div/a').text
            except:
                print(Exception)
            print(username)
            if username not in prev_user_list:

                # If we already follow, do not unfollow
                if webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div').text == 'Follow':
                    print('not following & not in follow list')

                    webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div').click()
                    new_followed.append(username)
                    followed += 1
                    print('added to following list')
                    sleep(randint(15, 25))

                    # Liking the picture
                    button_like = webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button')
                    button_like.click()
                    likes += 1
                    print('like added_current like count this session ', likes)
                    sleep(randint(18, 25))

                    # Comments and tracker
                    comm_prob = randint(1, 10)
                    print('{}_{}: {}'.format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea').click()
                        comment_box = webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea')

                        if comm_prob < 7:
                            comment_box.send_keys('Really cool!, please follow me back')
                            sleep(2)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys('Nice work :), could you kindly follow me back?')
                            sleep(2)
                        elif comm_prob == 9:
                            comment_box.send_keys('Nice gallery!! follow me please!')
                            sleep(2)
                        elif comm_prob == 10:
                            comment_box.send_keys('So cool! :), give me a follow back')
                            sleep(2)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        print('comment added')
                        sleep(randint(30, 35))

                # Next picture
                # webdriver.find_element_by_link_text('Next').click()
                webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button').click()
                print('next post')
                sleep(randint(25, 29))
            else:
                webdriver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button').click()
                sleep(randint(20, 26))
    # Some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
        print(x)
        continue

for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
