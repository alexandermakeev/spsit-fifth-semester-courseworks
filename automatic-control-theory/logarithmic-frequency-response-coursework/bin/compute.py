from math import log, atan, pi
from enum import Enum
from type import Type

class Compute:
	def __init__(self, w, k=1.):
		self.w = w
		self.k = k
		self.units = []
		self.frequency_points = []
		for item in w:
			try:
				temp = item[1].index('s**2')
				a = float(item[1][:temp])
				item[1] = item[1][temp+4:]
			except ValueError:
				a = 0
			temp = item[1].index('s')
			b = float(item[1][:temp])
			try:
				temp = item[1].rindex('+')
			except ValueError:
				temp = item[1].rindex('-')
			c = float(item[1][temp:])
			a = a / abs(c)
			b = b / abs(c)
			if item[0]:
				self.k /= abs(c)
				if a == 0:
					t = b
					type = Type.aperiodic_first_order
				else:
					t = a ** .5
					type = Type.oscillatory
			else:
				self.k *= abs(c)
				if a == 0:
					t = b
					type = Type.forsing_first_order
				else:
					t = a ** .5
					type = Type.forsing_second_order
			c = c / abs(c)
			if item[0]:
				self.units.append([True, a, b, c])
			else:
				self.units.append([False, a, b, c])
			lg = round(log(1./t, 10), 2)
			self.frequency_points.append([lg, type])
		self.frequency_points.sort(key=lambda x: x[0])

	def get_fi(self, omega):
		fi = -90
		for unit in self.units:
			if unit[0]:
				fi -= atan((unit[2] * omega)/(unit[1] * omega ** 2 + unit[3])) * (180/pi)
			else:
				fi += atan((unit[2] * omega)/(unit[1] * omega ** 2 + unit[3])) * (180/pi)
		return fi