from consts import READ
from classes import Spell

name = 'Свиток заклинания «Огненный пиздец»'

isStackable = True

actions = ( READ, )

def makeAction(self, action, bot, user):
	if action == READ:
		Spell(userId = user.id, protoId = 5)
		self.destroySelf()
		bot.sendMessage(user.id, 'Вы изучили заклинание «Огненный пиздец». К сожалению, свиток сгорел во время обучения.')
		return True

	return False
