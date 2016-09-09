from consts import *

name = 'Меч'

isWeapon = True
attackMethods = (ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('sword', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 3
	elif method == ATTACK_THROW:
		return 1
	else:
		return 0
