import sqlite3

def reset(userId):
	db = sqlite3.connect('database.sqlite')
	db.execute('DELETE FROM user WHERE id = {}'.format(userId))
	db.execute('DELETE FROM item WHERE user_id = {}'.format(userId))
	db.commit()
	db.close()
