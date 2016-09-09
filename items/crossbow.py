from consts import *

name = 'Арбалет'

isWeapon = True

attackMethods = ( ATTACK_SLASH, ATTACK_FIRE )

def getAttackMethodSkills(self, method):
	if method == ATTACK_FIRE:
		return ('crossbow', 'arch')
	if method == ATTACK_SLASH:
		return ('hammer', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_FIRE:
		for item in user.items:
			if item.protoId == 24:
				return item.getDamage(user, method)
	elif method == ATTACK_THROW:
		return 0
	else:
		return 0

def isCanUseAttackMethod(self, user, method):
	if method == ATTACK_FIRE:
		for item in user.items:
			if item.protoId == 24:
				return True
		return False
	else:
		return True

def afterUsingAttackMethod(self, user, method):
	if method == ATTACK_FIRE:			
		for item in user.items:
			if item.protoId == 24:
				item.itemId = 0
				item.drop()
				return
				