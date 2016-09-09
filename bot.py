#!/usr/bin/env python3

from telegram import ReplyKeyboardMarkup,ReplyKeyboardHide,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackQueryHandler
from classes import *
from consts import *
from reset import reset
from diceroller import DiceRoller
import sys
import logging
import json
from sqlobject import SQLObjectNotFound
import random
from prototypesloader import load_item_prototype, load_ability, load_trader, load_mob_prototype
# from tabulate import tabulate

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(token='236596213:AAHiE9gdpLZXV28KulV1I57Ztui5CB3ggvY')

loadedUsers = {}
def get_user(id):
	if not id in loadedUsers or not loadedUsers[id]:
		try:
			loadedUsers[id] = User.get(id)
		except SQLObjectNotFound:
			loadedUsers[id] = User(id = id)
	
	return loadedUsers[id]

def create_keyboard(actions = [], autoformat = True):
	if len(actions):
		if autoformat:
			buttons = [[action] for action in actions]
		else:
			buttons = actions
		return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
	else:
		return ReplyKeyboardHide()

def line_bar(n, start, end, fill = ':', empty = '.', length = 25):

	distance = end - start
	i = distance / length
	pos = int((n - start) / i)

	return '[ '+ ''.join([fill for i in range(0,pos)]) + ''.join([empty for i in range(0,length-pos)]) +' ]'

SESSION = {}

def check_session_data(userId):
	if not userId in SESSION:
		SESSION[userId] = {}

def get_session_data(userId, name):
	check_session_data(userId)
	if name in SESSION[userId]:
		return SESSION[userId][name]
	else:
		return None

def set_session_data(userId, name, value):
	check_session_data(userId)
	SESSION[userId][name] = value

def clear_session_data(userId):
	SESSION[userId] = {}

def standart_keyboard(user):
	actions = [[ACTION_LOOK_OUT, ACTION_CHANGE_LOCATION], [ACTION_OPEN_INVENTORY, ACTION_LOOK_ATTRIBUTES], [ACTION_MAKE_SPECIAL_ACTION]]
	location = user.getLocation()

	if (location.getItems().count()):
		actions[2].append(ACTION_GET_ITEM)
	if (location.getMobs().count()):
		actions[2].append(ACTION_ATTACK)

	return create_keyboard(actions, False)

def what_next(bot, user, text = 'Что дальше?'):
	return bot.sendMessage(user.id, text, reply_markup = standart_keyboard(user))


def start(bot, update):
	reset(update.message.chat.id)
	loadedUsers[id] = None
	user = get_user(update.message.chat.id)
	user.currentState = STATE_UNREGISTERED
	start_message(bot, update, user)

def debug(bot, update):
	user = get_user(update.message.chat.id)
	bot.sendMessage(user.id, json.dumps(user.serialize()))

def additem(bot, update):
	user = get_user(update.message.chat.id)
	command = update.message.text.split(' ')
	if len(command) > 1:
		protoId = int(command[1])
		parentId = 0
		if len(command) > 2:
			parentId = int(command[2])
		user.addItem(protoId, parentId)
		bot.sendMessage(user.id, "added")

def resetstate(bot, update):
	user = get_user(update.message.chat.id)
	user.currentState = STATE_JUST_STAYING
	user.prevState = STATE_JUST_STAYING
	bot.sendMessage(user.id, "resetted")

def spawn(bot, update):
	user = get_user(update.message.chat.id)
	command = update.message.text.split(' ')
	if len(command) > 1:
		protoId = int(command[1])
		mob = Mob.create(protoId = protoId, locationId = user.locationId)
		bot.sendMessage(user.id, "spawned")

def addexp(bot, update):
	user = get_user(update.message.chat.id)
	command = update.message.text.split(' ')
	if len(command) > 1:
		val = int(command[1])
		user.addExp(bot, val)
		bot.sendMessage(user.id, "added")


def start_message(bot, update, user):
	bot.sendMessage(user.id, 'Добро пожаловать в Тармиан!')
	input_nick(bot, update, user)
	
AVAILABLE_RACES = [load_mob_prototype(i) for i in (1,3,4)]

def input_nick(bot, update, user):
	if user.currentState == STATE_WAITING_INPUT_NICK and update.message.text:
		if len(update.message.text) > 20:
			bot.sendMessage(user.id, "Ник слишком длинный", reply_markup = create_keyboard())
			return
		user.name = update.message.text
		user.currentState = STATE_WAITING_INPUT_RACE
		bot.sendMessage(user.id, "Привет, "+user.name+"! Выбери расу своего персонажа", reply_markup = create_keyboard([race.name for race in AVAILABLE_RACES]))
	else:
		user.currentState = STATE_WAITING_INPUT_NICK
		bot.sendMessage(user.id, "Введите ник", reply_markup = create_keyboard())

def input_race(bot, update, user):

	if user.currentState == STATE_WAITING_INPUT_RACE and update.message.text in [race.name for race in AVAILABLE_RACES]:
		for race in AVAILABLE_RACES:
			if race.name == update.message.text:
				user.raceId = race.id
				user.race = load_mob_prototype(user.raceId)
				user.currentState = STATE_WAITING_INPUT_GENDER
				bot.sendMessage(user.id, "Выбери свой пол", reply_markup = create_keyboard([[GENDER_MALE, GENDER_FEMALE]], False))
				return

	bot.sendMessage(user.id, "Выбери расу своего персонажа", reply_markup = create_keyboard([race.name for race in AVAILABLE_RACES]))


def input_gender(bot, update, user):
	if update.message.text and update.message.text in (GENDER_MALE, GENDER_FEMALE):
		if update.message.text == GENDER_FEMALE:
			user.gender = GENDER_FEMALE_ID
		else:
			user.gender = GENDER_MALE_ID
		user.currentState = STATE_WAITING_INPUT_ATTRIBUTES
		bot.send_sticker(user.id, GENDER_STICKERS[user.gender], reply_markup = create_keyboard())
		return input_attributes(bot, update, user)
	else:
		bot.sendMessage(user.id, "Выбери свой пол", reply_markup = create_keyboard([['Мужской', 'Женский']], False))

def attributes_keyboard(user):
	keyboard = [
		[InlineKeyboardButton('Очков осталось: '+str(user.pointsLost),callback_data='a')],
		[InlineKeyboardButton(ST, callback_data='st'), InlineKeyboardButton(BLOCKED,callback_data='st-'), InlineKeyboardButton('[ '+str(user.st)+' ]',callback_data='st'), InlineKeyboardButton(BLOCKED,callback_data='st+')],
		[InlineKeyboardButton(DX, callback_data='dx'), InlineKeyboardButton(BLOCKED,callback_data='dx-'), InlineKeyboardButton('[ '+str(user.dx)+' ]',callback_data='dx'), InlineKeyboardButton(BLOCKED,callback_data='dx+')],
		[InlineKeyboardButton(IQ, callback_data='iq'), InlineKeyboardButton(BLOCKED,callback_data='iq-'), InlineKeyboardButton('[ '+str(user.iq)+' ]',callback_data='iq'), InlineKeyboardButton(BLOCKED,callback_data='iq+')],
		[InlineKeyboardButton(HT, callback_data='ht'), InlineKeyboardButton(BLOCKED,callback_data='ht-'), InlineKeyboardButton('[ '+str(user.ht)+' ]',callback_data='ht'), InlineKeyboardButton(BLOCKED,callback_data='ht+')]
	]

	race = user.race
	if user.st > race.st // 2:
		keyboard[1][1].text = MINUS
	if user.pointsLost > 0 and user.st < race.st*1.5:
		keyboard[1][3].text = PLUS
	if user.dx > race.dx // 2:
		keyboard[2][1].text = MINUS
	if user.pointsLost > 0 and user.dx < race.dx*1.5:
		keyboard[2][3].text = PLUS
	if user.iq > race.iq // 2:
		keyboard[3][1].text = MINUS
	if user.pointsLost > 0 and user.iq < race.iq*1.5:
		keyboard[3][3].text = PLUS
	if user.ht > race.ht // 2:
		keyboard[4][1].text = MINUS
	if user.pointsLost > 0 and user.ht < race.ht*1.5:
		keyboard[4][3].text = PLUS

	if user.pointsLost == 0:
		keyboard.append([InlineKeyboardButton('Готово', callback_data='done')])
	return InlineKeyboardMarkup(keyboard)

def input_attributes(bot, update, user):
	race = user.race
	user.st = race.st
	user.dx = race.dx
	user.iq = race.iq
	user.ht = race.ht
	user.hpMax = race.hpMax
	user.hp = race.hpMax
	user.pointsLost = 5
	bot.sendMessage(user.id, "Распредели стартовые очки по аттрибутам", reply_markup = attributes_keyboard(user))

def button_attributes(bot, update, user):
	query = update.callback_query
	if query.data == 'done':
		bot.editMessageText(text = "Вы распределили стартовые очки следующим образом:\n"+ST+": "+str(user.st)+"\n"+DX+": "+str(user.dx)+"\n"+IQ+": "+str(user.iq)+"\n"+HT+": "+str(user.ht),chat_id=user.id,message_id=query.message.message_id)
		return input_weapon(bot, update, user)

	p = user.st+user.dx+user.iq+user.ht
	race = user.race

	if query.data == 'st-':
		if user.st > race.st // 2:
			user.st -= 1
	elif query.data == 'st+':
		if user.pointsLost > 0 and user.st < race.st*1.5:
			user.st += 1
	elif query.data == 'dx-':
		if user.dx > race.dx // 2:
			user.dx -= 1
	elif query.data == 'dx+':
		if user.pointsLost > 0 and user.dx < race.dx*1.5:
			user.dx += 1
	elif query.data == 'iq-':
		if user.iq > race.iq // 2:
			user.iq -= 1
	elif query.data == 'iq+':
		if user.pointsLost > 0 and user.iq < race.iq*1.5:
			user.iq += 1
	elif query.data == 'ht-':
		if user.ht > race.ht // 2:
			user.ht -= 1
	elif query.data == 'ht+':
		if user.pointsLost > 0 and user.ht < race.ht*1.5:
			user.ht += 1


	if p == user.st+user.dx+user.iq+user.ht:
		return

	user.pointsLost += p - (user.st+user.dx+user.iq+user.ht)

	bot.editMessageReplyMarkup(reply_markup = attributes_keyboard(user),chat_id=user.id,message_id=query.message.message_id)

def input_weapon(bot, update, user):

	if user.currentState == STATE_WAITING_INPUT_WEAPON and update.message.text and update.message.text in (WEAPON_BOW, WEAPON_SWORD):
		if update.message.text == WEAPON_SWORD:
			user.sword += 1
			user.addItem(WEAPON_SWORD_ID)
		elif update.message.text == WEAPON_BOW:
			user.bow += 1
			user.addItem(WEAPON_BOW_ID)
			q = user.addItem(3) # колчан
			for i in range(0,30):
				user.addItem(4, q)

		user.currentState = STATE_JUST_STARTED
		bot.sendMessage(user.id, "Игра началась", reply_markup = create_keyboard(['Где я?']))
	else:
		user.currentState = STATE_WAITING_INPUT_WEAPON
		bot.sendMessage(user.id, "Выбери оружие", reply_markup = create_keyboard([[WEAPON_SWORD, WEAPON_BOW]], False))

def inventory_keyboard(user, itemId = 0):

	keyboard = []
	items = []
	if (itemId):
		item = Item.get(itemId)
		if item.isContainer():
			items = item.items
			keyboard.append([InlineKeyboardButton('[ '+item.getName()+' ]', callback_data = 'all'),InlineKeyboardButton('Вещей внутри: '+str(len(items)), callback_data = 'all')])
		else:
			keyboard.append([InlineKeyboardButton('[ '+item.getName()+' ]', callback_data = 'all')])
	else:
		items = [item for item in user.items if item.itemId == 0]
		keyboard.append([InlineKeyboardButton('Деньги: '+str(user.money)+MONEY, callback_data = 'money'), InlineKeyboardButton('Вещи: '+str(len(items)), callback_data = 'all')])

	itemTypes = {}
	i = 0
	for innerItem in items:
		row = [InlineKeyboardButton(innerItem.getName(), callback_data = 'open:'+str(innerItem.id))]
		if itemId:
			row.append(InlineKeyboardButton(ITEM_REMOVE, callback_data = 'remove:'+str(innerItem.id)))
		row.append(InlineKeyboardButton(ITEM_PUT, callback_data = 'put:'+str(innerItem.id)))
		row.append(InlineKeyboardButton(ITEM_DROP, callback_data = 'drop:'+str(innerItem.id)))

		if innerItem.isStackable() and innerItem.protoId in itemTypes:
			pos, count = itemTypes[innerItem.protoId]
			count += 1
			row[0] = InlineKeyboardButton(innerItem.getName()+' ('+str(count)+')', callback_data = 'open:'+str(innerItem.id))
			keyboard[pos] = row
		else:
			count = 1
			i += 1
			keyboard.append(row)

		if innerItem.isStackable():
			itemTypes[innerItem.protoId] = (i, count)			
	
	if itemId:
		if len(item.getActions()):
			for action in item.getActions():
				keyboard.append([InlineKeyboardButton('[ '+action+' ]', callback_data = 'makeaction:'+str(item.id)+':'+action)])
		keyboard.append([InlineKeyboardButton('Назад', callback_data = 'open:'+str(item.itemId)), InlineKeyboardButton('Закрыть инвентарь', callback_data = 'close')])
	else:
		keyboard.append([InlineKeyboardButton('Закрыть инвентарь', callback_data = 'close')])

	return InlineKeyboardMarkup(keyboard)

def put_item_keyboard(user, itemId):
	keyboard = []
	items = [item for item in user.items if item.isContainer() and item.id != itemId]
	for item in items:
		row = [
			InlineKeyboardButton(item.getName(), callback_data = 'putconfirm:'+str(itemId)+':'+str(item.id)),
		]
		keyboard.append(row)
	keyboard.append([InlineKeyboardButton('Отмена', callback_data = 'actioncancel:'+str(itemId))])
	return InlineKeyboardMarkup(keyboard)

def open_inventory(bot, update, user):
	user.currentState = STATE_INVENTORY
	bot.sendMessage(user.id, "Ваш инвентарь:", reply_markup = inventory_keyboard(user))

def button_inventory(bot, update, user):
	query = update.callback_query
	
	ar = query.data.split(':')
	if len(ar) > 1:
		command, itemId = ar[0], int(ar[1])
		if len(ar) > 2:
			secondArgument = ar[2]

		if itemId:
			item = Item.get(itemId)
	else:
		command = query.data

	if command == 'open':
		bot.editMessageReplyMarkup(reply_markup = inventory_keyboard(user, itemId),chat_id=user.id,message_id=query.message.message_id)
		return
	if command == 'remove':
		parent = Item.get(item.itemId)
		item.itemId = parent.itemId
		bot.editMessageReplyMarkup(reply_markup = inventory_keyboard(user, item.itemId),chat_id=user.id,message_id=query.message.message_id)
		return
	if command == 'put':
		bot.editMessageText(text = 'Куда вы хотите поместить '+item.getName()+'?', reply_markup = put_item_keyboard(user, itemId),chat_id=user.id,message_id=query.message.message_id)			
		return
	if command == 'putconfirm':
		item2Id = int(secondArgument)
		item.itemId = item2Id
		bot.editMessageText(text = 'Ваш инвентарь:', reply_markup = inventory_keyboard(user, item2Id),chat_id=user.id,message_id=query.message.message_id)		
		return
	if command == 'drop':
		bot.editMessageText(text = 'Вы посмотрели свой инвентарь', chat_id=user.id, message_id=query.message.message_id)
		bot.sendMessage(user.id, 'Вы действительно хотите выбросить '+item.getName()+'?', reply_markup = InlineKeyboardMarkup([[
			InlineKeyboardButton('Да', callback_data = 'dropconfirm:'+str(item.id)),
			InlineKeyboardButton('Нет', callback_data = 'actioncancel:'+str(item.id)),
		]]))
	if command == 'dropconfirm':
		back = item.itemId
		item.itemId = 0
		item.drop()

		bot.editMessageText(text = 'Вы выбросили '+item.getName(), chat_id=user.id, message_id=query.message.message_id)
		bot.sendMessage(text = 'Ваш инвентарь:', reply_markup = inventory_keyboard(user, back),chat_id=user.id,message_id=query.message.message_id)
	if command == 'makeaction':
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы посмотрели свой инвентарь', chat_id=user.id, message_id=query.message.message_id)
		if not item.makeAction(secondArgument, bot, user):
			bot.sendMessage(user.id, 'Что-то пошло не так')
		return what_next(bot, user)

	if command == 'actioncancel':
		bot.editMessageText(text = 'Ваш инвентарь:', reply_markup = inventory_keyboard(user, item.itemId),chat_id=user.id,message_id=query.message.message_id)		
		return

	if command == 'close':
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы посмотрели свой инвентарь', chat_id=user.id, message_id=query.message.message_id)
		return what_next(bot, user)

def look_out(bot, update, user):
	loc = user.getLocation()
	text = '*' + loc.getName() + '*\n' + loc.getDescription() + '\n'

	users = list(loc.getUsers())
	if len(users) > 1:
		text += '\nСписок игроков в локации:'
		for u in users:
			text += '\n '+u.name
	else:
		text += '\nКроме вас здесь никого нет'

	text += '\n'

	links = loc.getLinks()
	if (len(links)):
		text += '\nОтсюда можно перейти в следующие локации:'
		for link in links:
			l = Location.get(link)
			text += '\n '+l.getName()
	else:
		text += '\n Отсюда некуда идти'


	items = list(loc.getItems())
	if (len(items)):
		text += '\n\nНа земле лежат следующие предметы:'
		itemsToShow = []
		itemTypes = {}
		i = 0
		for innerItem in items:
			if innerItem.isStackable() and innerItem.protoId in itemTypes:
				pos, count = itemTypes[innerItem.protoId]
				count += 1
				itemsToShow[pos] = innerItem.getName()+' ('+str(count)+')'
			else:
				count = 1
				i += 1
				itemsToShow.append(innerItem.getName())
			itemTypes[innerItem.protoId] = (i-1, count)

		for innerItemName in itemsToShow:
			text += '\n '+innerItemName

	mobs = list(loc.getMobs())
	if (len(mobs)):
		text += '\n\nТак же здесь находятся:'
		for mob in mobs:
			text += '\n '+mob.getName()

	bot.sendMessage(user.id, text, reply_markup = standart_keyboard(user), parse_mode = 'Markdown')	

def change_location_menu(bot, update, user):
	loc = user.getLocation()
	links = loc.getLinks()

	if (len(links)):
		text = 'Отсюда можно перейти в следующие локации:'
		buttons = []
		i = 0
		for link in links:
			l = Location.get(link)

			if update.message.text == l.getName():
				onChangeLocation(bot, user, Location.get(user.locationId), l)
				user.currentState = STATE_JUST_STAYING
				user.locationId = l.id
				bot.sendMessage(user.id, 'Вы переместились в локацию «'+l.getName()+'»', reply_markup = standart_keyboard(user))	
				return

			text += '\n '+l.getName()
			if i % 2:
				buttons[i // 2].append(l.getName())
			else:
				buttons.append([l.getName()])
			i += 1

		buttons.append(['Отмена'])

		if update.message.text == 'Отмена':		
			user.currentState = user.prevState
			return what_next(bot, user)

		if user.currentState != STATE_SELECT_MOVE_TO:
			user.prevState = user.currentState
			user.currentState = STATE_SELECT_MOVE_TO

		bot.sendMessage(user.id, text, reply_markup = create_keyboard(buttons, False))	
	else:
		bot.sendMessage(user.id, 'Отсюда некуда идти', reply_markup = standart_keyboard(user))	

def select_item_to_get_menu(bot, update, user):
	loc = user.getLocation()
	items = []
	itemTypes = {}
	i = 0
	for innerItem in [item for item in loc.getItems() if item.itemId == 0]:
		if innerItem.isStackable() and innerItem.protoId in itemTypes:
			pos, count = itemTypes[innerItem.protoId]
			count += 1
			items[pos] = InlineKeyboardButton(innerItem.getName()+' ('+str(count)+')', callback_data='get:'+str(innerItem.id))
		else:
			count = 1
			i += 1
			items.append(InlineKeyboardButton(innerItem.getName(), callback_data='get:'+str(innerItem.id)))
		itemTypes[innerItem.protoId] = (i-1, count)

	if (len(items)):

		i = 0
		keyboard = []
		for itemButton in items:
			if i % 2:
				keyboard[i // 2].append(itemButton)
			else:
				keyboard.append([itemButton])
			i += 1

		keyboard += [[InlineKeyboardButton('Подобрать всё', callback_data='getall'), InlineKeyboardButton('Отмена', callback_data='cancel')]]

		user.prevState = user.currentState
		user.currentState = STATE_SELECT_ITEM_TO_GET

		bot.sendMessage(user.id, 'Что вы хотите подобрать?', reply_markup = InlineKeyboardMarkup(keyboard))
	else:
		bot.sendMessage(user.id, 'Здесь нечего подбирать', reply_markup = standart_keyboard(user))	

def button_select_item_to_get(bot, update, user):
	query = update.callback_query
	
	ar = query.data.split(':')
	if len(ar) > 1:
		command, itemId = ar[0], int(ar[1])
		item = Item.get(itemId)
	else:
		command = query.data

	if command == 'cancel':
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы не выбрали что подобрать', chat_id=user.id, message_id=query.message.message_id)
		
	if command == 'get':
		item.up(user)
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы подобрали '+item.getName(), chat_id=user.id, message_id=query.message.message_id)
		
	if command == 'getall':
		location = user.getLocation()
		count = 0
		for item in location.getItems():
			item.up(user)
			count += 1

		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы подобрали '+str(count)+' предметов', chat_id=user.id, message_id=query.message.message_id)
		
	return what_next(bot, user)

def look_attributes_keyboard(user):
	genderEmoji = ('👩','👨')[user.gender-1]

	keyboard = [
		[InlineKeyboardButton(''.join([' ' for i in range(0, int((20 - len(user.name))/2))]) + genderEmoji + ' ' + user.name + ''.join([' ' for i in range(0, int((20 - len(user.name))/2))]), callback_data = 'name'), InlineKeyboardButton('Уровень [ '+str(user.level)+' ]', callback_data = 'level'), InlineKeyboardButton(user.race.name, callback_data = 'race')],
		[InlineKeyboardButton('HP: '+str(user.hp)+'/'+str(user.hpMax), callback_data = 'hp'), InlineKeyboardButton(line_bar(user.hp, 0, user.hpMax, '❤️', '_', 100//user.hpMax), callback_data = 'hp')]
	]
	if user.level >= MAX_LEVEL:
		keyboard.append([InlineKeyboardButton('Опыт: '+str(user.exp), callback_data = 'exp')])
	else:
		keyboard.append([InlineKeyboardButton('Опыт: '+str(user.exp)+' / '+str(user.getExpToNextLevel()), callback_data = 'exp'), InlineKeyboardButton(line_bar(user.exp, user.getExpToCurrentLevel(), user.getExpToNextLevel()), callback_data = 'exp')])
	
	lookingMode = get_session_data(user.id, 'lookingAttributesMode')
	if lookingMode == None:
		lookingMode = 1

	if lookingMode == 1:
		keyboard.append([InlineKeyboardButton(' Посмотреть [ Аттрибуты ] / Навыки ', callback_data = 'switch')])

		for attr in ATTRIBUTES_NAMES:
			keyboard.append([InlineKeyboardButton(ATTRIBUTES_NAMES[attr], callback_data=attr), InlineKeyboardButton(str(user.getAttributeValue(attr)), callback_data=attr), InlineKeyboardButton(('Низкий', 'Средний', 'Высокий')[user.getAttributeValue(attr) // 7] , callback_data = attr)])
	else:
		keyboard.append([InlineKeyboardButton(' Посмотреть Аттрибуты / [ Навыки ] ', callback_data = 'switch')])

		for skill in SKILL_NAMES:
			if user.getSkillValue(skill) > 0:
				keyboard.append([InlineKeyboardButton(SKILL_NAMES[skill], callback_data=skill), InlineKeyboardButton(str(int(user.getSkillValue(skill))), callback_data=skill), InlineKeyboardButton(line_bar(user.getSkillValue(skill)*100, int(user.getSkillValue(skill))*100, int(user.getSkillValue(skill)+1)*100), callback_data=skill)])

	if user.pointsLost > 0:
		keyboard.append([InlineKeyboardButton('Улучшить характеристики [ '+str(user.pointsLost)+' ]', callback_data = 'upgrade-attributes')])

	keyboard.append([InlineKeyboardButton('Закрыть', callback_data = 'close')])

	return InlineKeyboardMarkup(keyboard)

def look_attributes(bot, update, user):
	user.prevState = user.currentState
	user.currentState = STATE_LOOKING_ATTRIBUTES
	bot.sendMessage(user.id, 'Это вы:', reply_markup = look_attributes_keyboard(user))

def button_looking_attributes(bot, update, user):
	query = update.callback_query
	command = query.data

	if command == 'upgrade-attributes':
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы посмотрели свои аттрибуты')
		return upgrade_attributes(bot, update, user)

	if command == 'switch':
		lookingMode = get_session_data(user.id, 'lookingAttributesMode')
		if lookingMode == None:
			lookingMode = 1

		if lookingMode == 1:
			newMode = 2
		else:
			newMode = 1
	
		set_session_data(user.id, 'lookingAttributesMode', newMode)
		bot.editMessageReplyMarkup(chat_id = user.id, message_id = query.message.message_id, reply_markup = look_attributes_keyboard(user))
		return

	if command == 'close':
		user.currentState = user.prevState
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы посмотрели свои аттрибуты')
		return what_next(bot, user)




def select_target_for_attack(bot, update, user):
	location = user.getLocation()
	mobs = list(location.getMobs())

	if len(mobs) == 0:
		bot.sendMessage(user.id, 'Здесь некого атаковать', reply_markup = standart_keyboard(user))
		return

	user.prevState = user.currentState
	user.currentState = STATE_SELECT_TARGET_FOR_ATTACK

	keyboard = []
	i = 0
	for mob in mobs:
		button = InlineKeyboardButton(mob.getName(), callback_data = 'attack:'+str(mob.id))
		if i % 2:
			keyboard[i // 2].append(button)
		else:
			keyboard.append([button])
		i += 1
	keyboard.append([InlineKeyboardButton('Отмена', callback_data = 'cancel')])

	bot.sendMessage(user.id, 'Выберите цель для атаки', reply_markup = InlineKeyboardMarkup(keyboard))

ATTACK_KEYBOARD_PAGES = 3
def attack_keyboard(user):

	page = get_session_data(user.id, 'attackKeyboardPage')
	if page == None:
		page = 1

	items = []
	abilities = []

	if page == 1:
		keyboard = [[InlineKeyboardButton('[ Оружие ] / Предметы / Способности', callback_data = 'switch')]]
		items = [item for item in user.items if item.itemId == 0 and item.isWeapon()]
	elif page == 2:
		keyboard = [[InlineKeyboardButton('Оружие / [ Предметы ] / Способности', callback_data = 'switch')]]
		items = [item for item in user.items if item.itemId == 0 and not item.isWeapon()]
	else:
		keyboard = [[InlineKeyboardButton('Оружие / Предметы / [ Способности ]', callback_data = 'switch')]]
		abilities = [load_ability(i) for i in user.getAbilities()]

	itemTypes = {}
	i = 0
	for item in items:
		if item.isStackable() and item.protoId in itemTypes:
			pos, count = itemTypes[item.protoId]
			count += 1

			keyboard[pos][0] = InlineKeyboardButton(item.getName()+' ('+str(count)+')', callback_data = 'item:'+str(item.id))
		else:
			count = 1
			i += 1

			row = [InlineKeyboardButton(item.getName(), callback_data = 'item:'+str(item.id))]
			for method in item.getAttackMethods():
				row.append(InlineKeyboardButton(method, callback_data = 'itemaction:'+str(item.id)+':'+method))
			keyboard.append(row)

		itemTypes[item.protoId] = (i, count)

	if len(abilities):
		naturalAbilitiesRow = len(keyboard)
		keyboard.append([])
		for ability in abilities:
			if (ability.isNatural()):
				keyboard[naturalAbilitiesRow].append(InlineKeyboardButton(ability.name, callback_data = 'ability:'+str(ability.id)))
			else:
				keyboard.append([InlineKeyboardButton(ability.name, callback_data = 'ability:'+str(ability.id))])

	keyboard.append([InlineKeyboardButton('Сбежать', callback_data = 'escape')])

	return InlineKeyboardMarkup(keyboard)

def button_select_target_for_attack(bot, update, user):
	query = update.callback_query
	
	ar = query.data.split(':')
	if len(ar) > 1:
		command, mobId = ar[0], int(ar[1])
		mob = Mob.get(mobId)
	else:
		command = query.data

	if command == 'cancel':
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы не выбрали цель для атаки', chat_id=user.id, message_id=query.message.message_id)
		return what_next(bot, user)

	if command == 'attack':
		user.currentState = STATE_BATTLE
		user.attackMobId = mobId
		bot.editMessageText(text = 'Вы напали на '+mob.getName(), chat_id=user.id, message_id=query.message.message_id)
		mob = user.getAttackedMob()
		if mob:
			bot.sendMessage(user.id, user.name+' [HP:'+str(user.hp)+'/'+str(user.hpMax)+']\nВаш противник: '+mob.getName()+' [HP: '+str(mob.hp)+'/'+str(mob.hpMax)+']', reply_markup = attack_keyboard(user))
		else:
			user.currentState = user.prevState
			return what_next(bot, user)

def attack_menu(bot, update, user):
	mob = user.getAttackedMob()
	if mob:
		bot.sendMessage(user.id, user.name+' [HP:'+str(user.hp)+'/'+str(user.hpMax)+']\nВаш противник: '+mob.getName()+' [HP: '+str(mob.hp)+'/'+str(mob.hpMax)+']. Что вы используете?', reply_markup = attack_keyboard(user))
	else:
		user.currentState = user.prevState
		return what_next(bot, user)


def make_weapon_action(bot, user, mob, item, method):

	if not item.isCanAttack(user, method):
		return 'Вы не можете использовать тип атаки '+method+' у оружия '+item.getName()

	if method == ATTACK_THROW:
		skills = ('throw', 'arch')
	else:
		skills = item.getSkills(method)


	text = []
	flagMobKilled = False

	dices = 1
	if len(skills) == 0:
		text.append('Вы не используете специальных навыков')
	else:
		for skill in skills:
			skillValue = int(user.getSkillValue(skill))
			dices += skillValue
			text.append('Вы используете навык ' + SKILL_NAMES[skill] + ' который у вас равен '+ str(skillValue)+' и добавляете к броску '+str(skillValue)+' дайсов')

	text.append('Вы бросаете '+str(dices)+' дайсов для определения попадания')
	atkValue = 0
	atkDices = []
	for i in range(0,dices):
		val = DiceRoller.roll()
		atkDices.append(str(val))
		atkValue += val
	text.append('🎲 Выпало '+str(atkValue) + ' ('+', '.join(atkDices)+')')
	text.append(mob.getName() + ' пытается уклониться, используя аттрибут '+DX+' который равен '+ str(mob.dx)+' и бросает дайс')
	dxValue = DiceRoller.roll()
	text.append('🎲 Выпало '+str(dxValue)+' (+'+str(mob.dx)+')')
	if atkValue >= mob.dx+dxValue:
		text.append(str(atkValue)+'>='+str(mob.dx+dxValue)+'. Вы попадаете по противнику и используете аттрибут '+ST+' который у вас равен '+str(user.st)+' и бросаете дайс для определения урона')
		dmgValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(dmgValue)+' (+'+str(user.st)+')')
		text.append(mob.getName()+' использует аттрибут '+HT+' который равен '+str(mob.ht)+' и бросает дайс на сопротивление урону')
		htValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(htValue)+' (+'+str(mob.ht)+')')
		if user.st+dmgValue >= mob.ht+htValue:
			damage = item.getDamage(user, method)
			text.append(str(user.st+dmgValue)+'>='+str(mob.ht+htValue)+'. Вы наносите урон противнику. Урон от использования атаки типа '+method+' для предмета '+item.getName()+' равен '+str(damage))
			mob.hp -= damage
			if mob.hp <= 0:
				text.append('\n' + mob.getName() + ' погибает!')
				flagMobKilled = True
		else:
			text.append(str(user.st+dmgValue)+'<'+str(mob.ht+htValue)+'. Вы не наносите урона противнику.')
	else:
		text.append(str(atkValue)+'<'+str(mob.dx+dxValue)+'. Вы не попадаете по противнику')

	if (flagMobKilled):
		mob.afterKill(bot, user)
		mob.destroySelf()

	item.afterAttack(user, method)
	if len(skills):
		for skill in skills:
			skillValue = int(user.getSkillValue(skill))
			user.afterUsingSkill(skill)
			newSkillValue = int(user.getSkillValue(skill))
			if newSkillValue > skillValue:
				text.append("\nВаш навык "+SKILL_NAMES[skill]+" повысился до уровня "+str(newSkillValue))

	return '\n'.join(text)

def make_ability_action(bot, user, mob, ability):

	attr = ability.usingAttribute
	attrValue = user.getAttributeValue(attr)

	skills = ability.usingSkills

	text = []
	flagMobKilled = False

	dices = 1
	if len(skills) == 0:
		text.append('Вы не используете специальных навыков')
	else:
		for skill in skills:
			skillValue = int(user.getSkillValue(skill))
			dices += skillValue
			text.append('Вы используете навык ' + SKILL_NAMES[skill] + ' который у вас равен '+ str(skillValue)+' и добавляете к броску '+str(skillValue)+' дайсов')

	text.append('Вы бросаете '+str(dices)+' дайсов для определения попадания')
	atkValue = 0
	atkDices = []
	for i in range(0,dices):
		val = DiceRoller.roll()
		atkDices.append(str(val))
		atkValue += val
	text.append('🎲 Выпало '+str(atkValue) + ' ('+', '.join(atkDices)+')')
	text.append(mob.getName() + ' пытается уклониться, используя аттрибут '+DX+' который равен '+ str(mob.dx)+' и бросает дайс')
	dxValue = DiceRoller.roll()
	text.append('🎲 Выпало '+str(dxValue)+' (+'+str(mob.dx)+')')
	if atkValue >= mob.dx+dxValue:
		text.append(str(atkValue)+'>='+str(mob.dx+dxValue)+'. Вы попадаете по противнику и используете аттрибут '+ATTRIBUTES_NAMES[attr]+' который у вас равен '+str(attrValue)+' и бросаете дайс для определения урона')
		dmgValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(dmgValue)+' (+'+str(attrValue)+')')
		text.append(mob.getName()+' использует аттрибут '+HT+' который равен '+str(mob.ht)+' и бросает дайс на сопротивление урону')
		htValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(htValue)+' (+'+str(mob.ht)+')')
		if attrValue+dmgValue >= mob.ht+htValue:
			damage = ability.getDamage(user)
			text.append(str(attrValue+dmgValue)+'>='+str(mob.ht+htValue)+'. Вы наносите урон противнику. Урон от использования атаки типа '+ability.name+' равен '+str(damage))
			mob.hp -= damage
			if mob.hp <= 0:
				text.append('\n' + mob.getName() + ' погибает!')
				flagMobKilled = True
		else:
			text.append(str(attrValue+dmgValue)+'<'+str(mob.ht+htValue)+'. Вы не наносите урона противнику.')
	else:
		text.append(str(atkValue)+'<'+str(mob.dx+dxValue)+'. Вы не попадаете по противнику')

	if (flagMobKilled):
		mob.afterKill(bot, user)
		mob.destroySelf()

	ability.afterAttack(user)
	if len(skills):
		for skill in skills:
			skillValue = int(user.getSkillValue(skill))
			user.afterUsingSkill(skill)
			newSkillValue = int(user.getSkillValue(skill))
			if newSkillValue > skillValue:
				text.append("\nВаш навык "+SKILL_NAMES[skill]+" повысился до уровня "+str(newSkillValue))

	return '\n'.join(text)

def make_mob_attack(bot, user, mob):

	abilities = [load_ability(i) for i in mob.getAbilities()]
	items = [Item.get(i) for i in mob.items]

	text = []
	flagUserKilled = False

	bestAbility = (0, 0)
	i = 0
	for ability in abilities:
		dmg = ability.getDamage(mob)
		if dmg > bestAbility[1]:
			bestAbility = (i, dmg)
		i += 1

	# @TODO: добавить использование предметов

	ability = abilities[bestAbility[0]]

	text.append(mob.getName() + ' атакует вас используя способность '+ability.name)

	attr = ability.usingAttribute
	attrValue = mob.getAttributeValue(attr)

	skills = ability.usingSkills

	dices = 1
	if len(skills) == 0:
		text.append(mob.getName()+' не использует специальных навыков')
	else:
		for skill in skills:
			skillValue = int(mob.getSkillValue(skill))
			dices += skillValue
			text.append(mob.getName()+' использует навык ' + SKILL_NAMES[skill] + ' который равен '+ str(skillValue)+' и добавляет к броску '+str(skillValue)+' дайсов')

	text.append(mob.getName()+' бросает '+str(dices)+' дайсов для определения попадания')
	atkValue = 0
	atkDices = []
	for i in range(0,dices):
		val = DiceRoller.roll()
		atkDices.append(str(val))
		atkValue += val
	text.append('🎲 Выпало '+str(atkValue) + ' ('+', '.join(atkDices)+')')
	text.append('Вы пытаетесь уклониться, используя аттрибут '+DX+' который у вас равен '+ str(user.dx)+' и бросаете дайс')
	dxValue = DiceRoller.roll()
	text.append('🎲 Выпало '+str(dxValue)+' (+'+str(user.dx)+')')	
	if atkValue > user.dx+dxValue:
		text.append(str(atkValue)+'>'+str(user.dx+dxValue)+'. '+mob.getName()+' попадает по вам и использует аттрибут '+ATTRIBUTES_NAMES[attr]+' который равен '+str(attrValue)+' и бросает дайс для определения урона')
		dmgValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(dmgValue)+' (+'+str(attrValue)+')')
		text.append('Вы используете аттрибут '+HT+' который у вас равен '+str(user.ht)+' и бросаете дайс на сопротивление урону')
		htValue = DiceRoller.roll()
		text.append('🎲 Выпало '+str(htValue)+' (+'+str(user.ht)+')')
		if attrValue+dmgValue > user.ht+htValue:
			damage = ability.getDamage(mob)
			text.append(str(attrValue+dmgValue)+'>'+str(user.ht+htValue)+'. '+mob.getName()+' наносит вам урон. Урон от использования атаки типа '+ability.name+' равен '+str(damage))
			user.hp -= damage
			if user.hp <= 0:
				text.append('\n' + 'Вы погибли!')
				flagUserKilled = True
		else:
			text.append(str(attrValue+dmgValue)+'<='+str(user.ht+htValue)+'. '+mob.getName()+' не наносит вам урона.')
	else:
		text.append(str(atkValue)+'<='+str(user.dx+dxValue)+'. '+mob.getName()+' не попадает по вам.')
	
	if (flagUserKilled):
		user.afterKill()
		user.destroySelf()
		loadedUsers[user.id] = None
		text.append('\nК сожалению, вы погибли.')

	ability.afterAttack(mob)

	return '\n'.join(text)

def button_battle(bot, update, user):
	query = update.callback_query
	mob = user.getAttackedMob()
	if not mob:
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы пытались кого-то атаковать', chat_id=user.id, message_id=query.message.message_id)
		return what_next(bot, user)

	ar = query.data.split(':')
	if len(ar) > 1:
		command, itemId = ar[0], int(ar[1])
		if len(ar) > 2:
			method = ar[2]
	else:
		command = query.data

	if command == 'switch':
		
		page = get_session_data(user.id, 'attackKeyboardPage')
		if page == None:
			page = 2
		elif page >= ATTACK_KEYBOARD_PAGES:
			page = 1
		else:
			page += 1

		set_session_data(user.id, 'attackKeyboardPage', page)
		bot.editMessageReplyMarkup(chat_id = user.id, message_id= query.message.message_id, reply_markup = attack_keyboard(user))

	if command == 'escape':
		user.currentState = user.prevState
		user.attackMobId = None
		bot.editMessageText(text = 'Вы сбежали от '+mob.getName(), chat_id=user.id, message_id=query.message.message_id)
		return what_next(bot, user)

	if command == 'itemaction':
		item = Item.get(itemId)
		text = make_weapon_action(bot, user, mob, item, method)
		bot.editMessageText(text = 'Вы атаковали '+mob.getName()+' с помощью '+item.getName()+' используя действие '+method, chat_id=user.id, message_id=query.message.message_id)
		if mob.hp > 0:
			text += '\n\n'+make_mob_attack(bot, user, mob)
			bot.sendMessage(user.id, text, reply_markup = create_keyboard())
			if user.hp > 0:
				bot.sendMessage(user.id, user.name+' [HP:'+str(user.hp)+'/'+str(user.hpMax)+']\nВаш противник: '+mob.getName()+' [HP: '+str(mob.hp)+'/'+str(mob.hpMax)+']. Что вы используете?', reply_markup = attack_keyboard(user))
			else:
				bot.sendMessage(user.id, 'Хаха, лузер', reply_markup = create_keyboard([ACTION_RESTART]))
		else:
			user.currentState = user.prevState
			bot.sendMessage(user.id, text, reply_markup = create_keyboard())
			return what_next(bot, user, 'Вы победили '+mob.getName()+'! Что дальше?')

	if command == 'ability':
		ability = load_ability(itemId)
		text = make_ability_action(bot, user, mob, ability)
		bot.editMessageText(text = 'Вы атаковали '+mob.getName()+' используя способность '+ability.name, chat_id=user.id, message_id=query.message.message_id)
		if mob.hp > 0:
			text += '\n\n'+make_mob_attack(bot, user, mob)
			bot.sendMessage(user.id, text, reply_markup = create_keyboard())
			if user.hp > 0:
				bot.sendMessage(user.id, user.name+' [HP:'+str(user.hp)+'/'+str(user.hpMax)+']\nВаш противник: '+mob.getName()+' [HP: '+str(mob.hp)+'/'+str(mob.hpMax)+']. Что вы используете?', reply_markup = attack_keyboard(user))
			else:
				bot.sendMessage(user.id, 'Хаха, лузер', reply_markup = create_keyboard([ACTION_RESTART]))
		else:
			bot.sendMessage(user.id, text, reply_markup = create_keyboard())
			user.currentState = user.prevState
			return what_next(bot, user, 'Вы победили '+mob.getName()+'! Что дальше?')

def select_special_action(bot, update, user):

	if user.currentState != STATE_SELECT_SPECIAL_ACTION:
		user.prevState = user.currentState
		user.currentState = STATE_SELECT_SPECIAL_ACTION

	if update.message.text == SPECIAL_ACTION_BUTCHERING:
		return make_butchering(bot, update, user)
		
	if update.message.text == SPECIAL_ACTION_SAY:
		return make_speaking(bot, update, user)
		
	if update.message.text == ACTION_TRADE:
		return select_shop(bot, update, user)

	if update.message.text == 'Отмена':		
		user.currentState = user.prevState
		return what_next(bot, user)


	actions = [
		[SPECIAL_ACTION_BUTCHERING, SPECIAL_ACTION_SAY],
		['Отмена']
	]

	if (user.getLocation().isCanTrade(user)):
		actions[0].append(ACTION_TRADE)

	bot.sendMessage(user.id, 'Что вы хотите сделать?', reply_markup = create_keyboard(actions, False))


def make_butchering(bot, update, user):
	query = update.callback_query

	butcherableItems = [item for item in user.items if item.isButcherable()]

	if len(butcherableItems) == 0:
		user.currentState = user.prevState
		bot.sendMessage(text = 'У вас нет трупов для разделки', chat_id=user.id, reply_markup = standart_keyboard(user))
		return

	filteredItemsButtons = []

	i = 0
	itemTypes = {}
	for item in butcherableItems:
		if item.isStackable() and item.protoId in itemTypes:
			pos, count = itemTypes[item.protoId]
			count += 1

			filteredItemsButtons[pos] = InlineKeyboardButton(item.getName()+' ('+str(count)+')', callback_data = 'item:'+str(item.id))
		else:
			count = 1
			i += 1

			filteredItemsButtons.append(InlineKeyboardButton(item.getName(), callback_data = 'item:'+str(item.id)))

		itemTypes[item.protoId] = (i-1, count)


	keyboard = []

	i = 0
	for button in filteredItemsButtons:
		if i % 2:
			keyboard[i // 2].append(button)
		else:
			keyboard.append([button])
		i += 1

	keyboard.append([InlineKeyboardButton('Отмена', callback_data = 'cancel')])

	user.currentState = STATE_SELECT_ITEM_FOR_BUTCHERING	
	bot.sendMessage(text = 'Что вы хотите разделать?', chat_id=user.id, reply_markup = InlineKeyboardMarkup(keyboard))

def button_select_item_for_butchering(bot, update, user):
	query = update.callback_query

	ar = query.data.split(':')
	if len(ar) > 1:
		command, itemId = ar[0], int(ar[1])
		item = Item.get(itemId)
	else:
		command = query.data

	if command == 'cancel':
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы не выбрали что разделать', chat_id=user.id, message_id=query.message.message_id)
	
	if command == 'item':
		item.butchering()
		user.currentState = user.prevState
		bot.editMessageText(text = 'Вы разделали '+item.getName(), chat_id=user.id, message_id=query.message.message_id)
		
	return what_next(bot, user)

def make_speaking(bot, update, user):

	if user.currentState != STATE_SPEAKING:
		user.prevState = user.currentState
		user.currentState = STATE_SPEAKING
	elif update.message.text:
		user.currentState = user.prevState
		for currentUser in user.getLocation().getUsers():
			bot.sendMessage(currentUser.id, user.name + ': _' + update.message.text + '_', parse_mode = 'Markdown')
		return what_next(bot, user)

	bot.sendMessage(user.id, 'Что вы хотите сказать?', reply_markup = create_keyboard())

def upgrade_attributes_keyboard(user):

	keyboard = [[InlineKeyboardButton('Очков осталось: '+str(get_session_data(user.id, 'upgradePointsLost')), callback_data = 'header')]]
	
	lookingMode = get_session_data(user.id, 'lookingAttributesMode')
	if lookingMode == None:
		lookingMode = 1

	if lookingMode == 1:
		keyboard.append([InlineKeyboardButton(' Переключить [ Аттрибуты ] / Навыки ', callback_data = 'switch')])

		for attr in ATTRIBUTES_NAMES:
			row = [
				InlineKeyboardButton(ATTRIBUTES_NAMES[attr], callback_data=attr),
				InlineKeyboardButton(MINUS, callback_data=attr+'-'),
				InlineKeyboardButton(str(get_session_data(user.id, 'upgrade'+attr)), callback_data=attr),
				InlineKeyboardButton(PLUS, callback_data=attr+'+')
			]
			if get_session_data(user.id, 'upgrade'+attr) <= user.getAttributeValue(attr):
				row[1] = InlineKeyboardButton(BLOCKED, callback_data=attr)
			keyboard.append(row)

		row = [ 
			InlineKeyboardButton('Макс. HP', callback_data='hpMax'),
			InlineKeyboardButton(MINUS, callback_data='hpMax-'),
			InlineKeyboardButton(str(get_session_data(user.id, 'upgradeHPmax')), callback_data='hpMax'),
			InlineKeyboardButton(PLUS, callback_data='hpMax+')
		]
		if get_session_data(user.id, 'upgradeHPmax') <= user.hpMax:
			row[1] = InlineKeyboardButton(BLOCKED, callback_data='hpMax')
		keyboard.append(row)

	else:
		keyboard.append([InlineKeyboardButton(' Переключить Аттрибуты / [ Навыки ] ', callback_data = 'switch')])
		
		for skill in SKILL_NAMES:
			row = [
				InlineKeyboardButton(SKILL_NAMES[skill], callback_data=skill),
				InlineKeyboardButton(MINUS, callback_data=skill+'-'),
				InlineKeyboardButton(str(get_session_data(user.id, 'upgrade'+skill)), callback_data=skill),
				InlineKeyboardButton(PLUS, callback_data=skill+'+')
			]
			if get_session_data(user.id, 'upgrade'+skill) <= user.getSkillValue(skill):
				row[1] = InlineKeyboardButton(BLOCKED, callback_data=skill)
			keyboard.append(row)

	keyboard.append([InlineKeyboardButton('Готово', callback_data='done')])

	if get_session_data(user.id, 'upgradePointsLost') <= 0:
		for i in range(2,len(keyboard)-1):
			keyboard[i][3] = InlineKeyboardButton(BLOCKED, callback_data='st')

	return InlineKeyboardMarkup(keyboard)

def upgrade_attributes(bot, update, user):

	if user.currentState != STATE_WAITING_UPGRADE_ATTRIBUTES:
		user.prevState = user.currentState
		user.currentState = STATE_WAITING_UPGRADE_ATTRIBUTES

	set_session_data(user.id, 'upgradePointsLost', user.pointsLost)
	set_session_data(user.id, 'upgradeHPmax', user.hpMax)
	for attr in ATTRIBUTES_NAMES:
		set_session_data(user.id, 'upgrade'+attr, user.getAttributeValue(attr))
	for skill in SKILL_NAMES:
		set_session_data(user.id, 'upgrade'+skill, int(user.getSkillValue(skill)))

	bot.sendMessage(user.id, 'Распределите очки по аттрибутам и навыкам', reply_markup = upgrade_attributes_keyboard(user))

def button_upgrade_attributes(bot, update, user):
	query = update.callback_query
	command = query.data

	p = get_session_data(user.id, 'upgradePointsLost')
	hpMax = get_session_data(user.id, 'upgradeHPmax')
	
	attributes = {}
	for attr in ATTRIBUTES_NAMES:
		attributes[attr] = get_session_data(user.id, 'upgrade'+attr)

	skills ={}
	for skill in SKILL_NAMES:
		skills[skill] = get_session_data(user.id, 'upgrade'+skill)

	if command == 'done':
		user.pointsLost = p
		user.hpMax = hpMax

		for attr in attributes:
			user.setAttributeValue(attr, attributes[attr])
		for skill in skills:
			user.setSkillValue(skill, skills[skill])

		user.currentState = user.prevState
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы изменили свои аттрибуты')
		return what_next(bot, user)

	if command == 'switch':
		lookingMode = get_session_data(user.id, 'lookingAttributesMode')
		if lookingMode == None:
			lookingMode = 1

		if lookingMode == 1:
			newMode = 2
		else:
			newMode = 1
	
		set_session_data(user.id, 'lookingAttributesMode', newMode)
		bot.editMessageReplyMarkup(chat_id = user.id, message_id = query.message.message_id, reply_markup = upgrade_attributes_keyboard(user))
		return

	if command[-1::] == '+':
		param = command[:-1:]
		if param == 'hpMax':
			set_session_data(user.id, 'upgradeHPmax', hpMax+1)
		elif param in skills:
			set_session_data(user.id, 'upgrade'+param, skills[param]+1)
		elif param in attributes:
			set_session_data(user.id, 'upgrade'+param, attributes[param]+1)

		set_session_data(user.id, 'upgradePointsLost', p-1)

	if command[-1::] == '-':
		param = command[:-1:]
		if param == 'hpMax':
			set_session_data(user.id, 'upgradeHPmax', hpMax-1)
		elif param in skills:
			set_session_data(user.id, 'upgrade'+param, skills[param]-1)
		elif param in attributes:
			set_session_data(user.id, 'upgrade'+param, attributes[param]-1)

		set_session_data(user.id, 'upgradePointsLost', p+1)

	bot.editMessageReplyMarkup(chat_id = user.id, message_id = query.message.message_id, reply_markup = upgrade_attributes_keyboard(user))

def select_shop(bot, update, user):

	user.currentState = STATE_SELECT_SHOP

	if update.message.text == 'Отмена':
		user.currentState = user.prevState
		return what_next(bot, user)

	keyboard = []
	
	traders = [load_trader(t) for t in user.getLocation().getTraders() if load_trader(t).isCanTrade(user)]
	i = 0
	for trader in traders:

		if update.message.text == trader.name:
			user.currentState = STATE_TRADING
			set_session_data(user.id, 'trader', trader)
			return shop_menu(bot, update, user)

		if i % 2:
			keyboard[i // 2].append(trader.name)
		else:
			keyboard.append([trader.name])
		i += 1

	keyboard.append(['Отмена'])

	bot.sendMessage(user.id, 'С кем вы хотите торговать?', reply_markup = create_keyboard(keyboard, False))


def shop_menu_keyboard(user, trader):

	shopMode = get_session_data(user.id, 'traderShopMode')
	if shopMode == None:
		keyboard = [[InlineKeyboardButton('Купить', callback_data = 'setmode:1'), InlineKeyboardButton('Продать', callback_data = 'setmode:2')]]
		pricelist = []
	elif shopMode == 1:
		keyboard = [[InlineKeyboardButton('Переключить [ Купить ] / Продать', callback_data = 'setmode:2')]]
		pricelist = {}
		traderlist = trader.getSellList(user)
		for i in traderlist:
			pricelist[i] = (load_item_prototype(i).name, traderlist[i])
	elif shopMode == 2:
		keyboard = [[InlineKeyboardButton('Переключить Купить / [ Продать ]', callback_data = 'setmode:1')]]
		pricelist = {}
		traderlist = trader.getBuyList(user)
		for i in traderlist:
			count = user.countItemsByProto(i)
			if count:
				name = load_item_prototype(i).name
				if count > 1:
					name += ' ('+str(count)+')'
				pricelist[i] = (name, traderlist[i])

	if shopMode:
		ACTION = {1:'Купить', 2:'Продать'}[shopMode]
		for protoId in pricelist:
			name, price = pricelist[protoId]
			keyboard.append([
				InlineKeyboardButton(name, callback_data = 'item:'+str(protoId)),
				InlineKeyboardButton(ACTION+' за '+str(price)+MONEY, callback_data = 'trade:'+str(protoId))
			])

	if shopMode == None:
		keyboard.append([InlineKeyboardButton('Закрыть', callback_data = 'close')])
	else:
		keyboard.append([InlineKeyboardButton('Ваши деньги: '+str(user.money)+MONEY, callback_data = 'money'), InlineKeyboardButton('Закрыть', callback_data = 'close')])

	return InlineKeyboardMarkup(keyboard);

def shop_menu(bot, update, user):

	trader = get_session_data(user.id, 'trader')

	if trader == None:
		user.currentState = user.prevState
		return what_next(bot, user)

	bot.sendMessage(user.id, trader.name + ': ' + trader.getHelloMessage(user), reply_markup = shop_menu_keyboard(user, trader))

def button_shop_menu(bot, update, user):
	query = update.callback_query

	ar = query.data.split(':')
	if len(ar) > 1:
		command, param = ar[0], int(ar[1])
	else:
		command = query.data

	trader = get_session_data(user.id, 'trader')

	if trader == None:
		user.currentState = user.prevState
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы пытались торговать, но что-то пошло не так')
		return what_next(bot, user)

	if command == 'close':
		user.currentState = user.prevState
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы торговали с '+trader.name)
		return what_next(bot, user)

	if command == 'setmode':
		set_session_data(user.id, 'traderShopMode', param)
		bot.editMessageReplyMarkup(chat_id = user.id, message_id = query.message.message_id, reply_markup = shop_menu_keyboard(user, trader))
		return

	shopMode = get_session_data(user.id, 'traderShopMode')
	if shopMode == None:
		user.currentState = user.prevState
		bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы пытались торговать, но что-то пошло не так')
		return what_next(bot, user)

	if command == 'trade':
		if shopMode == 1: # юзер покупает у продавца
			price = trader.getSellPrice(user, param)
			if user.money >= price:
				item = Item(protoId = param, userId = user.id)
				user.money -= price
				bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы купили '+item.getName())
			else:
				bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'У вас недостаточно денег для покупки '+load_item_prototype(param).name)
		else: # продавец покупает у юзера
			price = trader.getBuyPrice(user, param)
			if user.removeItem(param):
				user.money += price
				bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Вы продали '+load_item_prototype(param).name)
			else:
				bot.editMessageText(chat_id = user.id, message_id = query.message.message_id, text = 'Что-то пошло не так и вы не смогли продать '+load_item_prototype(param).name)

		bot.sendMessage(user.id, trader.name + ': ' + trader.getHelloMessage(user), reply_markup = shop_menu_keyboard(user, trader))
		return




#
#
#
#

def button(bot, update):
	user = get_user(update.callback_query.message.chat.id)

	if user.currentState == STATE_LOOKING_ATTRIBUTES:
		return button_looking_attributes(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_ATTRIBUTES:
		return button_attributes(bot, update, user)

	if user.currentState == STATE_INVENTORY:
		return button_inventory(bot, update, user)

	if user.currentState == STATE_SELECT_ITEM_TO_GET:
		return button_select_item_to_get(bot, update, user)

	if user.currentState == STATE_SELECT_TARGET_FOR_ATTACK:
		return button_select_target_for_attack(bot, update, user)

	if user.currentState == STATE_BATTLE:
		return button_battle(bot, update, user)

	if user.currentState == STATE_SELECT_ITEM_FOR_BUTCHERING:
		return button_select_item_for_butchering(bot, update, user)

	if user.currentState == STATE_WAITING_UPGRADE_ATTRIBUTES:
		return button_upgrade_attributes(bot, update, user)

	if user.currentState == STATE_TRADING:
		return button_shop_menu(bot, update, user)

def reply(bot, update):
	# print (update)
	user = get_user(update.message.chat.id)


	if user.currentState == STATE_UNREGISTERED:
		return start_message(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_NICK:
		return input_nick(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_RACE:
		return input_race(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_GENDER:
		return input_gender(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_ATTRIBUTES:
		return input_attributes(bot, update, user)

	if user.currentState == STATE_WAITING_INPUT_WEAPON:
		return input_weapon(bot, update, user)

	if user.currentState == STATE_JUST_STARTED:
		user.currentState = STATE_JUST_STAYING
		user.prevState = STATE_JUST_STAYING
		bot.sendMessage(user.id, "Вы находитесь на главной площади Прокреона", reply_markup = standart_keyboard(user))
		return

	if user.currentState == STATE_INVENTORY:
		return open_inventory(bot, update, user)

	if user.currentState == STATE_SELECT_MOVE_TO:
		return change_location_menu(bot, update, user)

	if user.currentState == STATE_SELECT_ITEM_TO_GET:
		return select_item_to_get_menu(bot, update, user)

	if user.currentState == STATE_SELECT_TARGET_FOR_ATTACK:
		return select_target_for_attack(bot, update, user)

	if user.currentState == STATE_BATTLE:
		return attack_menu(bot, update, user)

	if user.currentState == STATE_SELECT_SPECIAL_ACTION:
		return select_special_action(bot, update, user)

	if user.currentState == STATE_SELECT_ITEM_FOR_BUTCHERING:
		return make_butchering(bot, update, user)

	if user.currentState == STATE_SPEAKING:
		return make_speaking(bot, update, user)		

	if user.currentState == STATE_WAITING_UPGRADE_ATTRIBUTES:
		return upgrade_attributes(bot, update, user)

	if user.currentState == STATE_SELECT_SHOP:
		return select_shop(bot, update, user)

	if user.currentState == STATE_TRADING:
		return shop_menu(bot, update, user)



	if update.message.text == ACTION_OPEN_INVENTORY:
		return open_inventory(bot, update, user)		

	if update.message.text == ACTION_LOOK_OUT:
		return look_out(bot, update, user)		

	if update.message.text == ACTION_CHANGE_LOCATION:
		return change_location_menu(bot, update, user)		

	if update.message.text == ACTION_GET_ITEM:
		return select_item_to_get_menu(bot, update, user)		

	if update.message.text == ACTION_LOOK_ATTRIBUTES:
		return look_attributes(bot, update, user)		

	if update.message.text == ACTION_ATTACK:
		return select_target_for_attack(bot, update, user)		

	if update.message.text == ACTION_MAKE_SPECIAL_ACTION:
		return select_special_action(bot, update, user)

	if update.message.text == ACTION_RESTART:
		return start(bot, update)



	bot.sendMessage(user.id, "It was inevitable", reply_markup = standart_keyboard(user))

def onChangeLocation(bot, user, fromLocation, toLocation):
	if toLocation.id == 2:
		rat = Mob.create(protoId = 2, locationId = toLocation.id)
		rat.bite = random.randint(1,7)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('restart', start))
updater.dispatcher.add_handler(CommandHandler('debug', debug))
updater.dispatcher.add_handler(CommandHandler('give', additem))
updater.dispatcher.add_handler(CommandHandler('resetstate', resetstate))
updater.dispatcher.add_handler(CommandHandler('spawn', spawn))
updater.dispatcher.add_handler(CommandHandler('addexp', addexp))
updater.dispatcher.add_handler(MessageHandler([Filters.text], reply))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

try:
	updater.start_polling()
except(KeyboardInterrupt):
	updater.stop()
	quit()