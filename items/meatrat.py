from consts import EAT

name = 'Мясо крысы'

isStackable = True

actions = ( EAT, )

def makeAction(self, action, bot, user):
	if action == EAT:
		if user.hp + 1 <= user.hpMax:
			user.hp += 1
			self.destroySelf()
			bot.sendMessage(user.id, 'Вы съели мясо крысы. Ну и гадость же!')
			return True

	return False
