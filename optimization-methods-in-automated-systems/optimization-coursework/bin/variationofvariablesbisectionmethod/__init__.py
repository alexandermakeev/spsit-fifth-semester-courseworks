from math import *

class VariationOfVariablesBisectionMethod:
	def __init__(self, y1, y2, a_y1, b_y1, a_y2, b_y2, 
		func='(y1-1)*cos(3.14*(y1**2+y2**2)**.5)', 
		delta=.5, epsilon=.1, step_y1=.05, step_y2=.05):
		self.y1 = y1
		self.y2 = y2
		self.a_y1 = a_y1
		self.b_y1 = b_y1
		self.a_y2 = a_y2
		self.b_y2 = b_y2
		self.func = func
		self.delta = delta
		self.epsilon = epsilon
		self.results = []
		self.step_y1 = abs(step_y1)
		self.step_y2 = abs(step_y2)
		self.n = 0
		self.y1_stop = False
		self.y2_stop = False

		#find direction
		if self.y1 < self.a_y1:
			self.step_y1 = self.step_y1
		elif self.y1 > self.b_y1:
			self.step_y1 = -self.step_y1
		if self.y2 < self.a_y2:
			self.step_y2 = self.step_y2
		elif self.y2 > self.b_y2:
			self.step_y2 = -self.step_y2


		#reach the bounded area
		while True:
			temp = self.y1 + self.step_y1
			if self.a_y1 <= temp <= self.b_y1:
				break
			self.y1 = temp
			self.n += 1
			f = self.get_f(self.y1, self.y2)
			self.results.append([f, self.y1, self.y2, self.n])
		while True:
			temp = self.y2 + self.step_y2
			if self.a_y2 <= temp <= self.b_y2:
				break
			self.y2 = temp
			self.n += 1
			f = self.get_f(self.y1, self.y2)
			self.results.append([f, self.y1, self.y2, self.n])

		#find extrema
		while not self.y1_stop or not self.y2_stop:
			if self.y1_compute():
				self.y1_stop = True
			if self.y2_compute():
				self.y2_stop = True

	def get_f(self, y1, y2):
		return eval(self.func)

	def y1_compute(self):
		x1 = (self.b_y1 - self.a_y1) / 2. - self.delta
		x2 = (self.b_y1 - self.a_y1) / 2. + self.delta
		self.n += 1
		if self.get_f(x1, self.y2) < self.get_f(x2, self.y2):
			self.b_y1 = (self.b_y1 + self.a_y1) / 2.
		else:
			self.a_y1 = (self.b_y1 + self.a_y1) / 2.
		self.y1 = (self.b_y1 + self.a_y1) / 2.
		self.results.append([self.get_f(self.y1, self.y2), self.y1, self.y2, self.n])
		return abs((self.b_y1 - self.a_y1) / 2.) < self.epsilon

	def y2_compute(self):
		x1 = (self.b_y2 - self.a_y2) / 2. - self.delta
		x2 = (self.b_y2 - self.a_y2) / 2. + self.delta
		self.n += 1
		if self.get_f(self.y1, x1) < self.get_f(self.y1, x2):
			self.b_y2 = (self.b_y2 + self.a_y2) / 2.
		else:
			self.a_y2 = (self.b_y2 + self.a_y2) / 2.
		self.y2 = (self.b_y2 + self.a_y2) / 2.
		self.results.append([self.get_f(self.y1, self.y2), self.y1, self.y2, self.n])
		return abs((self.b_y2 - self.a_y2) / 2.) < self.epsilon