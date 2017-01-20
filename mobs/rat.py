from classes import Item

name = 'Крыса'

st = 3
dx = 15
iq = 0
ht = 5
hpMax = 2
mpMax = 0

abilities = (3, )

def afterDead(self, bot, user):
	body = Item(protoId = 102, locationId = self.locationId)
	user.addExp(bot, 50)
