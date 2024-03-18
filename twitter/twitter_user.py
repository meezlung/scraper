from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver, EventFiringWebElement
from selenium.webdriver.common.by import By

from time import sleep

class TwitterUser:
    def __init__(self, link: str) -> None:
        load_dotenv()
        self.USERNAME: str = os.environ['NAME']
        self.PASSWORD: str = os.environ['PASSWORD']

        self.service = Service(executable_path='./geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.driver.maximize_window()

        self.insta_url: str = link
        self.driver.get(self.insta_url)

        self.array = list()
        self.objects: dict[str, str] = {}

    # ---------------- Twitter User Info ----------------

    def press_login_button(self) -> None:
        xpath = "//span[contains(text(), 'Log in')]"
        login_button = self.driver.find_element(By.XPATH, xpath)
        login_button.click()

    def login_username(self) -> None:
        xpath = "//input[@name='text']"
        username = self.driver.find_element(By.XPATH, xpath)
        username.send_keys(self.USERNAME)

    def press_next(self) -> None:
        xpath = "//span[contains(text(), 'Next')]"
        next_button = self.driver.find_element(By.XPATH, xpath)
        next_button.click()

    def login_password(self) -> None:
        xpath = "//input[@name='password']"
        password = self.driver.find_element(By.XPATH, xpath)
        password.send_keys(self.PASSWORD)

    def press_big_login_button(self) -> None:
        xpath = "//div[@data-testid='LoginForm_Login_Button']"
        big_login_button = self.driver.find_element(By.XPATH, xpath)
        big_login_button.click()

    def get_handle_name(self) -> None:
        xpath = "//div[@data-testid='UserName']"
        user_tag = self.driver.find_element(By.XPATH, xpath).text
        
        index = user_tag.find('@')
        name = user_tag[:index-2] 
        username = user_tag[index:]

        self.objects['name'] = name
        self.objects['username'] = username

        print("Name:", name)
        print("Username:", username)

    def get_description(self) -> None:
        xpath = "//div[@data-testid='UserDescription']"
        description = self.driver.find_element(By.XPATH, xpath).text
        self.objects['description'] = description
        
        print("Description:", description)

    def get_tweets(self, number_of_tweets: int) -> list[str]:
        links = []
        wait = WebDriverWait(self.driver, 10)

        xpath = '//article[@data-testid="tweet"]'
        articles = self.driver.find_elements(By.XPATH, xpath)

        counter = 0

        while True:
            for article in articles:
                hrefs = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid=User-Name] a[role=link][href*=status]')))
            
                for href in hrefs:
                    link = href.get_attribute('href')
                    if link not in links and len(links) < number_of_tweets + 1:
                        links.append(link)
                        counter += 1
                        print(f'Link {counter}:', link)

                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 200)', "")
                articles = self.driver.find_elements(By.XPATH, xpath)

                if len(links) == number_of_tweets:
                    break

            if len(links) == number_of_tweets:
                break

        return links

    # ---------------- Tweeter Thread ----------------

    def get_username(self, user_tag: str) -> tuple[str, str]:
        index = user_tag.find('@')
        name = user_tag[:index-2] 
        username = user_tag[index:]
        
        print('--------')
        print(name)
        print(username)

        return name, username
    
    def get_info_per_link(self, link: str, number_of_replies_from_each_thread: int, link_counter: int) -> dict[tuple[str, str], tuple[str | None, str | None, str | None]]:
        self.driver.get(link)
        wait = WebDriverWait(self.driver, 10)

        users: dict[tuple[str, str], tuple[str | None, str | None, str | None]] = dict()

        sleep(5)

        xpath = '//article[@data-testid="tweet"]'
        tweets = self.driver.find_elements(By.XPATH, xpath)
        
        counter = 0

        while True:
            for tweet in tweets:
                print()
                print('--------------------')
                print('Counter: ', counter)
                print(tweet)
                print()
                print(f'Link: {link_counter}', link)
                print('--------------------')
                print()
                print('Finding username.')
                # user_tag = tweet.find_element(By.XPATH, "//div[@data-testid='User-Name']").text
                # name, username = self.get_username(user_tag)

                name = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1awozwy r-6koalj r-1udh08x r-3s2u2q'][style='text-overflow: unset; color: rgb(231, 233, 234);'] span[class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                username = tweet.find_element(By.CSS_SELECTOR, "[data-testid='User-Name'] div[class='css-1rynq56 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-18u37iz r-1wvb978'][style='text-overflow: unset; color: rgb(113, 118, 123);'] span[class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']").text
                print(name, username)


                sleep(1)

                tweetText = None
                tweetPhoto = None
                tweetVideo = None

                try:
                    print()
                    print('Finding text.')
                    tweetText = tweet.find_element(By.CSS_SELECTOR, "[data-testid='tweetText'] span[style='text-overflow: unset;']").text
                    print(f'Text found: {tweetText}')
                    sleep(1)
                except:
                    tweetText = None
                    print('No text found.')

                try:
                    print()
                    print('Finding tweet photo.')
                    tweetPhotoPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid='tweetPhoto'] img[alt='Image'][draggable='true']")
                    tweetPhoto = tweetPhotoPath.get_attribute('src')
                    print(f'Tweet photo found: {tweetPhoto}')
                    sleep(1)
                except:
                    tweetPhoto = None
                    print('No photo found.')

                try:
                    print()
                    print('Finding tweet video.')
                    tweetVideoPath = tweet.find_element(By.CSS_SELECTOR, "[data-testid='videoComponent'] source[type='video/mp4']")
                    tweetVideo = tweetVideoPath.get_attribute('src')
                    print(f'Tweet video found: {tweetVideo}')
                    sleep(1)
                    
                except:
                    tweetVideo = None
                    print('No video found.')

                if (name, username) not in users.keys(): 
                    users[(name, username)] = (tweetText, tweetPhoto, tweetVideo)
                    print()
                    print(users)
                    print()

                    counter += 1

                sleep(1)
                self.driver.execute_script('window.scrollBy(0, 200)', "")
                tweets = self.driver.find_elements(By.XPATH, xpath)

                if number_of_replies_from_each_thread == counter:
                    break

            if number_of_replies_from_each_thread == counter:
                break
            

        print(users)
        sleep(1)

        return users