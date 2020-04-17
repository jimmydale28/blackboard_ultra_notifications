from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from collections import defaultdict


class parser:
	def __init__(self):
		self.done = []

	def build_element_dict(self, in_element):
		elem_dict = defaultdict(str)

		for i in in_element:
			elem_dict[i.find_element_by_xpath('..').get_attribute('aria-label')] = i

		return dict(elem_dict)

	def get_work_element(self, in_element):
		in_dict = self.build_element_dict(in_element)
		return_ele = None

		for class_name, element in in_dict.items():
			name = class_name.split(',')[0].replace('View all work for ', '')
			if name not in self.done:
				self.done.append(name)
				return_ele = element
				break
			else:
				pass

		return return_ele

	def get_current_done(self):
		return self.done[len(self.done)-1]
	
class bb():
	def __init__(self, site_url, user_name, password):
		self.site_url = site_url
		self.user_name = user_name
		self.password = password
		self.browser = Firefox(executable_path='C:/Python3/Lib/site-packages/selenium/webdriver/firefox/geckodriver.exe')
		self.parser = parser()

	def nav_home(self):
		self.browser.get(self.site_url)

	def login_input(self):
		user_input = self.browser.find_element_by_id('user_id')
		user_input.send_keys(self.user_name)

		user_pass = self.browser.find_element_by_id('password')
		user_pass.send_keys(self.password)

	def login_submit(self):
		submit_button = self.browser.find_element_by_id('entry-login')
		try:
			submit_button.click()
		except ElementClickInterceptedException:
			self.handle_login_intercept()

	def handle_login_intercept(self):
		try:
			agree_button = self.browser.find_element_by_id('agree_button')
			agree_button.click()
			self.login_submit()
		except NoSuchElementException:
			time.sleep(2)
			return self.handle_login_intercept()

	def click_grades(self):
		self.browser.get('%s/ultra/grades' % self.site_url)

	def get_all_work(self):
		try:
			view_work = self.browser.find_elements_by_xpath('//span[contains(text(), \"View all work\")]')
			assert len(view_work) > 1
			work_ele = self.parser.get_work_element(view_work)
			if work_ele != None:
				self.click_all_work(work_ele)
			else:
				print('\n\nScript Finished\n\n')

		except NoSuchElementException:
			time.sleep(5)
			return self.get_all_work()

		except AssertionError:
			time.sleep(5)
			print('except')
			return self.get_all_work()

		except ElementClickInterceptedException:
			time.sleep(5)
			print('Intercept exception')
			return self.get_all_work()


	def click_all_work(self, work_element):
		work_element.click()
		print('done')
		self.get_item_elements()


	def get_item_elements(self):
		row_elements = []
		try:
			div_elements = self.browser.find_elements_by_css_selector('div')
			for ele in div_elements:
				if ele.get_attribute("class") == 'row tabular-row js-row child-is-invokable':
					row_elements.append(ele)
		except:
			time.sleep(5)
			print('exception get items')
			return self.get_item_elements()

		'''DATABASE NAME'''
		print('\n\nDATABASE NAME\n%s\n\n' % self.parser.get_current_done())
		for ele in row_elements:
			ele_text = ele.text

			e_text = ele_text.split('\n')
			assignment, due, status, grade = None, None, None, None,
			try:
				assignment = e_text[0]
			except:
				pass
			try:
				due = e_text[1]
			except:
				pass
			try:
				status = e_text[2]
			except:
				pass
			try:
				grade = e_text[3]
			except:
				pass

			'''DATABASE ENTRY'''
			print(assignment, due, status, grade)

		self.click_grades()
		time.sleep(5)
		self.get_all_work()


if __name__ == '__main__':

	site_url = ''
	user_name = ''
	password = ''

	BB = bb(site_url, user_name, password)
	BB.nav_home()
	BB.login_input()
	BB.login_submit()
	BB.click_grades()

	BB.get_all_work()
