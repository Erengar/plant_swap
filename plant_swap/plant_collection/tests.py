from django.test import TestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class test_front_page(TestCase):
    fixtures = ['final_fix.json']

    
    @classmethod
    def setUpData(cls):
        User.objects.create_user(username='Polo', password='Liteon987')

    def test_front_page_view(self):
        response = self.client.get('/')
        return self.assertTemplateUsed(response, 'front_page.html')
    
    def test_front_page_navbar(self):
        page = self.client.get('/')
        return self.assertContains(page, "navbar")
    
    def test_front_page_login(self):
        page = self.client.get('/')
        return self.assertContains(page, ' href="/accounts/login/"')
    
    def test_front_page_logout(self):
        self.client.login(username='Polo', password='Liteon987')
        page = self.client.get('/')
        return self.assertContains(page, 'href="/accounts/logout/"')

    def test_front_page_like(self):
        self.client.login(username='Polo', password='Liteon987')
        response = self.client.get('/')
        return self.assertContains(response, 'fa-regular fa-heart')
    

class test_front_page_selenium(StaticLiveServerTestCase):
    fixtures = ['final_fix.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = FirefoxOptions()
        options.add_argument("--headless")
        cls.selenium = webdriver.Firefox(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_front_page_like(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        self.selenium.find_element(By.XPATH, '/html/body/nav/div[1]/a[1]').click()
        element = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div/div/div/div[2]/div[2]/div[2]/div[1]/a/i')))
        element.click()
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')))
        heart = self.selenium.find_element(By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')
        return self.assertIn('has-text-danger fa-solid fa-heart', heart.get_attribute('class'))

    def test_my_collection_like(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        element = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/a/i')))
        element.click()
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')))
        heart = self.selenium.find_element(By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')
        return self.assertIn('has-text-danger fa-solid fa-heart', heart.get_attribute('class'))

    def test_plant_detail_like(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/div[2]/div/div[1]/figure/a/img').click()
        element = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/section/div/div/div/div[2]/div/div/section[1]/div[3]/div[1]/a/i')))
        element.click()
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')))
        heart = self.selenium.find_element(By.CLASS_NAME, 'has-text-danger.fa-solid.fa-heart')
        return self.assertIn('has-text-danger fa-solid fa-heart', heart.get_attribute('class'))

    def test_plant_detail_update_delete(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        self.selenium.find_element(By.LINK_TEXT, 'Poppy').click()
        update = self.selenium.find_element(By.CLASS_NAME, 'fa-pen-to-square')
        delete = self.selenium.find_element(By.CLASS_NAME, 'fa-trash-can')
        return self.assertIsNotNone(update) and self.assertIsNotNone(delete)
    
    def test_carousel(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Dandy').click()
        first_images = self.selenium.find_elements(By.CSS_SELECTOR, 'div.carousel_image[hidden="true"]')
        self.selenium.find_element(By.ID, 'right-btn').click()
        second_images = self.selenium.find_elements(By.CSS_SELECTOR, 'div.carousel_image[hidden="true"]')
        return self.assertNotEqual(first_images, second_images)

    #IT DELETES STATIC FILES, WHY???
    def test_delete(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        self.selenium.find_element(By.LINK_TEXT, 'Poppy').click()
        self.selenium.find_element(By.CLASS_NAME, 'fa-trash-can').click()
        self.selenium.find_element(By.CSS_SELECTOR, '.box > .button').click()
        page = self.selenium.find_element(By.CLASS_NAME, 'section')
        return self.assertNotIn(page.get_attribute('innerHTML'), 'Poppy')
    
    #Need to implement update tests and add tests
    #Unfinished
    def test_add_plant(self):
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.LINK_TEXT, 'Login/Signup').click()
        username = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')
        username.send_keys('Polo')
        password.send_keys('Liteon987')
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/form/div[3]/input').click()
        self.selenium.find_element(By.XPATH, '/html/body/section/div/div/div[1]/a/div').click()
        self.selenium.find_element(By.XPATH, '//*[@id="input_tag0"]').send_keys('test.jpg')
        image = self.selenium.find_element(By.CLASS_NAME, '.columns > .image')
        return self.assertIsNotNone(image)