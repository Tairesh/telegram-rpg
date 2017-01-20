from classes import Item

name = 'Дварф'

st = 15
dx = 2
iq = 5
ht = 15
hpMax = 15
mpMax = 10

abilities = (1,2,3)

def afterDead(self, bot = None, user = None):
	body = Item(protoId = 104, locationId = self.locationId)
	if bot and user:
		user.addExp(bot, 500)
