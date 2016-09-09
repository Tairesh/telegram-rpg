from consts import *

name = 'Хлыст'

isWeapon = True

attackMethods = ( ATTACK_SLASH, )

def getAttackMethodSkills(self, method):
	if method == ATTACK_SLASH:
		return ('lash', 'fight')
	else:
		return ()

def getDamage(self, user, method):
	if method == ATTACK_SLASH:
		return 1
	else:
		return 0
		