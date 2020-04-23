import sqlite3
import datetime


class write_database:
	def __init__(self):
		self.conn = sqlite3.connect('blackboard.db')
		self.c = self.conn.cursor()

	def check_existance(self, database_name):
		exists = False
		try:
			self.c.execute('''
				CREATE TABLE %s
				(ASSIGNMENT text, ASSIGNMENT_DATE date, ASSIGNMENT_STATUS text, ASSIGNMENT_GRADE text);
				''' % database_name)
			self.conn.commit()
			exists = True
		except sqlite3.OperationalError:
			exists = True

		return exists

	def check_assignment(self, database_name, assignment_name):
		check_flag = False
		try:
			self.c.execute('''
				SELECT * FROM %s 
				WHERE ASSIGNMENT IN (%s);
				''' % (database_name, assignment_name)
				)
			double_check = self.c.fetchall()
			if len(double_check) > 0:
				check_flag = True
		except sqlite3.OperationalError:
			pass
		return check_flag

	def get_assignment_grade(self, database_name, assignment_name):
		self.c.execute('''
			SELECT ASSIGNMENT_GRADE FROM %s
			WHERE ASSIGNMENT IN (%s);
			'''  % (database_name, assignment_name))
		self.conn.commit()
		query = self.c.fetchone()

		return query[0]

	def update_assignment_record(self, database_name, assignment_name, assignment_stats, assignment_grade):
		self.c.execute('''
			UPDATE %s
			SET ASSIGNMENT_STATUS = %s, ASSIGNMENT_GRADE = %s
			WHERE ASSIGNMENT IN (%s);
			'''  % (database_name, assignment_stats, assignment_grade, assignment_name))
		self.conn.commit()

	def add_assignment(self, database_name, assignment_name, assignment_date, assignment_stats, assignment_grade):
		self.c.execute('''
			INSERT INTO %s (ASSIGNMENT, ASSIGNMENT_DATE, ASSIGNMENT_STATUS, ASSIGNMENT_GRADE)
			VALUES (%s, %s, %s, %s);
			''' % (database_name, assignment_name, assignment_date, assignment_stats, assignment_grade))
		self.conn.commit()

	def write(self, database_name, entry):
		db_name = database_name.replace(' ', '_')
		exists = self.check_existance(db_name)

		entry_date = entry[1]
		
		if ' ' in entry_date:
			entry_date_split = entry_date.split(' ')
			try:
				entry_date = "'%s'" % datetime.datetime.strptime(entry_date_split[len(entry_date_split)-1], '%m/%d/%y')
			except ValueError:
				arbortery_date = '01/01/20'
				entry_date = "'%s'" % datetime.datetime.strptime(arbortery_date, '%m/%d/%y')
		else:
			entry_date = "'%s'" % datetime.datetime.strptime(entry_date, '%m/%d/%y')

		entry_name, entry_status, entry_grade = "'%s'" % entry[0], "'%s'" % entry[2], "'%s'" % entry[3]

		if exists == True:
			assignment_check = self.check_assignment(db_name, entry_name)
			if assignment_check == False:
				self.add_assignment(db_name, entry_name, entry_date, entry_status, entry_grade)
			else:

				db_assignment_grade = self.get_assignment_grade(db_name, entry_name)
				assignment_grade = entry_grade

				if db_assignment_grade != assignment_grade:
					self.update_assignment_record(db_name, entry_name, entry_status, entry_grade)
