from selenium import webdriver
from news.models import Profile, Article, Category, Comment
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import Select
from django.urls import reverse
import time


class TestLoginPage(StaticLiveServerTestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
    
    def tearDown(self):
        self.browser.close()

    def test_signup(self):
        form_elements = [["username", "Wise1246"], 
        ['first_name', "Muhammad"], ['last_name', "Sumeer"],
        ['email', "amir00505@gmail.com"],
        ['password1', "Khan1234"], ['password2', "Khan1234"] ]
        self.browser.get(self.live_server_url + reverse('signup'))
        
        signupForm = self.browser.find_element_by_class_name("signup_form")
        #fills in sign up form
        for element in form_elements:
            signupForm.find_element_by_name(element[0]).send_keys(element[1])

        """
        signupForm = self.browser.find_element_by_class_name("signup_form")
        signupForm.find_element_by_name("username").send_keys("Wise124")
        signupForm.find_element_by_name("first_name").send_keys("Muhammad")
        signupForm.find_element_by_name("last_name").send_keys("Sumeer")
        signupForm.find_element_by_name("email").send_keys("amir00505@gmail.com")
        signupForm.find_element_by_name("password1").send_keys("Khan1234")
        signupForm.find_element_by_name("password2").send_keys("Khan1234")"""

        dob_elements = [['dob_month', '8'],['dob_day', '3'], ['dob_year','1999']]
        #fills in dob
        for element in dob_elements:

            dob = Select(signupForm.find_element_by_name(element[0]))
            dob.select_by_value(element[1])
        """
        dob_day = Select(signupForm.find_element_by_name("dob_day"))
        dob_day.select_by_value("3")
        dob_year = Select(signupForm.find_element_by_name("dob_year"))
        dob_year.select_by_value("1999")"""

        signupForm.find_element_by_class_name("sign_up").click()

        time.sleep(2)

        username = self.browser.find_element_by_class_name("user_btns").find_element_by_id("profile").text
        #checks if sign up successful
        self.assertEqual(form_elements[0][1], username)


        #logout test starts here

        #self.browser.find_element_by_class_name("user_btns").find_element_by_id("logout").click()

        #login test starts here
    def test_login(self):
        self.browser.get(self.live_server_url+reverse('login'))
        loginForm = self.browser.find_element_by_class_name("login_form")
        loginForm.find_element_by_name("username").send_keys("Wise124")
        loginForm.find_element_by_name("password").send_keys("Khan1234")
        loginForm.find_element_by_class_name("login").click()
        

        username = self.browser.find_element_by_class_name("user_btns").find_element_by_id("profile").text
        #checks if login is successfull
        self.assertEqual("Wise124", username)
        

        
    def test_like(self):

        self.browser.get(self.live_server_url+reverse('login'))
        loginForm = self.browser.find_element_by_class_name("login_form")
        loginForm.find_element_by_name("username").send_keys("Wise124")
        loginForm.find_element_by_name("password").send_keys("Khan1234")
        loginForm.find_element_by_class_name("login").click()
        

        username = self.browser.find_element_by_class_name("user_btns").find_element_by_id("profile").text
        #checks if login is successfull
        self.assertEqual("Wise124", username)


        #like testing starts here
        self.browser.get(self.live_server_url + "/Article/1")
        like_text = self.browser.find_element_by_id("like-section").text
        like_count = int(like_text.split(" ")[0])
        time.sleep(2)
        self.browser.find_element_by_id("like").click()
        time.sleep(2)
        like_count += 1
        like_text = self.browser.find_element_by_id("like-section").text
        final_count = int(like_text.split(" ")[0])
        like = self.browser.find_element_by_css_selector("#dislike").text
        #checks if like is successfull
        self.assertEqual("Dislike", like)
        self.assertEqual(final_count, like_count)

        time.sleep(2)

    def test_add_comment(self):

        self.browser.get(self.live_server_url+reverse('login'))
        loginForm = self.browser.find_element_by_class_name("login_form")
        loginForm.find_element_by_name("username").send_keys("Wise124")
        loginForm.find_element_by_name("password").send_keys("Khan1234")
        loginForm.find_element_by_class_name("login").click()
        

        username = self.browser.find_element_by_class_name("user_btns").find_element_by_id("profile").text
        #checks if login is successfull
        self.assertEqual("Wise124", username)

        #adding comment
        self.browser.get(self.live_server_url + reverse('Article', args='1'))
        time.sleep(2)
        self.browser.find_element_by_class_name('comment-form').find_element_by_tag_name("textarea").send_keys("this is a comment")
        self.browser.find_element_by_class_name('comment-form').find_element_by_id("comment_btn").click()
        time.sleep(2)
        comment_obj = Comment.objects.get(content = "this is a comment" )
        id = comment_obj.id
        comment = self.browser.find_element_by_id("content-" + str(id)).text
        self.assertEqual("this is a comment", comment)
    
    def test_delete_comment(self):

        self.browser.get(self.live_server_url+reverse('login'))
        loginForm = self.browser.find_element_by_class_name("login_form")
        loginForm.find_element_by_name("username").send_keys("Wise124")
        loginForm.find_element_by_name("password").send_keys("Khan1234")
        loginForm.find_element_by_class_name("login").click()
        

        username = self.browser.find_element_by_class_name("user_btns").find_element_by_id("profile").text
        #checks if login is successfull
        self.assertEqual("Wise124", username)
        
        article = Article.objects.get(id = 1)
        comment_obj = list(Comment.objects.filter(article = article))
        id = comment_obj[0].id

        #deleting comment
        self.browser.get(self.live_server_url + reverse('Article', args='1'))
        time.sleep(2)
        count = self.browser.find_element_by_id("num-comment").text
        count = int(count.split(" ")[0])
        self.browser.find_element_by_id("main-" + str(id)).find_element_by_class_name("delete-btn").click()
        alert_obj = self.browser.switch_to.alert
        alert_obj.accept()
        time.sleep(2)
        final_count = self.browser.find_element_by_id("num-comment").text
        final_count = int(final_count.split(" ")[0])
        count-=1
        self.assertEqual(count, final_count)
        time.sleep(1)
   
        