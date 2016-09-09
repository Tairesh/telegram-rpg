from consts import *

name = 'Топор'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('axe', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 5
	elif method == ATTACK_THROW:
		return 2
	else:
		return 0
		