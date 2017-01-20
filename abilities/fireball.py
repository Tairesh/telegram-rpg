
name = 'Фаерболл'

usingAttribute = 'iq'
usingSkills = ( 'fire', )

def getDamage(owner):
	return 3

def afterAttack(owner):
	owner.mp -= 1

def isCanAttack(owner):
	return owner.mp >= 1
