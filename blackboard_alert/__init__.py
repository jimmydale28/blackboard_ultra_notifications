from blackboard_alert.config import Config
from blackboard_alert.main.get_bb_data import bb

def start(config_class=Config):
	site_url = ''
	user_name = ''
	password = ''
	classes = 

	BB = bb(site_url, user_name, password, classes)
	BB.nav_home()
	BB.login_input()
	BB.login_submit()
	BB.click_grades()

	BB.get_all_work()
