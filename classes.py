from sqlobject import *
from consts import *
from prototypesloader import load_item_prototype, load_trader, load_mob_prototype

sqlhub.processConnection = connectionForURI('sqlite:/home/ilya/telegram-rpg/database.sqlite')

class User(SQLObject):
	active = BoolCol(default = 0)
	lastMessage = IntCol(default = 0)
	name = StringCol(default = None)
	raceId = IntCol(default = None)
	gender = IntCol(default = 0)
	level = IntCol(default = 1)
	exp = IntCol(default = 0)
	pointsLost = IntCol(default = 5)
	money = IntCol(default = 100)
	currentState = IntCol(default = 0)
	prevState = IntCol(default = 0)
	st = IntCol(default = 10)
	dx = IntCol(default = 10)
	iq = IntCol(default = 10)
	ht = IntCol(default = 10)
	sword = FloatCol(default = 0)
	bow = FloatCol(default = 0)
	throw = FloatCol(default = 0)
	axe = FloatCol(default = 0)
	crossbow = FloatCol(default = 0)
	hammer = FloatCol(default = 0)
	knife = FloatCol(default = 0)
	mace = FloatCol(default = 0)
	pike = FloatCol(default = 0)
	spear = FloatCol(default = 0)
	lash = FloatCol(default = 0)
	blowgun = FloatCol(default = 0)
	bite = FloatCol(default = 0)
	punch = FloatCol(default = 0)
	kick = FloatCol(default = 0)
	arch = FloatCol(default = 0)
	fight = FloatCol(default = 0)
	dodge = FloatCol(default = 0)
	locationId = IntCol(default = 1)
	hp = IntCol(default = 10)
	hpMax = IntCol(default = 10)
	attackMobId = IntCol(default = None)
	items = MultipleJoin('Item')

	levelsExp = {
		1: 0,
		2: 1000,
		3: 3000,
		4: 5000,
		5: 10000,
		6: 25000,
		7: 50000,
		8: 100000,
		9: 300000,
		10: 700000
	}

	def _init(self, *args, **kw):
		SQLObject._init(self, *args, **kw)
		self.race = load_mob_prototype(self.raceId)

	def addItem(self, protoId, parentId = 0):
		if (parentId):
			item = Item(userId = self.id, protoId = protoId, itemId = parentId)
		else:
			item = Item(userId = self.id, protoId = protoId)
		return item.id

	def removeItem(self, protoId):
		if self.countItemsByProto(protoId):
			item = Item.selectBy(protoId = protoId, userId = self.id)[0]
			for innerItem in item.items:
				innerItem.itemId = item.itemId
			item.destroySelf()
			return True
		else:
			return False

	def getLocation(self):
		return Location.get(self.locationId)

	def getAttackedMob(self):
		if not self.attackMobId:
			return None
		try:
			return Mob.get(self.attackMobId)
		except SQLObjectNotFound:
			self.attackMobId = None
			return None

	def getSkillValue(self, skill):
		return {
			'sword': self.sword,
			'bow': self.bow,
			'throw': self.throw,
			'axe': self.axe,
			'crossbow': self.crossbow,
			'hammer': self.hammer,
			'knife': self.knife,
			'mace': self.mace,
			'pike': self.pike,
			'spear': self.spear,
			'lash': self.lash,
			'blowgun': self.blowgun,
			'bite': self.bite,
			'punch': self.punch,
			'kick': self.kick,
			'arch': self.arch,
			'fight': self.fight,
			'dodge': self.dodge,
		}[skill]

	def afterUsingSkill(self, skill):
		currentValue = int(self.getSkillValue(skill))
		increment = 0.1/(currentValue+1)

		if skill == 'sword':
			self.sword += increment
		elif skill == 'bow':
			self.bow += increment
		elif skill == 'throw':
			self.throw += increment
		elif skill == 'axe':
			self.axe += increment
		elif skill == 'crossbow':
			self.crossbow += increment
		elif skill == 'hammer':
			self.hammer += increment
		elif skill == 'knife':
			self.knife += increment
		elif skill == 'mace':
			self.mace += increment
		elif skill == 'pike':
			self.pike += increment
		elif skill == 'spear':
			self.spear += increment
		elif skill == 'lash':
			self.lash += increment
		elif skill == 'blowgun':
			self.blowgun += increment
		elif skill == 'bite':
			self.bite += increment
		elif skill == 'punch':
			self.punch += increment
		elif skill == 'kick':
			self.kick += increment
		elif skill == 'arch':
			self.arch += increment
		elif skill == 'fight':
			self.fight += increment
		elif skill == 'dodge':
			self.dodge += increment


	def setSkillValue(self, skill, val):
		if skill == 'sword':
			self.sword = val
		elif skill == 'bow':
			self.bow = val
		elif skill == 'throw':
			self.throw = val
		elif skill == 'axe':
			self.axe = val
		elif skill == 'crossbow':
			self.crossbow = val
		elif skill == 'hammer':
			self.hammer = val
		elif skill == 'knife':
			self.knife = val
		elif skill == 'mace':
			self.mace = val
		elif skill == 'pike':
			self.pike = val
		elif skill == 'spear':
			self.spear = val
		elif skill == 'lash':
			self.lash = val
		elif skill == 'blowgun':
			self.blowgun = val
		elif skill == 'bite':
			self.bite = val
		elif skill == 'punch':
			self.punch = val
		elif skill == 'kick':
			self.kick = val
		elif skill == 'arch':
			self.arch = val
		elif skill == 'fight':
			self.fight = val
		elif skill == 'dodge':
			self.dodge = val

	def getAttributeValue(self, attr):
		return {
			'st': self.st,
			'dx': self.dx,
			'iq': self.iq,
			'ht': self.ht
		}[attr]

	def setAttributeValue(self, attr, val):
		if attr == 'st':
			self.st = val
		elif attr == 'dx':
			self.dx = val
		elif attr == 'iq':
			self.iq = val
		elif attr == 'ht':
			self.ht = val

	def getExpToNextLevel(self):
		nextLevel = self.level+1
		if nextLevel > MAX_LEVEL:
			return INFINITY
		return User.levelsExp[nextLevel]

	def getExpToCurrentLevel(self):
		return User.levelsExp[self.level]

	def calcLevel(self):
		level = 0
		for i in User.levelsExp:
			if self.exp >= User.levelsExp[i]:
				level = i
			else:
				break
		self.level = level

	def addExp(self, bot, delta):
		text = ['Вы получаете '+str(delta)+' опыта!']
		level = self.level
		self.exp += delta
		self.calcLevel()
		if self.level > level:
			self.pointsLost += self.level-level
			text.append('Вы достигли уровня '+str(self.level)+'! У вас '+str(self.pointsLost)+' неизрасходованных очков для повышения навыков или аттрибутов')
		bot.sendMessage(self.id, '\n\n'.join(text))

	def countItemsByProto(self, protoId):
		return Item.selectBy(userId = self.id, protoId = protoId).count()

	def getAbilities(self):
		if self.race:
			return self.race.abilities
		else:
			return ()

	def afterKill(self):
		for item in [item for item in self.items if item.itemId == 0]:
			item.drop()
		self.race.afterDead(self)


	def serialize(self):
		return {
			'id': self.id,
			'active': self.active,
			'lastMessage': self.lastMessage,
			'name': self.name,
			'gender': self.gender,
			'level': self.level,
			'exp': self.exp,
			'race': {'id':self.race.id, 'name':self.race.name},
			'pointsLost': self.pointsLost,
			'money': self.money,
			'currentState': self.currentState,
			'prevState': self.prevState,
			'st': self.st,
			'dx': self.dx,
			'iq': self.iq,
			'ht': self.ht,
			'sword': self.sword,
			'bow': self.bow,
			'throw': self.throw,
			'axe': self.axe,
			'crossbow': self.crossbow,
			'hammer': self.hammer,
			'knife': self.knife,
			'mace': self.mace,
			'pike': self.pike,
			'spear': self.spear,
			'lash': self.lash,
			'blowgun': self.blowgun,
			'bite': self.bite,
			'punch': self.punch,
			'kick': self.kick,
			'arch': self.arch,
			'fight': self.fight,
			'dodge': self.dodge,
			'hp': self.hp,
			'hpMax': self.hpMax,
			'locationId': self.locationId,
			'items': [item.serialize() for item in self.items]
		}
		

class Item(SQLObject):
	protoId = IntCol()
	userId = IntCol(default = None)
	locationId = IntCol(default = None)
	mobId = IntCol(default = None)
	itemId = IntCol(default = 0)
	# item = ForeignKey('Item')
	items = MultipleJoin('Item')

	def _init(self, *args, **kw):
		SQLObject._init(self, *args, **kw)
		self.prototype = load_item_prototype(self.protoId)
		# print (self.prototype)

	def getName(self):
		if (self.prototype):
			return self.prototype.name
		return 'Непонятная хуйня'

	def isStackable(self):
		if (self.prototype):
			return self.prototype.isStackable
		return False

	def isContainer(self):
		if (self.prototype):
			return self.prototype.isContainer
		return False

	def getActions(self):
		if (self.prototype):
			return self.prototype.actions
		return [];

	def makeAction(self, action, bot, user):
		if (self.prototype):
			return self.prototype.makeAction(self, action, bot, user)
		return False

	def getSkills(self, method):
		if (self.prototype):
			return self.prototype.getAttackMethodSkills(self, method)
		return ()

	def getAttackMethods(self):
		if (self.prototype):
			return self.prototype.attackMethods + (ATTACK_THROW, )
		else:
			return (ATTACK_THROW, )

	def getDamage(self, user, method):
		if (self.prototype):
			return self.prototype.getDamage(self, user, method)
		return 0

	def isCanAttack(self, user, method):
		if (self.prototype):
			return self.prototype.isCanUseAttackMethod(self, user, method)
		return False

	def afterAttack(self, user, method):
		if method == ATTACK_THROW:
			self.drop()
		if self.prototype:
			self.prototype.afterUsingAttackMethod(self, user, method)

	def isButcherable(self):
		if (self.prototype):
			return self.prototype.isButcherable
		return False

	def getButcheringResults(self):
		if (self.prototype):
			return self.prototype.getButcheringResults(self)
		return ()

	def isWeapon(self):
		if (self.prototype):
			return self.prototype.isWeapon
		return False


	def drop(self):
		if self.userId:
			self.locationId = User.get(self.userId).locationId
			self.userId = None
		if self.mobId:
			self.locationId = Mob.get(self.mobId).locationId
			self.mobId = None

		for item in self.items:
			item.drop()

	def up(self, user):
		self.locationId = None
		self.userId = user.id

		for item in self.items:
			item.up(user)

	def butchering(self):
		for protoId, count in self.getButcheringResults():
			for i in range(0,count):
				Item(protoId = protoId, userId = self.userId, itemId = self.itemId)

		self.destroySelf()

	def serialize(self):
		data = {
			'id': self.id,
			'protoId': self.protoId,
			'name': self.getName()
		}
		if self.isContainer():
			data['items'] = [item.serialize() for item in self.items]
		return data

class Location:
	
	def __init__(self, id):
		self.id = id

	def get(id):
		return LOCATION_CLASSES[id](id)

	def getName(self):
		return 'Хрен знает что такое';

	def getDescription(self):
		return 'Хрен знает что такое';

	def getLinks(self):
		return ()

	def getTraders(self):
		return ()

	def isCanTrade(self, user):
		for t in self.getTraders():
			if load_trader(t).isCanTrade(user):
				return True
		return False

	def getUsers(self):
		return User.selectBy(locationId = self.id)

	def getItems(self):
		return Item.selectBy(locationId = self.id)

	def getMobs(self):
		return Mob.selectBy(locationId = self.id)
		
class MainSquare(Location):

	def getName(self):
		return 'Главная площадь'

	def getDescription(self):
		return 'Главная площадь Прокреона -- столицы империи Тармиан'

	def getLinks(self):
		return (2,3)

class Dungeon(Location):

	def getName(self):
		return 'Подземелья'

	def getDescription(self):
		return 'Мрачные подземелья в которых водятся драконы (а может и нет)'
		
	def getLinks(self):
		return (1,)

class MarketPlace(Location):

	def getName(self):
		return 'Рынок'

	def getDescription(self):
		return 'Вас в спину толкает чья-то рука. Вы тут же оглядываетесь но никого не видите.'

	def getLinks(self):
		return (1,)

	def getTraders(self):
		return (1,2)
		

LOCATION_CLASSES = {
	1: MainSquare,
	2: Dungeon,
	3: MarketPlace
}

class Mob(SQLObject):
	protoId = IntCol()
	locationId = IntCol()
	name = StringCol(default = None)
	st = IntCol(default=10)
	dx = IntCol(default=10)
	ht = IntCol(default=10)
	iq = IntCol(default=10)
	sword = FloatCol(default = 0)
	bow = FloatCol(default = 0)
	throw = FloatCol(default = 0)
	axe = FloatCol(default = 0)
	crossbow = FloatCol(default = 0)
	hammer = FloatCol(default = 0)
	knife = FloatCol(default = 0)
	mace = FloatCol(default = 0)
	pike = FloatCol(default = 0)
	spear = FloatCol(default = 0)
	lash = FloatCol(default = 0)
	blowgun = FloatCol(default = 0)
	bite = FloatCol(default = 0)
	punch = FloatCol(default = 0)
	kick = FloatCol(default = 0)
	arch = FloatCol(default = 0)
	fight = FloatCol(default = 0)
	dodge = FloatCol(default = 0)
	hp = IntCol(default=10)
	hpMax = IntCol(default=10)
	items = MultipleJoin('Item')

	def _init(self, *args, **kw):
		SQLObject._init(self, *args, **kw)
		self.prototype = load_mob_prototype(self.protoId)

	def create(protoId, locationId, name = None):
		mob = Mob(protoId = protoId, locationId = locationId, name = name)		
		mob.st = mob.prototype.st
		mob.dx = mob.prototype.dx
		mob.iq = mob.prototype.iq
		mob.ht = mob.prototype.ht
		mob.hpMax = mob.prototype.hpMax
		mob.hp = mob.hpMax
		return mob

	def getName(self):
		if (self.prototype):
			protoName = self.prototype.name
		else:
			protoName = "Непонятное существо"

		if self.name:
			return self.name + ' (' + protoName.lower() + ')'
		else:
			return protoName

	def addItem(self, protoId, parentId = 0):
		if (parentId):
			item = Item(mobId = self.id, protoId = protoId, itemId = parentId)
		else:
			item = Item(mobId = self.id, protoId = protoId)
		return item.id

	def afterKill(self, bot, user):
		for item in [item for item in self.items if item.itemId == 0]:
			item.drop()
		if (self.prototype):
			self.prototype.afterDead(self, bot, user)

	def getAbilities(self):
		if (self.prototype):
			return self.prototype.abilities
		return ()

	def getAttributeValue(self, attr):
		return {
			'st': self.st,
			'dx': self.dx,
			'iq': self.iq,
			'ht': self.ht
		}[attr]

	def getSkillValue(self, skill):
		return {
			'sword': self.sword,
			'bow': self.bow,
			'throw': self.throw,
			'axe': self.axe,
			'crossbow': self.crossbow,
			'hammer': self.hammer,
			'knife': self.knife,
			'mace': self.mace,
			'pike': self.pike,
			'spear': self.spear,
			'lash': self.lash,
			'blowgun': self.blowgun,
			'bite': self.bite,
			'punch': self.punch,
			'kick': self.kick,
			'arch': self.arch,
			'fight': self.fight,
			'dodge': self.dodge,
		}[skill]
