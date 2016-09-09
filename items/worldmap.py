
SHOW_MAP = 'Посмотреть карту'
FILE_ID = 'AgADAgADt6gxGzrQ3wEV6L0WgUKSo6MacQ0ABFC-ghRVr22mzL8BAAEC'

name = 'Карта мира'

isStackable = True

actions = ( SHOW_MAP, )

def makeAction(self, action, bot, user):
	if action == SHOW_MAP:
		bot.sendPhoto(user.id, FILE_ID, 'Карта империи Тармиан и окрестных земель')
		return True

	return False
