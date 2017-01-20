
name = 'Огненный пиздец'

usingAttribute = 'iq'
usingSkills = ( 'fire', )

def getDamage(owner):
	return 10

def afterAttack(owner):
	owner.mp -= 3

def isCanAttack(owner):
	return owner.mp >= 3
