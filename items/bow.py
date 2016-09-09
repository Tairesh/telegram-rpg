from consts import *

name = 'Лук'

isWeapon = True
attackMethods = ( ATTACK_FIRE, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_FIRE:
		return ('bow', 'arch')
	else:
		return ('fight', )

def getDamage(self, user, method):
	if method == ATTACK_FIRE:
		for item in user.items:
			if item.protoId == 4:
				return item.getDamage(user, method)
	elif method == ATTACK_THROW:
		return 0
	else:
		return 0

def isCanUseAttackMethod(self, user, method):
	if method == ATTACK_FIRE:
		for item in user.items:
			if item.protoId == 4:
				return True
		return False
	else:
		return True

def afterUsingAttackMethod(self, user, method):
	if method == ATTACK_FIRE:			
		for item in user.items:
			if item.protoId == 4:
				item.itemId = 0
				item.drop()
				return
