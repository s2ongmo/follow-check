from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

def count():
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # 'notranslate' is the only class of <a> tags provided to each user
    lists = soup.select('a.notranslate')
    list_text = [item.get_text() for item in lists]
    list_text = [text.replace('인증됨', '☑') for text in list_text]
    return list_text


def scroll():
    try:
        # Wait up to 10 seconds for the element to come out
        pop_up_window = WebDriverWait(browser, 10).until(
            # Find the class '_aano'
            # '_aano' is the only class given to a follower or a following list window.
            EC.presence_of_element_located((By.CLASS_NAME, 'xyi19xy')))
        while True:
            # If you substitute the scroll height of the found element into the current scroll height, the scroll will come down
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)

            try:
                # 로딩 스피너 확인
                browser.find_element(By.CLASS_NAME, 'xemfg65')
                continue  # 로딩 스피너가 있으면 계속 스크롤
            except NoSuchElementException:
                # 로딩 스피너가 없으면 루프 탈출
                break
    except TimeoutException:
        print("Failed to load the scrollable popup window.")


def follower():
    time.sleep(2)
    browser.execute_script("document.querySelectorAll('._alvs')[0].click();")
    time.sleep(2)
    scroll()
    follower_text = count()
    print("팔로워 수: " + str(len(follower_text)))
    return follower_text

def following():
    time.sleep(2)
    browser.execute_script("document.querySelectorAll('._alvs')[1].click();")
    time.sleep(2)
    scroll()
    following_text = count()
    print("팔로잉 수: " + str(len(following_text)))
    return following_text

def run_script():
    try:
        follower_text = follower()
        browser.execute_script("document.querySelector('._abl-').click();")  # close pop-up
        following_text = following()
        browser.execute_script("document.querySelector('._abl-').click();")  # close pop-up

        result = []
        for follow in following_text:
            if follow not in follower_text:
                result.append(follow)

        output_text.delete('1.0', tk.END)
        for name in result:
            output_text.insert(tk.END, name + '\n')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_script():
    thread = Thread(target=run_script)
    thread.start()

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
username = 's2ongmo'
browser = webdriver.Chrome(options=options)
browser.get('https://www.instagram.com/' + username)

app = tk.Tk()
app.title("Instagram Mutual Follow Check")
app.geometry("400x300")
btn_check = tk.Button(app, text="No 맞팔", command=start_script)
btn_check.pack(pady=20)
output_text = scrolledtext.ScrolledText(app, height=10)
output_text.pack(fill=tk.BOTH, expand=True)
app.mainloop()
