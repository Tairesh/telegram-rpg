from consts import DRINK

name = 'Бутылочка с красным зельем'

isStackable = True

actions = ( DRINK, )

def makeAction(self, action, bot, user):
	if action == DRINK:
		user.hp = user.hpMax
		self.protoId = 50
		bot.sendMessage(user.id, 'Вы выпили красное зелье. Ваше здоровье полностью восстановлено.')
		return True

	return False
