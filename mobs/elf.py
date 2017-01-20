from classes import Item

name = 'Эльф'

st = 7
dx = 13
iq = 12
ht = 8
hpMax = 10
mpMax = 15

abilities = (1,2,3)

def afterDead(self, bot = None, user = None):
	body = Item(protoId = 103, locationId = self.locationId)
	if bot and user:
		user.addExp(bot, 300)
