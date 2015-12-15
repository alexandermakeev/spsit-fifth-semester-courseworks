import csv

from kivy.uix.textinput import TextInput
from Crypto.Cipher import AES
from hashlib import sha256

class Data:

	def __init__(self, file_data_original):
		self.file_data_original = file_data_original
		self.IV = 16 * '\x00'
		self.mode = AES.MODE_CFB
		self.expense = []
		self.levels = []
		self.concentration = []
		with open(file_data_original, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.expense.append(row[0])
				self.levels.append(row[1])
				self.concentration.append(row[2])

	def get_expense(self):
		return [TextInput(text=item, font_size='18sp', background_color=[.25,.25,.25, 1], 
			cursor_color=[1,1,1,1], hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]) for item in self.expense]

	def get_levels(self):
		return [TextInput(text=item, font_size='18sp', background_color=[.25,.25,.25, 1], 
			cursor_color=[1,1,1,1], hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]) for item in self.levels]

	def get_concentration(self):
		return [TextInput(text=item, font_size='18sp', background_color=[.25,.25,.25, 1], 
			cursor_color=[1,1,1,1], hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]) for item in self.concentration]

	def encrypt_text(self, data, password):
		key = sha256(password).digest()
		encryptor = AES.new(key, self.mode, IV=self.IV)
		return encryptor.encrypt(data)

	def decrypt_text(self, ciphertext, password):
		key = sha256(password).digest()
		decryptor = AES.new(key, self.mode, IV=self.IV)
		return decryptor.decrypt(ciphertext)

	def encrypt_file(self, plain, path, password):
		ciphertext = self.encrypt_text(plain, password)
		f = open(path, 'w')
		f.write(ciphertext)
		f.close()

	def decrypt_file(self, path, password):
		f = open(path, 'r')
		ciphertext = f.read()
		f.close()
		return self.decrypt_text(ciphertext, password)

	def read(self, path, password):
		plain = self.decrypt_file(path, password)
		self.expense = []
		self.levels = []
		self.concentration = []
		try:
			for line in plain.split('\n'):
				if line == '':
					continue
				items = line.split(',')
				self.expense.append(items[0])
				self.levels.append(items[1])
				self.concentration.append(items[2])
			return True
		except IndexError:
			return False

	def save(self, path, password, expense, levels, concentration):
		plain = ''	
		for i in range(len(expense)):
			plain += expense[i].text + ',' + levels[i].text + ',' + concentration[i].text + '\n'
		self.encrypt_file(plain, path, password)