from classes import Item

name = 'Человек'

st = 10
dx = 10
iq = 10
ht = 10
hpMax = 10
mpMax = 10

abilities = (1,2,3)

def afterDead(self, bot = None, user = None):
	body = Item(protoId = 101, locationId = self.locationId)
	if bot and user:
		user.addExp(bot, 400)
