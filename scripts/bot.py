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

def fetch_images(link, driver):
    images = []
    driver.get(link)
    if driver.title == 'Page Not Found • Instagram':
        print('Username does not exist')
        return [],''
    name = driver.current_url.split('/')[-2]
    newpath = '../outputs/{}'.format(name)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while(True):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(DELAY)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        for i in driver.find_elements_by_tag_name('a'):
            if i.get_attribute('href').startswith('https://www.instagram.com/p/'):
                images.append(i.get_attribute('href'))
        images = list(set(images))
    return images, newpath

def process_posts(links, direc, driver):
    all_details = []
    temp = {}
    for link in links:
        details = {}
        driver.get(link)
        details['caption'] = driver.title
        for i in driver.find_elements_by_tag_name('img'):
            try:
                if i.get_attribute('src').startswith('https://instagram') and i.get_attribute('alt').endswith("'s profile picture") == False:
                    details['img_link'] = i.get_attribute('src')
                    details['description'] = i.get_attribute('alt')
                    break
            except:
                pass
        if details != {}:
            all_details.append(details)
    temp['posts'] = all_details
    y = json.dumps(temp, indent=4)
    print(y, file=open(direc+'/meta.txt', 'w'))
    return all_details

def download_pics(details, folder, driver):
    newpath = folder + '/photos'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for i in details:
        if 'img_link' in i.keys():
            filename = newpath + '/' + i['img_link'].split('?')[0].split('/')[-1]
            urlretrieve(i['img_link'], filename)
            
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
    
def download(update, context):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    posts, wd = fetch_images('https://www.instagram.com/{}/'.format(update.message.text.split(' ')[1]), driver)
    if posts != []:
        details = process_posts(posts, wd, driver)
        download_pics(details, wd, driver)
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
    dp.add_handler(CommandHandler("download", download))
    updater.start_polling()
    updater.idle()

main()   
