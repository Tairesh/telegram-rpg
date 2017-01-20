from consts import DRINK

name = 'Бутылочка с синим зельем'

isStackable = True

actions = ( DRINK, )

def makeAction(self, action, bot, user):
	if action == DRINK:
		user.mp = user.mpMax
		self.protoId = 50
		bot.sendMessage(user.id, 'Вы выпили синее зелье. Ваша мана полностью восстановлена.')
		return True

	return False
