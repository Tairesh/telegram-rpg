from consts import *

name = 'Копьё'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('spear', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 3
	elif method == ATTACK_THROW:
		return 2
	else:
		return 0
		