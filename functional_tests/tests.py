import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        # Edith has heard about a cool online
        # app with todolists. She decides to evaluate it.
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        # Satisfied she goes to bed
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.2)

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # She sees header and title of the page talk about
        # To Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do items
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She enters 'Buy feathers' in the text field
        inputbox.send_keys('Buy feathers')

        # When she pushes 'Enter', the page is reloaded
        # and the page has "1: Buy feathers' as a list item.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy feathers')

        # The text field still invites her to enter a to-do.
        # She enters "Make fan of feathers" to the text field
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make fan of feathers')
        inputbox.send_keys(Keys.ENTER)

        # The page is reloaded and has 2 items of her list.
        self.wait_for_row_in_list_table('1: Buy feathers')
        self.wait_for_row_in_list_table('2: Make fan of feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # User 1: Edith
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)

        # The page is reloaded and has 2 items of her list.
        self.wait_for_row_in_list_table('1: Buy feathers')

        # Edith is interested if the site has remembered her list.
        # Then she sees a special URL-address with explanations.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # User 2: Francis
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertNotIn('Make fan of feathers', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # The page is reloaded and has 2 items of her list.
        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # No traces of Edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
