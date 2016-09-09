from consts import *

name = 'Нож'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('knife', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 1
	elif method == ATTACK_THROW:
		return 1
	else:
		return 0
		