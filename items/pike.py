from consts import *

name = 'Пика'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('pike', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 2
	elif method == ATTACK_THROW:
		return 2
	else:
		return 0
		