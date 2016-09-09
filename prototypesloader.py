
import os
import logging
from importlib.machinery import SourceFileLoader

logger = logging.getLogger('rg')

ITEMS_PROTOTYPES_FILES = {
	1: 'sword',
	2: 'bow',
	10: 'axe',
	11: 'hammer',
	12: 'knife',
	13: 'mace',
	14: 'pike',
	15: 'spear',
	16: 'lash',
	17: 'blowgun',
	18: 'crossbow',

	4: 'arrow',
	24: 'bolt',
	34: 'dart',

	3: 'quiver',
	6: 'backpack',

	5: 'worldmap',

	101: 'deadhuman',
	102: 'deadrat',
	103: 'deadelf',
	104: 'deaddwarf',

	201: 'meatrat'
}

def load_item_prototype(id):

	if not id in ITEMS_PROTOTYPES_FILES:
		return None

	name = ITEMS_PROTOTYPES_FILES[id]
	path = 'items/{0}.py'.format(name)

	if not os.path.exists(path):
		return None

	item_loader = SourceFileLoader(name, path)
	item = item_loader.load_module()
	item.id = id

	return check_item_prototype(item, name)

def check_item_prototype(item, name):
	item.code_name = name

	required = ( 'name', )

	for r in required:
		if not hasattr(item, r):
			logger.warn('Item "{0}" has no attribute {1}!'.format(name, r))
			return None

	defaults = [
		( lambda *args: None, ( 'afterUsingAttackMethod', )),
		( lambda *args: 0, ( 'getDamage', )),
		( lambda *args: True, ( 'isCanUseAttackMethod', )),
		( lambda *args: False, ( 'makeAction', )),
		( lambda *args: (), ( 'getAttackMethodSkills', 'getButcheringResults' )),
		( (), ( 'actions', 'attackMethods' )),
		( False, ( 'isStackable', 'isContainer', 'isButcherable', 'isWeapon' ))
	]

	for def_val, names in defaults:
		for name in names:
			if not hasattr(item, name):
				setattr(item, name, def_val)

	return item


ABILITES_FILES = {
	1: 'punch',
	2: 'kick',
	3: 'bite'
}

def load_ability(id):

	if not id in ABILITES_FILES:
		return None

	name = ABILITES_FILES[id]
	path = 'abilities/{0}.py'.format(name)

	if not os.path.exists(path):
		return None

	ability_loader = SourceFileLoader(name, path)
	ability = ability_loader.load_module()
	ability.id = id

	return check_ability(ability, name)

def check_ability(ability, name):
	ability.code_name = name

	required = ( 'name', )

	for r in required:
		if not hasattr(ability, r):
			logger.warn('Ability "{0}" has no attribute {1}!'.format(name, r))
			return None

	defaults = [
		( lambda *args: 0, ( 'getDamage', )),
		( lambda *args: None, ( 'afterAttack', )),
		( None, ( 'usingAttribute', )),
		( (), ( 'usingSkills', )),
		( True, ( 'isNatural', ))
	]

	for def_val, names in defaults:
		for name in names:
			if not hasattr(ability, name):
				setattr(ability, name, def_val)

	return ability


TRADERS_FILES = {
	1: 'weapon',
	2: 'food',
	3: 'cloth'
}

def load_trader(id):

	if not id in TRADERS_FILES:
		return None

	name = TRADERS_FILES[id]
	path = 'traders/{0}.py'.format(name)

	if not os.path.exists(path):
		return None

	trader_loader = SourceFileLoader(name, path)
	trader = trader_loader.load_module()
	trader.id = id

	return check_trader(trader, name)

def traderGetSellPrice(self, user, protoId):
	pricelist = self.getSellList(user)
	if protoId in pricelist:
		return pricelist[protoId]
	else:
		return None

def traderGetBuyPrice(self, user, protoId):
	pricelist = self.getBuyList(user)
	if protoId in pricelist:
		return pricelist[protoId]
	else:
		return None

def check_trader(trader, name):
	trader.code_name = name

	required = ( 'name', )

	for r in required:
		if not hasattr(trader, r):
			logger.warn('Trader "{0}" has no attribute {1}!'.format(name, r))
			return None

	defaults = [
		( lambda *args: (), ( 'getSellList', 'getBuyList' )),
		( lambda *args: True, ( 'isCanTrade', )),
		( lambda *args: 'Что вы хотите продать или купить?', ( 'getHelloMessage', ))
	]

	trader.getSellPrice = lambda user, protoId: traderGetSellPrice(trader, user, protoId)
	trader.getBuyPrice = lambda user, protoId: traderGetBuyPrice(trader, user, protoId)

	for def_val, names in defaults:
		for name in names:
			if not hasattr(trader, name):
				setattr(trader, name, def_val)

	return trader



MOBS_PROTOTYPES_FILES = {
	1: 'human',
	2: 'rat',
	3: 'elf',
	4: 'dwarf'
}

def load_mob_prototype(id):

	if not id in MOBS_PROTOTYPES_FILES:
		return None

	name = MOBS_PROTOTYPES_FILES[id]
	path = 'mobs/{0}.py'.format(name)

	if not os.path.exists(path):
		return None

	mob_loader = SourceFileLoader(name, path)
	mob = mob_loader.load_module()
	mob.id = id

	return check_mob(mob, name)

def check_mob(mob, name):
	mob.code_name = name

	required = ( 'name', 'st', 'dx', 'iq', 'ht', 'hpMax' )

	for r in required:
		if not hasattr(mob, r):
			logger.warn('Mob "{0}" has no attribute {1}!'.format(name, r))
			return None

	defaults = [
		( lambda *args: None, ( 'afterDead', )),
		( (), ( 'abilities', ))
	]

	for def_val, names in defaults:
		for name in names:
			if not hasattr(mob, name):
				setattr(mob, name, def_val)

	return mob