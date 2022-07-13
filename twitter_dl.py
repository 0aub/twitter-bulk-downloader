from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from zipfile import ZipFile
import argparse
import time
import os


# cli arguments
parser = argparse.ArgumentParser()
parser.add_argument('-url', '--url', help='target account url', type=str, required=True)
parser.add_argument("-u",'--username', help='your username', type=str, required=True)
parser.add_argument("-p",'--password', help='your password', type=str, required=True)
parser.add_argument("-m","--media", help="download media (default: False)", default=False, action="store_true")
parser.add_argument("-l","--likes", help="download likes (default: False)", default=False, action="store_true")
args = parser.parse_args()

# public variables
TARGET_URL =  args.url
USERNAME =  args.username
PASSWORD =  args.password
MEDIA = args.media
LIKES = args.likes

# chrome driver sittings
def extensions():
    # Add your Chrome Extensions
    options = webdriver.ChromeOptions()
    options.add_extension(r'extensions\TMD.crx')
    prefs = {'download.default_directory': os.path.join(os.getcwd(), 'Downloads', TARGET_URL.split('/')[-1].replace('_', '-'))}
    options.add_experimental_option('prefs', prefs)
    return options

# create a chrome driver
def chrome_launch():
    # Run Chrome Driver
    driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=extensions())
    return driver

# refresh to the target page
def target_page(driver):
    # user page
    driver.get(TARGET_URL)
    time.sleep(10)

# prepare of account page
def twitter_launch(driver):
    # Main page
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(10)
    # login
    username_textbox = driver.find_element("xpath", '//input[@autocomplete="username"]')
    username_textbox.send_keys(USERNAME)
    username_textbox.send_keys(Keys.ENTER)
    time.sleep(2)
    password_textbox = driver.find_element("xpath", '//input[@name="password"]')
    password_textbox.send_keys(PASSWORD)
    password_textbox.send_keys(Keys.ENTER)
    time.sleep(4)

    if 'Confirmation code' in driver.page_source:
        code = input('Confirmation code: ')
        code_textbox = driver.find_element("xpath", '//input[@autocomplete="none"]')
        code_textbox.send_keys(code.strip())
        code_textbox.send_keys(Keys.ENTER)

    inform('Complete logging in ', emoji='◔◡◔')

# create the important directories
def directories():
    # create user folder
    if not os.path.exists('Downloads'):
        os.mkdir('Downloads')
        os.mkdir('Downloads\\' + TARGET_URL.split('/')[-1])
    else:
        if not os.path.exists('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-')):
            os.mkdir('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-'))
    if MEDIA:
        if not os.path.exists('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-') + '\\media'):
            os.mkdir('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-') + '\\media')
    if LIKES:
        if not os.path.exists('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-') + '\\likes'):
            os.mkdir('Downloads\\' + TARGET_URL.split('/')[-1].replace('_', '-') + '\\likes')

    inform('The directories are ready ', emoji='(👍≖‿‿≖)👍')

# extract zip file in a directory
def extraction(directory):
    download_path = os.path.join(os.getcwd(), 'Downloads', TARGET_URL.split('/')[-1].replace('_', '-'))
    for file in os.listdir(download_path):
        if file.endswith('.zip'):
            file_path = os.path.join(download_path, file)
            with ZipFile(file_path) as zip_file:
                zip_file.extractall(os.path.join(download_path, directory))
            os.remove(file_path)

# setup limit
def set_limit(driver, size):
    limit_textbox = driver.find_element("xpath", '//input[@name="limit"]')
    limit_textbox.send_keys(size)
    
# start gathering
def gather_media(driver):
    # go to target url
    target_page(driver)
    time.sleep(5)
    # download actions
    driver.find_element("xpath", '//a[@data-timeline-type="user"]').click()
    time.sleep(3)
    set_limit(driver, '1000000000')
    time.sleep(1)
    driver.find_element("xpath", '//button[@class="twMediaDownloader_button_start btn"]').click()

    inform('Gathering ' + TARGET_URL.split('/')[-1] + '\'s media ... ', emoji='ύ.ὺ')

    download_path = os.path.join(os.getcwd(), 'Downloads', TARGET_URL.split('/')[-1].replace('_', '-'))
    downloaded = False
    while not downloaded:
        for file in os.listdir(download_path):
            if file.endswith('.zip'):
                time.sleep(5)
                extraction('media')
                downloaded = True
                break
        time.sleep(5)
        print('.', end='')

    inform('Media folder is ready ', emoji='(─‿‿─)')

# start gathering
def gather_likes(driver):
    # go to target url
    target_page(driver)
    time.sleep(5)
    # download actions
    driver.find_element("xpath", '//a[@data-timeline-type="likes"]').click()
    time.sleep(3)
    set_limit(driver, '1000000000')
    time.sleep(1)
    driver.find_element("xpath", '//button[@class="twMediaDownloader_button_start btn"]').click()

    inform('Gathering ' + TARGET_URL.split('/')[-1] + '\'s likes ... ', emoji='ύ.ὺ')

    download_path = os.path.join(os.getcwd(), 'Downloads', TARGET_URL.split('/')[-1].replace('_', '-'))
    downloaded = False
    while not downloaded:
        for file in os.listdir(download_path):
            if file.endswith('.zip'):
                time.sleep(5)
                extraction('likes')
                downloaded = True
                break
        time.sleep(5)
        print('.', end='')

    inform('Likes folder is also ready ', emoji='(¬‿¬)')

# emoji
def cat_emoji():
    return '''

        /\_____/\\
       /  o   o  \\
      ( ==  ^  == )
       )         (
      (           )
     ( (  )   (  ) )
    (__(__)___(__)__)
    
    '''

def monkey_emoji():
    return '''
           .="=.
         _/.-.-.\_     _
        ( ( o o ) )    ))
         |/  "  \|    //
          \\'---'/    //
          /`"""`\\  ((
         / /_,_\ \\  \\
         \_\\_'__/ \  ))
         /`  /`~\  |//
        /   /    \  /
    ,--`,--'\/\    /
     '-- "--'  '--'
             
'''

# nice way to print
def inform(string, emoji='', status=True, ask=False):
    color = '\033[0;96m'
    purpose = '[INFO]'
    if not status:
        color = '\033[0;91m'
    if ask:
        purpose = '[ASK]'
        color = '\033[0;95m'
    print('\n', color, purpose, '\033[0;93m', '--> ', '\033[0;97m', string, '\033[0;91m', emoji)

# main function
def main():
    if MEDIA or LIKES:
        directories()
        driver = chrome_launch()
        twitter_launch(driver)
        if MEDIA:
            gather_media(driver)
        if LIKES:
            gather_likes(driver)
        inform('We are done here ', emoji=cat_emoji())
    else:
        inform('Please run the script properly you monkey ', emoji=monkey_emoji())
    
if __name__ == "__main__":
    main()