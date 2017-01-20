import sqlite3
from time import time

def migrate():
	db = sqlite3.connect('database.sqlite')

	lastMigration = None
	try:
		lastMigration = db.execute('SELECT id FROM migrations ORDER BY id DESC LIMIT 1').fetchone()[0]
	except(sqlite3.OperationalError):
		create_migrations_table(db)
	
	if lastMigration == None:
		lastMigration = '0'

	lastMigration = str(int(lastMigration) + 1)

	count = 0
	while 'migration'+lastMigration in globals():
		globals()['migration'+lastMigration](db)
		db.execute('INSERT INTO migrations (id, date) VALUES ({}, {})'.format(lastMigration, time()))
		lastMigration = str(int(lastMigration)+1)
		count += 1

	print (str(count)+' new migrations appruved')

	db.commit()
	db.close()

def create_migrations_table(db):

	db.execute('''
		CREATE TABLE migrations (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`date` UNSIGNED INTEGER NOT NULL
		);
	''')

def migration1(db):
	
	db.execute(''' 
		CREATE TABLE user (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`active` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`last_message` INTEGER NOT NULL DEFAULT 0,
			`gender` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`name` VARCHAR(255) DEFAULT NULL,
			`race_id` UNSIGNED INTEGER DEFAULT NULL,
			`level` UNSIGNED INTEGER DEFAULT 1,
			`exp` UNSIGNED INTEGER DEFAULT 0,
			`points_lost` UNSIGNED INTEGER DEFAULT 5,
			`money` UNSIGNED INTEGER DEFAULT 100,
			`current_state` UNSIGNED INTEGER DEFAULT 0,
			`prev_state` UNSIGNED INTEGER DEFAULT 0,
			`location_id` UNSIGNED INTEGER DEFAULT 1,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(2) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(2) DEFAULT 10,
			`attack_mob_id` UNSIGNED INTEGER DEFAULT NULL
		);
	''')
	db.execute('''
		CREATE TABLE item (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`proto_id` UNSIGNED INTEGER NOT NULL,
			`user_id` UNSIGNED INTEGER DEFAULT NULL,
			`location_id` UNSIGNED INTEGER DEFAULT NULL,
			`mob_id` UNSIGNED INTEGER DEFAULT NULL,
			`item_id` UNSIGNED INTEGER NOT NULL DEFAULT 0
		);
	''')
	db.execute('''
		CREATE TABLE mob (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`proto_id` UNSIGNED INTEGER NOT NULL,
			`location_id` UNSIGNED INTEGER NOT NULL,
			`name` VARCHAR(255) DEFAULT NULL,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(2) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(2) DEFAULT 10		
		);
	''')

def migration2(db):
	db.execute('ALTER TABLE user RENAME TO tmp_user;')
	db.execute('''
		CREATE TABLE user (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`active` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`last_message` INTEGER NOT NULL DEFAULT 0,
			`gender` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`name` VARCHAR(255) DEFAULT NULL,
			`race_id` UNSIGNED INTEGER DEFAULT NULL,
			`level` UNSIGNED INTEGER DEFAULT 1,
			`exp` UNSIGNED INTEGER DEFAULT 0,
			`points_lost` UNSIGNED INTEGER DEFAULT 5,
			`money` UNSIGNED INTEGER DEFAULT 100,
			`current_state` UNSIGNED INTEGER DEFAULT 0,
			`prev_state` UNSIGNED INTEGER DEFAULT 0,
			`location_id` UNSIGNED INTEGER DEFAULT 1,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`axe` UNSIGNED REAL DEFAULT 0,
			`crossbow` UNSIGNED REAL DEFAULT 0,
			`hammer` UNSIGNED REAL DEFAULT 0,
			`knife` UNSIGNED REAL DEFAULT 0,
			`mace` UNSIGNED REAL DEFAULT 0,
			`pike` UNSIGNED REAL DEFAULT 0,
			`spear` UNSIGNED REAL DEFAULT 0,
			`lash` UNSIGNED REAL DEFAULT 0,
			`blowgun` UNSIGNED REAL DEFAULT 0,
			`bite` UNSIGNED REAL DEFAULT 0,
			`punch` UNSIGNED REAL DEFAULT 0,
			`kick` UNSIGNED REAL DEFAULT 0,
			`arch` UNSIGNED REAL DEFAULT 0,
			`fight` UNSIGNED REAL DEFAULT 0,
			`dodge` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(2) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(2) DEFAULT 10,
			`attack_mob_id` UNSIGNED INTEGER DEFAULT NULL
		);
	''')
	db.execute('''
		INSERT INTO user 
			(`id`,`active`,`last_message`,`gender`,`name`,`race_id`,`level`,`exp`,`points_lost`,`money`,`current_state`,`prev_state`,`location_id`,`st`,`dx`,`iq`,`ht`,`sword`,`bow`,`throw`,`hp`,`hp_max`, `attack_mob_id` )
		SELECT  
			`id`, `active`, `last_message`, `gender`, `name`, `race_id`, `level`, `exp`, `points_lost`, `money`, `current_state`, `prev_state`, `location_id`, `st`, `dx`, `iq`, `ht`, `sword`, `bow`, `throw`, `hp`, `hp_max`, `attack_mob_id` 
		FROM tmp_user WHERE 1
	''')
	db.execute('DROP TABLE tmp_user')


def migration3(db):
	db.execute('ALTER TABLE mob RENAME TO tmp_mob;')
	db.execute('''
		CREATE TABLE `mob` (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`proto_id` UNSIGNED INTEGER NOT NULL,
			`location_id` UNSIGNED INTEGER NOT NULL,
			`name` VARCHAR(255) DEFAULT NULL,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`axe` UNSIGNED REAL DEFAULT 0,
			`crossbow` UNSIGNED REAL DEFAULT 0,
			`hammer` UNSIGNED REAL DEFAULT 0,
			`knife` UNSIGNED REAL DEFAULT 0,
			`mace` UNSIGNED REAL DEFAULT 0,
			`pike` UNSIGNED REAL DEFAULT 0,
			`spear` UNSIGNED REAL DEFAULT 0,
			`lash` UNSIGNED REAL DEFAULT 0,
			`blowgun` UNSIGNED REAL DEFAULT 0,
			`bite` UNSIGNED REAL DEFAULT 0,
			`punch` UNSIGNED REAL DEFAULT 0,
			`kick` UNSIGNED REAL DEFAULT 0,
			`arch` UNSIGNED REAL DEFAULT 0,
			`fight` UNSIGNED REAL DEFAULT 0,
			`dodge` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(2) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(2) DEFAULT 10		
		);
	''')
	db.execute('''
		INSERT INTO mob 
			(`id`,`proto_id`,`location_id`,`name`,`st`,`dx`,`iq`,`ht`,`sword`,`bow`,`throw`,`hp`,`hp_max`)
		SELECT  
			`id`,`proto_id`,`location_id`,`name`,`st`,`dx`,`iq`,`ht`,`sword`,`bow`,`throw`,`hp`,`hp_max`
		FROM tmp_mob WHERE 1
	''')
	db.execute('DROP TABLE tmp_mob')

def migration4(db):
	db.execute('ALTER TABLE user RENAME TO tmp_user;')
	db.execute('''
		CREATE TABLE user (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`active` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`last_message` INTEGER NOT NULL DEFAULT 0,
			`gender` UNSIGNED INTEGER(1) NOT NULL DEFAULT 0,
			`name` VARCHAR(255) DEFAULT NULL,
			`race_id` UNSIGNED INTEGER DEFAULT NULL,
			`level` UNSIGNED INTEGER DEFAULT 1,
			`exp` UNSIGNED INTEGER DEFAULT 0,
			`points_lost` UNSIGNED INTEGER DEFAULT 5,
			`money` UNSIGNED INTEGER DEFAULT 100,
			`current_state` UNSIGNED INTEGER DEFAULT 0,
			`prev_state` UNSIGNED INTEGER DEFAULT 0,
			`location_id` UNSIGNED INTEGER DEFAULT 1,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`axe` UNSIGNED REAL DEFAULT 0,
			`crossbow` UNSIGNED REAL DEFAULT 0,
			`hammer` UNSIGNED REAL DEFAULT 0,
			`knife` UNSIGNED REAL DEFAULT 0,
			`mace` UNSIGNED REAL DEFAULT 0,
			`pike` UNSIGNED REAL DEFAULT 0,
			`spear` UNSIGNED REAL DEFAULT 0,
			`lash` UNSIGNED REAL DEFAULT 0,
			`blowgun` UNSIGNED REAL DEFAULT 0,
			`bite` UNSIGNED REAL DEFAULT 0,
			`punch` UNSIGNED REAL DEFAULT 0,
			`kick` UNSIGNED REAL DEFAULT 0,
			`arch` UNSIGNED REAL DEFAULT 0,
			`fight` UNSIGNED REAL DEFAULT 0,
			`dodge` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(3) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(3) DEFAULT 10,
			
			`mp` UNSIGNED INTEGER(3) DEFAULT 10,
			`mp_max` UNSIGNED INTEGER(3) DEFAULT 10,
			`fire` UNSIGNED REAL DEFAULT 0,
			`water` UNSIGNED REAL DEFAULT 0,
			`air` UNSIGNED REAL DEFAULT 0,
			`ground` UNSIGNED REAL DEFAULT 0,
			`dark` UNSIGNED REAL DEFAULT 0,
			`light` UNSIGNED REAL DEFAULT 0,

			`attack_mob_id` UNSIGNED INTEGER DEFAULT NULL
		);
	''')
	db.execute('''
		INSERT INTO user 
			(`id`, `active`, `last_message`, `gender`, `name`, `race_id`, `level`, `exp`, `points_lost`, `money`, `current_state`, `prev_state`, `location_id`, `st`, `dx`, `iq`, `ht`, `sword`, `bow`, `throw`, `axe`, `crossbow`, `hammer`, `knife`, `mace`, `pike`, `spear`, `lash`, `blowgun`, `bite`, `punch`, `kick`, `arch`, `fight`, `dodge`, `hp`, `hp_max`, `attack_mob_id`)
		SELECT  
			`id`, `active`, `last_message`, `gender`, `name`, `race_id`, `level`, `exp`, `points_lost`, `money`, `current_state`, `prev_state`, `location_id`, `st`, `dx`, `iq`, `ht`, `sword`, `bow`, `throw`, `axe`, `crossbow`, `hammer`, `knife`, `mace`, `pike`, `spear`, `lash`, `blowgun`, `bite`, `punch`, `kick`, `arch`, `fight`, `dodge`, `hp`, `hp_max`, `attack_mob_id`
		FROM tmp_user WHERE 1
	''')
	db.execute('DROP TABLE tmp_user')

	db.execute('ALTER TABLE mob RENAME TO tmp_mob;')
	db.execute('''
		CREATE TABLE `mob` (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`proto_id` UNSIGNED INTEGER NOT NULL,
			`location_id` UNSIGNED INTEGER NOT NULL,
			`name` VARCHAR(255) DEFAULT NULL,
			`st` UNSIGNED INTEGER DEFAULT 10,
			`dx` UNSIGNED INTEGER DEFAULT 10,
			`iq` UNSIGNED INTEGER DEFAULT 10,
			`ht` UNSIGNED INTEGER DEFAULT 10,
			`sword` UNSIGNED REAL DEFAULT 0,
			`bow` UNSIGNED REAL DEFAULT 0,
			`throw` UNSIGNED REAL DEFAULT 0,
			`axe` UNSIGNED REAL DEFAULT 0,
			`crossbow` UNSIGNED REAL DEFAULT 0,
			`hammer` UNSIGNED REAL DEFAULT 0,
			`knife` UNSIGNED REAL DEFAULT 0,
			`mace` UNSIGNED REAL DEFAULT 0,
			`pike` UNSIGNED REAL DEFAULT 0,
			`spear` UNSIGNED REAL DEFAULT 0,
			`lash` UNSIGNED REAL DEFAULT 0,
			`blowgun` UNSIGNED REAL DEFAULT 0,
			`bite` UNSIGNED REAL DEFAULT 0,
			`punch` UNSIGNED REAL DEFAULT 0,
			`kick` UNSIGNED REAL DEFAULT 0,
			`arch` UNSIGNED REAL DEFAULT 0,
			`fight` UNSIGNED REAL DEFAULT 0,
			`dodge` UNSIGNED REAL DEFAULT 0,
			`hp` UNSIGNED INTEGER(2) DEFAULT 10,
			`hp_max` UNSIGNED INTEGER(2) DEFAULT 10,
			
			`mp` UNSIGNED INTEGER(3) DEFAULT 10,
			`mp_max` UNSIGNED INTEGER(3) DEFAULT 10,
			`fire` UNSIGNED REAL DEFAULT 0,
			`water` UNSIGNED REAL DEFAULT 0,
			`air` UNSIGNED REAL DEFAULT 0,
			`ground` UNSIGNED REAL DEFAULT 0,
			`dark` UNSIGNED REAL DEFAULT 0,
			`light` UNSIGNED REAL DEFAULT 0
		);
	''')
	db.execute('''
		INSERT INTO mob 
			(`id`, `proto_id`, `location_id`, `name`, `st`, `dx`, `iq`, `ht`, `sword`, `bow`, `throw`, `axe`, `crossbow`, `hammer`, `knife`, `mace`, `pike`, `spear`, `lash`, `blowgun`, `bite`, `punch`, `kick`, `arch`, `fight`, `dodge`, `hp`, `hp_max`)
		SELECT  
			`id`, `proto_id`, `location_id`, `name`, `st`, `dx`, `iq`, `ht`, `sword`, `bow`, `throw`, `axe`, `crossbow`, `hammer`, `knife`, `mace`, `pike`, `spear`, `lash`, `blowgun`, `bite`, `punch`, `kick`, `arch`, `fight`, `dodge`, `hp`, `hp_max`
		FROM tmp_mob WHERE 1
	''')
	db.execute('DROP TABLE tmp_mob')

def migration5(db):
	db.execute('''
		CREATE TABLE `spell` (
			`id` INTEGER PRIMARY KEY NOT NULL,
			`proto_id` UNSIGNED INTEGER NOT NULL,
			`user_id` UNSIGNED INTEGER NOT NULL
		);
	''')


if __name__ == '__main__':
	migrate()