from random import randint

class DiceRoller:

	def roll(count = 1, value = 20):
		if count == 1:
			return randint(1,value)
		else:
			result = 0
			for i in range(0,count):
				result += randint(1,value)
			return result