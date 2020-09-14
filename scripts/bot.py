from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import time
import os
from config import *
import json
import sys
import random
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

def login(username, password, driver):
    driver.get('https://www.instagram.com/accounts/login/?hl=en')
    time.sleep(DELAY)
    for i in driver.find_elements_by_tag_name('input'):
        if i.get_attribute('name') == 'username':
            i.send_keys(username)
        elif i.get_attribute('name') == 'password':
            i.send_keys(password + '\n')
            break
    time.sleep(DELAY)
    driver.get('https://www.instagram.com/')
    time.sleep(DELAY)
    for i in driver.find_elements_by_tag_name('button'):
        if i.text == 'Not Now':
            i.click()

def get_posts_hashtag(tag, num, driver):
    posts = []
    driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
    while(len(posts) <= num+9):
        for i in driver.find_elements_by_tag_name('a'):
            if i.get_attribute('href').startswith('https://www.instagram.com/p'):
                posts.append(i.get_attribute('href'))
                posts = list(set(posts))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return posts[9: num+9]

def like(driver):
    for i in driver.find_elements_by_tag_name('svg'):
        if i.get_attribute('aria-label') == 'Like':
            i.click()
            break

def comment(comm, driver):
    for i in driver.find_elements_by_tag_name('textarea'):
        if i.get_attribute('aria-label') == 'Add a comment…':
            i.click()
            i.send_keys(comm + '\n')
            break

def follow_followers(username, num, driver):
    driver.get('https://www.instagram.com/{}/'.format(username))
    for i in driver.find_elements_by_tag_name('a'):
        if '/followers/' in i.get_attribute('href'):
            i.click()
            break
    time.sleep(DELAY)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for i in driver.find_elements_by_tag_name('button'):
        if i.text == 'Follow':
            i.click()
            time.sleep(DELAY)
            num = num - 1
            if num == 0:
                break
def interact(update, context):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    login(INSTA_USERNAME,INSTA_PASSWORD, driver)
    msg = update.message.text
    tag = msg.split(' ')[1]
    total = int(msg.split(' ')[2])
    num_like = int(msg.split(' ')[3])
    num_comm = int(msg.split(' ')[4])
    posts = get_posts_hashtag(tag, total, driver)
    for i in posts:
        driver.get(i)
        time.sleep(DELAY)
        try:
            if(num_like >0):
                like(driver)
                num_like = num_like - 1
            time.sleep(DELAY)
            driver.execute_script("window.scrollTo(0, 300);")
            if(num_comm >0):
                cmnt = random.choice(COMMENTS)
                comment(cmnt, driver)
                num_comm = num_comm - 1
        except:
            pass
        time.sleep(random.randint(3,10))
    driver.close()
    driver.quit()
    
def follow(update, context):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    login(INSTA_USERNAME,INSTA_PASSWORD, driver)
    msg = update.message.text
    username = msg.split(' ')[1]
    num = int(msg.split(' ')[2])
    follow_followers(username, num, driver)
    driver.close()
    driver.quit()

def start(update, context):
    update.message.reply_text("""Hi! Send me a command!""")
    
def main():
    updater = Updater(BOT_ID, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("follow", follow))
    dp.add_handler(CommandHandler("interact", interact))
    updater.start_polling()
    updater.idle()

main()   
