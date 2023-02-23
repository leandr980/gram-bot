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

import dearpygui.dearpygui as dpg
from dearpygui_ext import logger
import time as t


def save_callback():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')

    # 'C:/Users/leandro/Downloads/chromedriver_win32/chromedriver.exe'  # Change this to your own chromedriver path!
    chrome_driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    print('started automation')
    chrome_driver.implicitly_wait(5)
    sleep(1)
    chrome_driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(2)

    username = chrome_driver.find_element('name', 'username')
    username.send_keys(set_username)  # Change this to your own Instagram username
    password = chrome_driver.find_element('name', 'password')
    password.send_keys(set_password)  # Change this to your own Instagram password
    print('login start')
    button_login = chrome_driver.find_element('xpath', '//*[@id="loginForm"]/div/div[3]')
    button_login.click()
    print('login complete')
    sleep(10)

    print('notification button start')
    try:
        chrome_driver.find_element('xpath', '//html//body//div[1]//section//main//div//div//div//div//button').click
        # notnow.click()  # Comment these last 2 lines out, if you don't get a pop up asking about notifications
    except:
        print('yeah')

    sleep(5)
    try:
        chrome_driver.find_element('xpath', '//*[@id="mount_0_0_f5"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
        # notnow.click()  # Comment these last 2 lines out, if you don't get a pop up asking about notifications
    except:
        pass
    hashtag_list = set_hashtags  # Change this to your own tags
    #hashtag_list = ['technology', 'trip', 'photography']  # Change this to your own tags

    prev_user_list = []  # If it's the first time you run it, use this line and comment the two below
    # prev_user_list = pd.read_csv('20190604-224633_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
    # prev_user_list = list(prev_user_list['0'])
    print('notification buttons complete')
    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hashtag in hashtag_list:
        tag += 1
        chrome_driver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
        sleep(randint(5, 7))
        # ActionChains(webdriver).send_keys(Keys.END).perform()

        recent_row = chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]/div[1]/a')
        print(recent_row.get_attribute('href'), hashtag + 'posts start---------------------------------------')
        recent_row.click()

        # first_thumbnail.click()
        sleep(randint(1, 2))
        try:
            for x in range(1, hashtag_split):
                try:
                    username = chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/div/div/div/a').text
                except:
                    print(Exception)
                print(username)
                if username not in prev_user_list:

                    # If we already follow, do not unfollow
                    if chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div').text == 'Follow':
                        print('not following & not in follow list')

                        chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div').click()
                        new_followed.append(username)
                        followed += 1
                        print('added to following list')
                        sleep(randint(15, 25))

                        # Liking the picture
                        button_like = chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button')
                        button_like.click()
                        likes += 1
                        print('like added_current like count this session ', likes)
                        sleep(randint(18, 25))

                        # Comments and tracker
                        comm_prob = randint(1, 10)
                        print('{}_{}: {}'.format(hashtag, x, comm_prob))
                        if comm_prob > 7:
                            comments += 1
                            chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea').click()
                            comment_box = chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/textarea')

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
                    chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button').click()
                    print('next post')
                    sleep(randint(25, 29))
                else:
                    chrome_driver.find_element('xpath', '//div[starts-with(@id,"mount_0_0_")]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button').click()
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


def button_user_pass():
    global set_username
    set_username = dpg.get_value("__input_user")
    print(f"username is {set_username}")

    global set_password
    set_password = dpg.get_value("__input_pass")
    print(f"password is {set_password}")


def button_driver_path():
    global chromedriver_path
    chromedriver_path = dpg.get_value("__input_driver_path")
    print(f"chromedriver path is {chromedriver_path}")


def button_set_hashtags():
    global set_hashtags
    set_hashtags = dpg.get_value("__input_hashtags")
    global hashtag_split
    hashtag_split = set_hashtags.split(",")
    print(f"selected hashtags are {hashtag_split}")


def button_set_follow_limit():
    global set_follow_limit
    set_follow_limit = dpg.get_value("__input_set_follow_limit")
    follow_limit_to_int = int(set_follow_limit)
    if follow_limit_to_int > 300:
        follow_limit_to_int = 300
    hashtag_len = len(hashtag_split)
    follow_limit_per_hashtag = follow_limit_to_int/hashtag_len
    follow_limit_divisable = hashtag_len % follow_limit_to_int == 0
    print(f"total follow limit is {follow_limit_to_int}")
    print(f"number of hashtags is {hashtag_len}")
    print(f"follow limit per hashtag is {follow_limit_per_hashtag}")
    print(f"is the follow limit divisable by total? {follow_limit_divisable}")


dpg.create_context()
dpg.create_viewport()

with dpg.window(tag="Primary Window"):
    # dpg.add_text("Logged in as: Display username here")
    dpg.add_spacer(height=30)

    # Set Login Details
    dpg.add_text("Username:")
    dpg.add_input_text(tag="__input_user")
    dpg.add_text("Password")
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="__input_pass")
        dpg.add_checkbox(label="Show Password")
    dpg.add_button(label="Set Login Details", callback=button_user_pass)

    dpg.add_spacer(height=20)

    # Headless mode
    with dpg.group(horizontal=True):
        dpg.add_checkbox(label="Toggle this checkbox if you want to run in headless mode")

    dpg.add_spacer(height=20)

    dpg.add_text("Path to chromedriver")
    dpg.add_input_text(tag="__input_driver_path")
    dpg.add_button(label="Set Driver Path", callback=button_driver_path)

    dpg.add_spacer(height=20)

    # Add the hashtags you want to use
    with dpg.group(horizontal=True):
        dpg.add_text("Add the hashtags you would like to use")
        dpg.add_text("*separate hashtags with a comma ex [technology,trip,photography,.....]", color=[170, 170, 170])
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="__input_hashtags")
        dpg.add_button(label="Set", callback=button_set_hashtags)

    dpg.add_spacer(height=20)

    # Add the number of people to follow
    with dpg.group(horizontal=True):
        dpg.add_text("Set the number of people to follow")
        dpg.add_text("*the max number to of people you can follow is 300", color=[170, 170, 170])
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="__input_set_follow_limit")
        dpg.add_button(label="Set", callback=button_set_follow_limit)

    dpg.add_spacer(height=20)

    # Min max timer for in between actions
    with dpg.group():
        dpg.add_text("Set the min & max time for in between actions")
        int_source = dpg.add_input_intx(label=f"input int", min_value=0, max_value=100, size=2)

    dpg.add_spacer(height=20)

    with dpg.group():
        dpg.add_checkbox(label="Follow Automatically")
        dpg.add_checkbox(label="Like Automatically")
        dpg.add_checkbox(label="Add Comments")

    dpg.add_spacer(height=20)

    # Start, stop and pause buttons for the script
    with dpg.group(horizontal=True):
        dpg.add_button(label="START", callback=save_callback)
        dpg.add_button(label="STOP")
        dpg.add_button(label="PAUSE")

dpg.create_viewport(title="Program name goes here")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
