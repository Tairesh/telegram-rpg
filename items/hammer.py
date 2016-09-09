from consts import *

name = 'Молот'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('hammer', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 2
	elif method == ATTACK_THROW:
		return 1
	else:
		return 0
		