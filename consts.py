from collections import OrderedDict


# consts

STATE_UNREGISTERED = 0
STATE_WAITING_INPUT_NICK = 1
STATE_WAITING_INPUT_RACE = 2
STATE_WAITING_INPUT_GENDER = 3
STATE_WAITING_INPUT_ATTRIBUTES = 4
STATE_WAITING_INPUT_WEAPON = 5
STATE_JUST_STARTED = 6
STATE_JUST_STAYING = 10
STATE_INVENTORY = 11
STATE_SELECT_MOVE_TO = 12
STATE_SELECT_ITEM_TO_GET = 13
STATE_SELECT_TARGET_FOR_ATTACK = 14
STATE_BATTLE = 15
STATE_SELECT_SPECIAL_ACTION = 16
STATE_SELECT_ITEM_FOR_BUTCHERING = 17
STATE_SPEAKING = 18
STATE_WAITING_UPGRADE_ATTRIBUTES = 19
STATE_SELECT_SHOP = 20
STATE_TRADING = 21
STATE_LOOKING_ATTRIBUTES = 22

GENDER_MALE = 'Мужской'
GENDER_MALE_ID = 2
GENDER_FEMALE = 'Женский'
GENDER_FEMALE_ID = 1
GENDER_STICKERS = {2:'BQADAgADQQADOtDfAUsAAWHzKVjo2wI',1:'BQADAgADQwADOtDfARykO07Ho4Z3Ag'}

PLUS = '➕'
MINUS = '➖'
BLOCKED = '🚫'
MONEY = ' 💰'
ST = 'Сила'
DX = 'Ловкость'
IQ = 'Интеллект'
HT = 'Здоровье'

ATTRIBUTES_NAMES = OrderedDict([
	['st', ST],
	['dx', DX],
	['iq', IQ],
	['ht', HT]
])

WEAPON_BOW = 'Лук'
WEAPON_BOW_ID = 2
WEAPON_BOW_SKILL = 'Лук'
WEAPON_SWORD = 'Меч'
WEAPON_SWORD_ID = 1
WEAPON_SWORD_SKILL = 'Меч'
WEAPON_AXE = 'Боевой топор'
WEAPON_AXE_ID = 10
WEAPON_AXE_SKILL = 'Топор'

SKILL_NAMES = OrderedDict([
	['sword', WEAPON_SWORD_SKILL],
	['bow', WEAPON_BOW_SKILL],
	['axe', WEAPON_AXE_SKILL],
	['crossbow', 'Арбалет'],
	['hammer', 'Молот'],
	['knife', 'Нож'],
	['mace', 'Булава'],
	['pike', 'Пика'],
	['spear', 'Копьё'],
	['lash', 'Хлыст'],
	['blowgun', 'Духовая трубка'],
	['throw', 'Метание'],
	['bite', 'Кусание'],
	['punch', 'Кулаки'],
	['kick', 'Пинание'],
	['arch', 'Прицеливание'],
	['fight', 'Рукопашный бой'],
	['dodge', 'Уклонение'],
	['fire', 'Огонь'],
	['water', 'Вода'],
	['air', 'Воздух'],
	['ground', 'Земля'],
	['dark', 'Тьма'],
	['light', 'Свет'],
])

ACTION_OPEN_INVENTORY = 'Открыть инвентарь'
ACTION_LOOK_OUT = 'Оглядеться'
ACTION_CHANGE_LOCATION = 'Переместиться'
ACTION_GET_ITEM = 'Подобрать'
ACTION_LOOK_ATTRIBUTES = 'Посмотреть аттрибуты'
ACTION_ATTACK = 'Атаковать'
ACTION_MAKE_SPECIAL_ACTION = 'Другие действия'
ACTION_TRADE = 'Торговать'
ACTION_RESTART = 'Начать заново'

EAT = 'Съесть'
DRINK = 'Выпить'
READ = 'Прочитать'

SPECIAL_ACTION_BUTCHERING = 'Разделать труп'
SPECIAL_ACTION_SAY = 'Сказать что-то'

ITEM_DROP = 'Выбросить'
ITEM_OPEN = 'Посмотреть'
ITEM_REMOVE = 'Извлечь'
ITEM_PUT = 'Поместить'

ATTACK_THROW = 'Метнуть'
ATTACK_FIRE = 'Выстрелить'
ATTACK_SLASH = 'Ударить'


MAX_LEVEL = 10

INFINITY = 9999999999999999999999999