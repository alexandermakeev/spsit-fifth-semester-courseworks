#!/usr/bin/env python

# -*- coding: utf-8 -*-

from math import log
from time import sleep
from random import uniform

from type import Type
from compute import Compute
from graph import Graph, MeshLinePlot, LinePlot

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')


class Main(App):

	def __init__(self, **kwargs):
		super(Main, self).__init__(**kwargs)

		self.screen_manager = ScreenManager()
		self.input_screen = Screen(name='input')
		self.plot_screen = Screen(name='plot')

		
		self.main = FloatLayout()
		self.main.add_widget(Label(text='Logarithmic frequency response', 
			pos_hint={'center_x':.5,'center_y':.93},
			font_size='20sp'))
		self.main.add_widget(Label(text='Logarithmic phase response', 
			pos_hint={'center_x':.5,'center_y':.46},
			font_size='20sp'))
		self.frequency_graph = Graph(
			xlabel='lg w', ylabel='20lgA', 
			x_ticks_minor=5, x_ticks_major=.2, 
			y_ticks_major=10, y_grid_label=True, 
			x_grid_label=True, padding=10,
			x_grid=True, y_grid=True, 
			xmin=-1, xmax=1, 
			ymin=-40, ymax=40, 
			size_hint=(1,.45), 
			pos_hint={'center_x':.5,'center_y':.7})
		self.phase_graph = Graph(
			xlabel='delta f', ylabel='f(w)', 
			x_ticks_minor=5, x_ticks_major=.2, 
			y_ticks_major=45,
			y_grid_label=True, x_grid_label=True, 
			padding=10, x_grid=True, y_grid=True, 
			xmin=-1, xmax=1, 
			ymin=-270, ymax=90, 
			size_hint=(1,.45),
			pos_hint={'center_x':.5,'center_y':.225})
		self.main.add_widget(self.frequency_graph)
		self.main.add_widget(self.phase_graph)
		back_btn = Button(text='Back', size_hint=(.2,.04), pos_hint={'center_x':.2,'center_y':.95})
		back_btn.bind(on_press=lambda x: self.go_to_input_screen(self.main))
		self.main.add_widget(back_btn)

		plot = MeshLinePlot(
			color=[.866666667, .866666667, .866666667, .7])
		plot.points = [(0, -40), (0, 40)]
		self.frequency_graph.add_plot(plot)

		self.plot_screen.add_widget(self.main)

		self.frequency_points = []
		self.phase_points = []
		self.numerator = []
		self.denominator = []

		self.performance = []

		self.max_performance_label = Label(pos_hint={'center_x':.8,'center_y':.95}, font_size='20sp')
		self.main.add_widget(self.max_performance_label)

		self.k = TextInput(
			text='1', 
			hint_text='k', 
			size_hint=(.04, .04), 
			pos_hint={'center_x':.15, 'center_y':.7}, 
			font_size='22sp'
			)

		for i in range(7):
			if i == 0:
				self.numerator.append(
					TextInput(
						text='15s+5', 
						size_hint=(.1, .04), font_size='22sp',
						pos_hint={'center_x':.225, 'center_y':.725})
					)
				self.denominator.append(
					TextInput(
						text='30s+3', 
						size_hint=(.1, .04), font_size='22sp',
						pos_hint={'center_x':.225, 'center_y':.675})
					)
			elif i == 1:
				self.numerator.append(
					TextInput(
						text='30s-30',
						size_hint=(.1, .04), font_size='22sp',
						pos_hint={'center_x':.225+i/9.8, 'center_y':.725})
					)
				self.denominator.append(
					TextInput(
						text='.45s**2+2.4s+5',
						size_hint=(.1, .04), font_size='22sp',
						pos_hint={'center_x':.225+i/9.8, 'center_y':.675})
					)
			else:
				self.numerator.append(
					TextInput(
						size_hint=(.1, .04),
						pos_hint={'center_x':.225+i/9.8, 'center_y':725}, 
						font_size='22sp')
					)
				self.denominator.append(
					TextInput(
						size_hint=(.1, .04), 
						pos_hint={'center_x':.225+i/9.8, 'center_y':675}, 
						font_size='22sp')
					)

	def draw_max_performance(self):
		self.max_performance_label.text = 'Max cut-off frequency (W c) is %f' % max(self.performance)

	def go_to_input_screen(self, main):
		self.frequency_points = []
		self.phase_points = []
		self.screen_manager.current = 'input'

	def go_to_plot_screen(self):
		self.color_a = uniform(0, 1)
		self.color_b = uniform(0, 1)
		self.color_c = uniform(0, 1)
		self.plot_layout()
		self.screen_manager.current = 'plot'

	def get_a(self, x1,y1,x2,y2):
		return (y2-y1)/(x2-x1)

	def get_b(self, x1,y1,x2,y2):
		return (x2*y1-x1*y2)/(x2-x1)

	def add_new_points(self):
		w = []
		for item in self.numerator:
			if item.text != '':
				w.append([False, item.text])
		for item in self.denominator:
			if item.text != '':
				w.append([True, item.text])
		k = float(self.k.text)
		t = .1
		c = Compute(w,k=k)
		values = c.frequency
		n = log(c.k, 10.0)
		k = 20 * n
		xmin = values[0][0] - 1.0
		xmax = values[len(values) - 1][0] + 3.0
		ymin = - k * 1.5
		ymax = k * 1.5 + .1

	def plot_layout(self):
		w = []
		for item in self.numerator:
			if item.text != '':
				w.append([False, item.text])
		for item in self.denominator:
			if item.text != '':
				w.append([True, item.text])
		k = float(self.k.text)
		t = .1
		c = Compute(w,k=k)
		values = c.frequency_points
		n = log(c.k, 10.0)
		k = 20 * n
		xmin = values[0][0] - 1.0
		xmax = values[len(values) - 1][0] + 3.0
		ymin = - k * 1.5
		ymax = k * 1.5 + .1

		if xmin < self.frequency_graph.xmin:
			self.frequency_graph.xmin = xmin
			self.phase_graph.xmin = xmin
		if xmax > self.frequency_graph.xmin:
			self.frequency_graph.xmax = xmax
			self.phase_graph.xmax = xmax
		
		
		plot = MeshLinePlot(
			color=[.866666667, .866666667, .866666667, .7])
		plot.points = [(xmin, 0), (xmax, 0)]
		self.frequency_graph.add_plot(plot)

		for item in values:
			plot = LinePlot(
				line_width=1, color=[.38, .67, .54, 1])
			plot.points = [(item[0], -40), (item[0], 40)]
			self.frequency_graph.add_plot(plot)
		frequency_plot = LinePlot(
			line_width=2, color=[self.color_a, self.color_b, self.color_c, 1])
		points = []
		points.append([xmin, k])
		points.append([values[0][0], k])
		self.frequency_graph.add_plot(frequency_plot)

		incline = 0
		current_ordinate = k

		for i in range(len(values)):
			incline = incline + values[i][1].value
			if i != len(values) - 1:
				current_ordinate = current_ordinate + incline * (values[i+1][0] - values[i][0])
				points.append([values[i + 1][0], current_ordinate])
			else:
				points.append([values[i][0] + 3, incline])

		for i in range(len(points) - 1):
			a = self.get_a(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
			b = self.get_b(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
			for i in range(int(points[i][0] * 100), int(points[i + 1][0] * 100)):
				self.frequency_points.append([i / 100., a * (i / 100.) + b])

		

		for i in range(-180, 90, 90):
			phase_plot = LinePlot(
				line_width=1, color=[.93, .46, 0, .7])
			phase_plot.points = [(xmin, i), (xmax, i)]
			self.phase_graph.add_plot(phase_plot)

		phase_plot = LinePlot(
			line_width=2, color=[self.color_a, self.color_b, self.color_c, 1])
		for i in range(int(xmin * 100), int(xmax * 100), 1):
			self.phase_points.append([i / 100., c.get_fi(i / 100.)])

		self.phase_graph.add_plot(phase_plot)
		Clock.schedule_once(lambda x: self.draw_phase(phase_plot), .5)
		Clock.schedule_once(lambda x: self.draw_frequency(frequency_plot), .5)

	def draw_frequency(self, plot):
		if len(self.frequency_points) == 0:
			self.performance.append(self.temp)
			self.draw_max_performance()
			return
		if int(self.frequency_points[0][1]) == 0:
			self.temp = self.frequency_points[0][0]
		plot.points = plot.points + [(self.frequency_points[0][0], self.frequency_points[0][1])]
		del self.frequency_points[0]
		Clock.schedule_once(lambda x: self.draw_frequency(plot))

	def draw_phase(self, plot):
		if len(self.phase_points) == 0:
			return
		plot.points = plot.points + [(self.phase_points[0][0], self.phase_points[0][1])]
		del self.phase_points[0]
		Clock.schedule_once(lambda x: self.draw_phase(plot))

	def input_layout(self):
		layout = FloatLayout()
		layout.add_widget(Label(text='W(s) = ', pos_hint={'center_x':.1, 'center_y':.7}, font_size='30sp'))
		layout.add_widget(self.k)

		add_to_numerator_btn = Button(text='Add new W to numerator', size_hint=(.15, .05), pos_hint={'center_x':.2, 'center_y':.25})
		add_to_numerator_btn.bind(on_press=lambda x: self.add_widget_to_numerator())
		remove_from_numerator_btn = Button(text='Remove last from numerator', size_hint=(.15, .05), pos_hint={'center_x':.2, 'center_y':.19})
		remove_from_numerator_btn.bind(on_press=lambda x: self.remove_widget_from_numerator())
		layout.add_widget(add_to_numerator_btn)
		layout.add_widget(remove_from_numerator_btn)

		add_to_denominator_btn = Button(text='Add new W to denominator', size_hint=(.15, .05), pos_hint={'center_x':.36, 'center_y':.25})
		add_to_denominator_btn.bind(on_press=lambda x: self.add_widget_to_denominator())
		remove_from_denominator_btn = Button(text='Remove last from denominator', size_hint=(.15, .05), pos_hint={'center_x':.36, 'center_y':.19})
		remove_from_denominator_btn.bind(on_press=lambda x: self.remove_widget_from_denominator())
		layout.add_widget(add_to_denominator_btn)
		layout.add_widget(remove_from_denominator_btn)

		continue_btn = Button(text='Continue', size_hint=(.15, .11), pos_hint={'center_x':.52, 'center_y':.22})
		continue_btn.bind(on_press=lambda x: self.go_to_plot_screen())
		layout.add_widget(continue_btn)

		for item in self.numerator:
			layout.add_widget(item)
		for item in self.denominator:
			layout.add_widget(item)
		return layout
	
	def build(self):
		self.input_screen.add_widget(self.input_layout())
		self.screen_manager.add_widget(self.input_screen)
		self.screen_manager.add_widget(self.plot_screen)
		return self.screen_manager

	def add_widget_to_numerator(self):
		for item in self.numerator:
			if item.pos_hint['center_y'] != .725:
				item.pos_hint = {'center_y':.725}
				return

	def add_widget_to_denominator(self):
		for item in self.denominator:
			if item.pos_hint['center_y'] != .675:
				item.pos_hint = {'center_y':.675}
				return

	def remove_widget_from_numerator(self):
		for item in reversed(self.numerator):
			if item.pos_hint['center_y'] != 725:
				item.pos_hint = {'center_y':725}
				item.text = ''
				return

	def remove_widget_from_denominator(self):
		for item in reversed(self.denominator):
			if item.pos_hint['center_y'] != 675:
				item.pos_hint = {'center_y':675}
				item.text = ''
				return

if __name__ == '__main__':
	Main().run()