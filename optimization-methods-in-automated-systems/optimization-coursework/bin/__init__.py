#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from variationofvariablesbisectionmethod import VariationOfVariablesBisectionMethod

class Main(App):
	def __init__(self, **kwargs):
		super(Main, self).__init__(**kwargs)
		self.textinput_function = TextInput(
			size_hint=(.4, .04),
			pos_hint={'center_x':.25, 'center_y':.8},
			font_size='20sp',
			text='(y1-1)*cos(3.14 * (y1**2+y2**2)**.5)'
			)
		self.textinput_y1 = TextInput(
			hint_text='y1', size_hint=(.04, .04),
			pos_hint={'center_x':.07, 'center_y':.7},
			font_size='20sp',
			text='-1.5'
			)
		self.textinput_y2 = TextInput(
			hint_text='y2', size_hint=(.04, .04),
			pos_hint={'center_x':.11, 'center_y':.7},
			font_size='20sp',
			text='2.5'
			)
		self.textinput_y1_min = TextInput(
			hint_text='y1 min', size_hint=(.04,.04),
			pos_hint={'center_x':.19, 'center_y':.7},
			font_size='20sp',
			text='-3.2'
			)
		self.textinput_y1_max = TextInput(
			hint_text='y1 max', size_hint=(.04,.04),
			pos_hint={'center_x':.23, 'center_y':.7},
			font_size='20sp',
			text='-2.8'
			)
		self.textinput_y2_min = TextInput(
			hint_text='y2 min', size_hint=(.04, .04),
			pos_hint={'center_x':.27, 'center_y':.7},
			font_size='20sp',
			text='-.5'
			)
		self.textinput_y2_max = TextInput(
			hint_text='y2 max', size_hint=(.04, .04),
			pos_hint={'center_x':.31, 'center_y':.7},
			font_size='20sp',
			text='.5'
			)
		self.textinput_y1_step = TextInput(
			hint_text='y1 step', size_hint=(.04, .04),
			pos_hint={'center_x':.39, 'center_y':.7},
			font_size='20sp',
			text='.05'
			)
		self.textinput_y2_step = TextInput(
			hint_text='y2 step', size_hint=(.04, .04),
			pos_hint={'center_x':.43, 'center_y':.7},
			font_size='20sp',
			text='.05'
			)
		self.textinput_delta = TextInput(
			text='.5',
			size_hint=(.2,.04), font_size='20sp',
			pos_hint={'center_x':.15, 'center_y':.6}
			)
		self.textinput_accuracy = TextInput(
			text='.1',
			size_hint=(.2,.04), font_size='20sp',
			pos_hint={'center_x':.35, 'center_y':.6}
			)
		self.label_result = Label(
			pos_hint={'center_x':.25, 'center_y':.4},
			font_size='20sp')

	def on_press_btn_result(self, instance):
		results = VariationOfVariablesBisectionMethod(
				float(self.textinput_y1.text),
				float(self.textinput_y2.text),
				float(self.textinput_y1_min.text),
				float(self.textinput_y1_max.text),
				float(self.textinput_y2_min.text),
				float(self.textinput_y2_max.text),
				func=self.textinput_function.text,
				step_y1=float(self.textinput_y1_step.text),
				step_y2=float(self.textinput_y2_step.text),
				delta=float(self.textinput_delta.text),
				epsilon=float(self.textinput_accuracy.text)
				).results
		self.layout_res.clear_widgets()
		self.label_result.text = 'F = ' + str(results[len(results) -1][0]) + '\nY1 = ' + \
		str(results[len(results) -1][1]) + '\nY2 = ' + str(results[len(results) -1][2]) + \
		'\nN = ' + str(results[len(results) -1][3])
		for res in results:
			for item in res:
				self.layout_res.add_widget(Label(
					text=str(item),
					font_size='18sp'
					))

	def build(self):
		main_layout = FloatLayout()
		label_name = Label(
			text='Метод поочередного варьирования переменных',
			pos_hint={'center_x':.5, 'center_y':.95},
			font_size='22sp')
		label_func = Label(
			text='Функция', pos_hint={'center_x':.25, 'center_y':.85},
			font_size='18sp')
		label_coordinates = Label(
			text='Исходные координаты',
			pos_hint={'center_x':.1, 'center_y':.75},
			font_size='18sp'
			)
		label_area = Label(
			text='Область',
			pos_hint={'center_x':.25, 'center_y':.75},
			font_size='18sp')
		label_steps = Label(
			text='Шаг',
			pos_hint={'center_x':.41, 'center_y':.75},
			font_size='18sp')
		label_delta = Label(
			text='Delta',
			pos_hint={'center_x':.14, 'center_y':.65},
			font_size='18sp')
		label_accuracy = Label(
			text='Точность вычисления целевой функции (Epsilon)',
			pos_hint={'center_x':.34, 'center_y':.65},
			font_size='18sp')
		btn_result = Button(
			text='Результат', size_hint=(.3,.04),
			pos_hint={'center_x':.25, 'center_y':.5},
			font_size='20sp')
		btn_result.bind(on_press=self.on_press_btn_result)

		layout_header_res = GridLayout(
			cols=4,
			pos_hint={'center_x':.75, 'center_y':.9},
			size_hint_x=.4)
		layout_header_res.add_widget(Label(
			text='F', font_size='20sp'))
		layout_header_res.add_widget(Label(
			text='Y1', font_size='20sp'))
		layout_header_res.add_widget(Label(
			text='Y2', font_size='20sp'))
		layout_header_res.add_widget(Label(
			text='N', font_size='20sp'))

		self.layout_res = GridLayout(
			cols=4,
			row_force_default=True,
			row_default_height=25,
			size_hint_y=None)
		self.layout_res.bind(
			minimum_height=self.layout_res.setter('height'))
		scroll_view = ScrollView(
			pos_hint={'center_x':.75, 'center_y':.5},
			size_hint=(.4, .7))
		scroll_view.add_widget(self.layout_res)

		main_layout.add_widget(label_name)
		main_layout.add_widget(label_func)
		main_layout.add_widget(self.textinput_function)
		main_layout.add_widget(label_coordinates)
		main_layout.add_widget(label_area)
		main_layout.add_widget(label_steps)
		main_layout.add_widget(self.textinput_y1)
		main_layout.add_widget(self.textinput_y2)
		main_layout.add_widget(self.textinput_y1_min)
		main_layout.add_widget(self.textinput_y1_max)
		main_layout.add_widget(self.textinput_y2_min)
		main_layout.add_widget(self.textinput_y2_max)
		main_layout.add_widget(self.textinput_y1_step)
		main_layout.add_widget(self.textinput_y2_step)
		main_layout.add_widget(label_delta)
		main_layout.add_widget(label_accuracy)
		main_layout.add_widget(self.textinput_delta)
		main_layout.add_widget(self.textinput_accuracy)
		main_layout.add_widget(btn_result)
		main_layout.add_widget(self.label_result)

		main_layout.add_widget(layout_header_res)
		main_layout.add_widget(scroll_view)
		return main_layout

if __name__ == '__main__':
	Main().run()