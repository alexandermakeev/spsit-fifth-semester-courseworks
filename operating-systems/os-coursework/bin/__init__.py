#!/usr/bin/env python
# -*- coding: utf-8 -*

from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.uix.widget import Widget

from data import Data
from configuration import Configuration
from graph import Graph, MeshLinePlot, LinePlot
from moretransitions import PixelTransition, RippleTransition, BlurTransition, RVBTransition
from filechooserthumbview import FileChooserThumbView
from desktopvideoplayer import DesktopVideoPlayer
from modernmenu import MenuSpawner
from oosheet import OOSheet
from subprocess import Popen, PIPE

class PlotTouchListener(Widget):
	def __init__(self, plot, scaling_down, scaling_up, **kwargs):
		super(PlotTouchListener, self).__init__(**kwargs)
		self.plot = plot
		self.scaling_down = scaling_down
		self.scaling_up = scaling_up
	def on_touch_up(self, touch):
		if touch.button == 'scrollup':
			self.plot.xmin = self.plot.xmin * self.scaling_down
			self.plot.xmax = self.plot.xmax * self.scaling_up
			self.plot.ymin = self.plot.ymin * self.scaling_down
			self.plot.ymax = self.plot.ymax * self.scaling_up
		elif touch.button == 'scrolldown':
			self.plot.xmin = self.plot.xmin * self.scaling_up
			self.plot.xmax = self.plot.xmax * self.scaling_down
			self.plot.ymin = self.plot.ymin * self.scaling_up
			self.plot.ymax = self.plot.ymax * self.scaling_down

class Main(App):

	data = Data('data_original')
	configuration = Configuration('main.cfg')
	Popen(['sh', 'openoffice.sh'], shell=False, stdout=PIPE, stderr=PIPE)
	
	expense_text_input = data.get_expense()
	levels_text_input = data.get_levels()
	concentration_text_input = data.get_concentration()

	screen_manager = ScreenManager(transition=RippleTransition(
		duration=configuration.screen_manager_transition_duration))
	home_screen = Screen(name='home')
	levels_plot_screen = Screen(name='levels_plot')
	concentration_plot_screen = Screen(name='concentration_plot')
	video_player_screen = Screen(name='video_player')
	video_file_screen = Screen(name='load_video_file')
	reference_screen = Screen(name='reference')
	load_data_screen = Screen(name='load_data')
	save_data_screen = Screen(name='save_data')
	save_record_screen = Screen(name='save_record')

	video_player = DesktopVideoPlayer( 
		size_hint=(1, .9),
		pos_hint={'center_x':.5, 'center_y':.5}, auto_play=False)
	video_player.source = configuration.video_path

	scaling_down = float(configuration.plot_scalling_down)
	scaling_up = float(configuration.plot_scalling_up)

	def update(self):
		self.expense_text_input = self.data.get_expense()
		self.levels_text_input = self.data.get_levels()
		self.concentration_text_input = self.data.get_concentration()
		self.home_screen.clear_widgets()
		self.home_screen.add_widget(self.home_layout())

	def update_plots(self):
		self.levels_plot_screen.clear_widgets()
		self.concentration_plot_screen.clear_widgets()
		self.levels_plot_screen.add_widget(self.levels_plot_layout())
		self.concentration_plot_screen.add_widget(self.concentration_plot_layout())

	def go_to_levels_plot_screen(self, *args):
		args[0].parent.dismiss()
		self.update_plots()
		self.screen_manager.current = 'levels_plot'

	def go_to_concentration_plot_screen(self, *args):
		args[0].parent.dismiss()
		self.update_plots()
		self.screen_manager.current = 'concentration_plot'

	def go_to_home_screen(self):
		self.screen_manager.current = 'home'

	def go_to_video_player_screen(self, *args):
		if len(args) != 0:
			args[0].parent.dismiss()
		self.screen_manager.current = 'video_player'
		self.video_player.toggle_video()

	def go_to_video_file_screen(self):
		self.screen_manager.current = 'load_video_file'
		self.video_player.toggle_video()

	def go_to_reference_screen(self, *args):
		args[0].parent.dismiss()
		self.screen_manager.current = 'reference'

	def go_to_load_data_screen(self, *args):
		args[0].parent.dismiss()
		self.screen_manager.current = 'load_data'

	def go_to_save_data_screen(self, *args):
		args[0].parent.dismiss()
		self.screen_manager.current = 'save_data'

	def go_to_save_record_screen(self):
		self.screen_manager.current = 'save_record'

	def on_press_select_video_file_btn(self, selection):
		if len(selection) != 0:
			self.video_player.source = selection[0]
			self.go_to_video_player_screen()

	def on_press_restore_data_btn(self):
		self.data = Data('data_original')
		self.update()
		self.go_to_home_screen()

	def on_press_add_new_value_btn(self):
		self.expense_text_input.append(TextInput(text=str(int(self.expense_text_input[len(self.expense_text_input)-1].text)+1), 
			font_size='18sp', background_color=[.25,.25,.25, 1], cursor_color=[1,1,1,1],
			hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]))
		self.levels_text_input.append(TextInput(text=str(0), font_size='18sp', 
			background_color=[.25,.25,.25, 1], cursor_color=[1,1,1,1],
			hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]))
		self.concentration_text_input.append(TextInput(text=str(0), font_size='18sp', 
			background_color=[.25,.25,.25, 1], cursor_color=[1,1,1,1],
			hint_text_color=[.7,.7,.7,1], foreground_color=[1,1,1,1]))
		self.home_grid_layout.add_widget(self.expense_text_input[len(self.expense_text_input)-1])
		self.home_grid_layout.add_widget(self.levels_text_input[len(self.levels_text_input)-1])
		self.home_grid_layout.add_widget(self.concentration_text_input[len(self.concentration_text_input)-1])

	def on_press_make_record(self, *args):
		args[0].parent.dismiss()
		for i in range(len(self.expense_text_input)):
			OOSheet('a' + str(i + 1)).value = self.expense_text_input[i].text
			OOSheet('b' + str(i + 1)).value = self.levels_text_input[i].text
			OOSheet('c' + str(i + 1)).value = self.concentration_text_input[i].text
		self.go_to_save_record_screen()

	def on_press_save_record_btn(self, dir):
		path = dir + self.configuration.record_path
		OOSheet().save_as(path)

	def on_press_save_btn(self, dir, filename, password):
		path = dir + '/' + filename
		self.data.save(path, password,
			self.expense_text_input,
			self.levels_text_input,
			self.concentration_text_input)
		self.go_to_home_screen()

	def on_press_load_data_btn(self, path, password, error):
		if len(path) != 0:
			if self.data.read(path[0], password.text):
				self.update()
				self.go_to_home_screen()
				error.text = ''
				password.text = ''
			else:
				password.text = ''
				error.text = 'Wrong password'
		else:
			error.text = 'Please select file!'


	def least_squares(self, x, y):
		if len(x) != len(y):
			return None
		xy = sum([i*j for i, j in zip(x, y)])
		x2 = sum([i**2 for i in x])
		sum_x = sum(x)
		sum_y = sum(y)
		n = len(x)
		x_average = sum_x/float(n)
		y_average = sum_y/float(n)
		b = (n * xy - sum_x * sum_y) / float(n*x2-sum_x**2)
		a = y_average - b * x_average
		return [a+b*i for i in x]

	def home_layout(self):
		main_home_layout = FloatLayout()

		h = GridLayout(cols=3, pos_hint={'center_x' : .65, 'center_y' : .97}, size_hint_x=.6)
		h.add_widget(Label(text=self.configuration.expense_label, font_size='20sp'))
		h.add_widget(Label(text=self.configuration.levels_label, font_size='20sp'))
		h.add_widget(Label(text=self.configuration.concentration_label, font_size='20sp'))
		main_home_layout.add_widget(h)

		if len(self.expense_text_input) == len(self.levels_text_input) == len(self.concentration_text_input):
			self.home_grid_layout = GridLayout(cols=3, row_force_default=True, row_default_height=30, size_hint_y=None)
			self.home_grid_layout.bind(minimum_height=self.home_grid_layout.setter('height'))
			for expense, level, concentration in zip(self.expense_text_input, self.levels_text_input, self.concentration_text_input):
				self.home_grid_layout.add_widget(expense)
				self.home_grid_layout.add_widget(level)
				self.home_grid_layout.add_widget(concentration)
		scroll_view = ScrollView(pos_hint={'center_x' : .65, 'center_y' : .52}, size_hint=(.6, .85))
		scroll_view.add_widget(self.home_grid_layout)
		main_home_layout.add_widget(scroll_view)

		menu = MenuSpawner(timeout=.5, 
			menu_args=dict(creation_direction=-1, radius=30,
			creation_timeout=.3,
			choices=[
				dict(text=self.configuration.menu_plots, index=1, callback=self.plots_submenu, font_size='18sp'),
				dict(text=self.configuration.menu_video_player, index=2, callback=self.go_to_video_player_screen, font_size='18sp'),
				dict(text=self.configuration.menu_make_record, index=3, callback=self.on_press_make_record, font_size='18sp'),
				dict(text=self.configuration.menu_data, index=4, callback=self.data_submenu, font_size='18sp'),
				dict(text=self.configuration.menu_reference, index=5, callback=self.go_to_reference_screen, font_size='18sp')
			]))
		main_home_layout.add_widget(menu)

		add_new_value_btn = Button(text='Add new value', font_size='18sp', 
			size_hint=(.15, .04), pos_hint={'center_x':.15, 'center_y':.8})
		add_new_value_btn.bind(on_press=lambda x:self.on_press_add_new_value_btn())
		main_home_layout.add_widget(add_new_value_btn)

		return main_home_layout

	def data_submenu(self, *args):
		args[0].parent.open_submenu(
			choices=[
				dict(text=self.configuration.submenu_load_data, index=1, callback=self.go_to_load_data_screen, font_size='18sp'),
				dict(text=self.configuration.submenu_save_data, index=2, callback=self.go_to_save_data_screen, font_size='18sp'),
			])

	def plots_submenu(self, *args):
		args[0].parent.open_submenu(
			choices=[
				dict(text=self.configuration.submenu_levels, index=1, callback=self.go_to_levels_plot_screen, font_size='18sp'),
				dict(text=self.configuration.submenu_concentration, index=2, callback=self.go_to_concentration_plot_screen, font_size='18sp')
			])

	def get_borders(self, x, y1, y2):
		xmin = min(x) - .1*abs(min(x))
		xmax = max(x) + .1*abs(max(x))
		ymin = min([min(item) for item in zip(y1, y2)])
		ymin -= .1*abs(ymin)
		ymax = max([max(item) for item in zip(y1, y2)])
		ymax += .1*abs(ymax)
		return xmin, xmax, ymin, ymax

	def levels_plot(self):
		expense = [float(item.text) for item in self.expense_text_input]
		levels = [float(item.text) for item in self.levels_text_input]
		least_squares = self.least_squares(expense, levels)
		xmin, xmax, ymin, ymax = self.get_borders(expense, levels, least_squares)
		graph = Graph(xlabel='Expense', ylabel='Level', x_ticks_minor=5,
		x_ticks_major=2.5, y_ticks_major=1,
		y_grid_label=True, x_grid_label=True, padding=10,
		x_grid=True, y_grid=True, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
		pos_hint={'center_x' : .5, 'center_y': .47}, size_hint=(1, .9))
		for x, y in zip(expense, levels):
			plot = LinePlot(line_width=4, color=self.configuration.plot_main_color)
			plot.points = [(x, y), (x+.1, y+.1)]
			graph.add_plot(plot)
		plot = MeshLinePlot(color=self.configuration.plot_least_squares_color)
		plot.points = [(i, j) for i, j in zip(expense, least_squares)]
		graph.add_plot(plot)
		return graph

	def concentration_plot(self):
		expense = [float(item.text) for item in self.expense_text_input]
		concentration = [float(item.text) for item in self.concentration_text_input]
		least_squares = self.least_squares(expense, concentration)
		xmin, xmax, ymin, ymax = self.get_borders(expense, concentration, least_squares)
		graph = Graph(xlabel='Expense', ylabel='Concentration', x_ticks_minor=5,
		x_ticks_major=2.5, y_ticks_major=100,
		y_grid_label=True, x_grid_label=True, padding=10,
		x_grid=True, y_grid=True, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
		pos_hint={'center_x' : .5, 'center_y': .47}, size_hint=(1, .9))
		for x, y in zip(expense, concentration):
			plot = LinePlot(line_width=4, color=self.configuration.plot_main_color)
			plot.points = [(x, y), (x+.1, y+.1)]
			graph.add_plot(plot)
		plot = MeshLinePlot(color=self.configuration.plot_least_squares_color)
		plot.points = [(i, j) for i, j in zip(expense, least_squares)]
		graph.add_plot(plot)
		return graph

	def levels_plot_layout(self):
		f = FloatLayout()
		back_btn = Button(text='Back', pos_hint={'center_x' : .1, 'center_y': .97}, 
			size_hint=(.2, .04), font_size='18sp')
		back_btn.bind(on_press=lambda x: self.go_to_home_screen())
		f.add_widget(back_btn)
		f.add_widget(Label(text=self.configuration.plot_levels_label,
			pos_hint={'center_x' : .5, 'center_y' : .93}, font_size='18sp'))
		plot = self.levels_plot()
		f.add_widget(plot)
		f.add_widget(PlotTouchListener(plot, self.scaling_down, self.scaling_up))
		return f

	def concentration_plot_layout(self):
		f = FloatLayout()
		back_btn = Button(text='Back', pos_hint={'center_x' : .1, 'center_y': .97}, 
			size_hint=(.2, .04), font_size='18sp')
		back_btn.bind(on_press=lambda x: self.go_to_home_screen())
		f.add_widget(back_btn)
		f.add_widget(Label(text=self.configuration.plot_concentration_label,
			pos_hint={'center_x' : .5, 'center_y' : .93}, font_size='18sp'))
		plot = self.concentration_plot()
		f.add_widget(plot)
		f.add_widget(PlotTouchListener(plot, self.scaling_down, self.scaling_up))
		return f

	def video_player_layout(self):
		layout = FloatLayout()
		chooseBtn = Button(
			text='Choose video file', 
			size_hint=(.4, .04), font_size='18sp',
			pos_hint={'center_x':.3,'center_y':.035})
		chooseBtn.bind(on_press=lambda x: self.go_to_video_file_screen())
		homeBtn = Button(
			text='Home', 
			size_hint=(.4, .04), font_size='18sp',
			pos_hint={'center_x':.7,'center_y':.035})
		homeBtn.bind(on_press=lambda x: self.go_to_home_screen())
		layout.add_widget(chooseBtn)
		layout.add_widget(homeBtn)
		layout.add_widget(self.video_player)
		return layout

	def reference_layout(self):
		main_layout = FloatLayout()
		main_layout.add_widget(Button(
			text='Home', 
			pos_hint={'center_x':.9, 'center_y':.975},
			size_hint=(.2,.04),
			on_press=lambda x: self.go_to_home_screen()))
		tabbedpanel = TabbedPanel(do_default_tab=False)

		about = TabbedPanelItem(text='About')
		about_layout = FloatLayout()
		about_layout.add_widget(Label(
			text=self.configuration.reference_about,
			pos_hint={'center_x':.5, 'center_y':.9},
			font_size='20sp'))
		about.add_widget(about_layout)
		
		menu = TabbedPanelItem(text='Reference')
		menu_layout = FloatLayout()
		menu_layout.add_widget(Label(
			text='#Menu', bold=True,
			pos_hint={'center_x':.1, 'center_y':.95},
			font_size='20sp'))
		menu_layout.add_widget(Label(
			text=self.configuration.reference_menu,
			pos_hint={'center_x':.5, 'center_y':.9},
			font_size='18sp'))
		menu_layout.add_widget(Label(text='#Plots', bold=True,
			pos_hint={'center_x':.1, 'center_y':.8},
			font_size='20sp'))
		menu_layout.add_widget(Label(
			text='Use scroll for scaling plots.',
			pos_hint={'center_x':.5, 'center_y':.75},
			font_size='18sp'))
		menu_layout.add_widget(Label(text='#VideoPlayer', bold=True,
			pos_hint={'center_x':.1, 'center_y':.65},
			font_size='20sp'))
		menu_layout.add_widget(Label(
			text=self.configuration.reference_videoplayer,
			pos_hint={'center_x':.5, 'center_y':.55},
			font_size='18sp'))
		menu.add_widget(menu_layout)
		menu_layout.add_widget(Label(
			text='#Data', bold=True,
			pos_hint={'center_x':.1,'center_y':.43},
			font_size='20sp'))
		menu_layout.add_widget(Label(
			text=self.configuration.reference_data,
			pos_hint={'center_x':.5, 'center_y':.33},
			font_size='18sp'))
		menu_layout.add_widget(Label(
			text='#Records', bold=True, 
			pos_hint={'center_x':.1, 'center_y':.2},
			font_size='20sp'))
		menu_layout.add_widget(Label(
			text=self.configuration.reference_record,
			pos_hint={'center_x':.5, 'center_y':.15},
			font_size='18sp'))

		tabbedpanel.add_widget(about)
		tabbedpanel.add_widget(menu)
		main_layout.add_widget(tabbedpanel)
		return main_layout

	def save_data_layout(self):
		layout = FloatLayout()
		layout.add_widget(Label(
			text='Choose path to save file',
			pos_hint={'center_x':.5,'center_y':.975},
			font_size='20sp'
			))
		filechooser = FileChooserThumbView(filters=['!%s' % self.configuration.save_hidden_files],
				size_hint=(1, .77), thumbsize=125,
				pos_hint={'center_x':.5,'center_y':.58})
		layout.add_widget(filechooser)
		layout.add_widget(Label(
			text='File name:', font_size='20sp',
			pos_hint={'center_x':.075,'center_y':.125}))
		textinput_filename = TextInput(
			text='*' + self.configuration.load_file_type,
			size_hint=(.85, .04), font_size='20sp',
			pos_hint={'center_x':.5375,'center_y':.125})
		layout.add_widget(textinput_filename)
		layout.add_widget(Label(
			text='Password:', font_size='20sp',
			pos_hint={'center_x':.075,'center_y':.083}))
		textinput_password = TextInput(
			size_hint=(.85, .04), font_size='20sp',
			pos_hint={'center_x':.5375,'center_y':.083},
			password=True)
		layout.add_widget(textinput_password)
		btn_save = Button(
			text='Save',
			size_hint=(.425, .04), font_size='18sp',
			pos_hint={'center_x':.325,'center_y':.035})
		btn_save.bind(on_press=lambda x: 
			self.on_press_save_btn(
				filechooser.path, 
				textinput_filename.text, 
				textinput_password.text))
		layout.add_widget(btn_save)
		btn_cancel = Button(
			text='Cancel',
			size_hint=(.425,.04), font_size='18sp',
			pos_hint={'center_x':.75,'center_y':.035})
		btn_cancel.bind(on_press=lambda x: self.go_to_home_screen())
		layout.add_widget(btn_cancel)
		return layout

	def load_data_layout(self):
		layout = FloatLayout()
		layout.add_widget(Label(
			text='Choose \'%s\' file to load and enter password' % self.configuration.load_file_type,
			pos_hint={'center_x':.5,'center_y':.975},
			font_size='20sp'))
		label_wrong_password = Label( 
			pos_hint={'center_x':.5,'center_y':.94},
			font_size='20sp',
			color=[.9,.49,.42,1])
		layout.add_widget(label_wrong_password)
		filechooser = FileChooserThumbView(filters=['*%s' % self.configuration.load_file_type],
				size_hint=(1, .8), thumbsize=125,
				pos_hint={'center_x':.5,'center_y':.55})
		layout.add_widget(filechooser)
		layout.add_widget(Label(
			text='Password:', font_size='20sp',
			pos_hint={'center_x':.075,'center_y':.083}))
		textinput_password = TextInput(
			size_hint=(.85, .04), font_size='20sp',
			pos_hint={'center_x':.5375,'center_y':.083},
			password=True)
		layout.add_widget(textinput_password)
		btn_load = Button(
			text='Load',
			size_hint=(.425, .04), font_size='18sp',
			pos_hint={'center_x':.325,'center_y':.035})
		btn_load.bind(on_press=lambda x: 
			self.on_press_load_data_btn(
				filechooser.selection, 
				textinput_password,
				label_wrong_password))
		layout.add_widget(btn_load)
		btn_cancel = Button(
			text='Cancel',
			size_hint=(.425,.04), font_size='18sp',
			pos_hint={'center_x':.75,'center_y':.035})
		btn_cancel.bind(on_press=lambda x: self.go_to_home_screen())
		layout.add_widget(btn_cancel)
		return layout

	def load_video_file_layout(self):
		layout = FloatLayout()
		layout.add_widget(Label(
			text='Choose video file to load',
			pos_hint={'center_x':.5,'center_y':.975},
			font_size='20sp'
			))
		filechooser = FileChooserThumbView(filters=['*.mp4', '*.avi', '*.mkv'],
				size_hint=(1, .85), thumbsize=125,
				pos_hint={'center_x':.5,'center_y':.55})
		layout.add_widget(filechooser)
		btn_load = Button(
			text='Load',
			size_hint=(.4, .04), font_size='18sp',
			pos_hint={'center_x':.3,'center_y':.035})
		btn_load.bind(on_press=lambda x: 
			self.on_press_select_video_file_btn(filechooser.selection))
		layout.add_widget(btn_load)
		btn_cancel = Button(
			text='Cancel',
			size_hint=(.4,.04), font_size='18sp',
			pos_hint={'center_x':.7,'center_y':.035})
		btn_cancel.bind(on_press=lambda x: self.go_to_video_player_screen())
		layout.add_widget(btn_cancel)
		return layout

	def save_record_layout(self):
		layout = FloatLayout()
		layout.add_widget(Label(
			text='Choose path to save file',
			pos_hint={'center_x':.5,'center_y':.975},
			font_size='20sp'
			))
		filechooser = FileChooserThumbView(filters=['*'],
				size_hint=(1, .77), thumbsize=125,
				pos_hint={'center_x':.5,'center_y':.53})
		layout.add_widget(filechooser)
		btn_save = Button(
			text='Save',
			size_hint=(.425, .04), font_size='18sp',
			pos_hint={'center_x':.325,'center_y':.035})
		btn_save.bind(on_press=lambda x: 
			self.on_press_save_record_btn(filechooser.path))
		layout.add_widget(btn_save)
		btn_cancel = Button(
			text='Cancel',
			size_hint=(.425,.04), font_size='18sp',
			pos_hint={'center_x':.75,'center_y':.035})
		btn_cancel.bind(on_press=lambda x: self.go_to_home_screen())
		layout.add_widget(btn_cancel)
		return layout

	def build(self):
		self.home_screen.add_widget(self.home_layout())
		self.concentration_plot_screen.clear_widgets()
		self.levels_plot_screen.add_widget(self.levels_plot_layout())
		self.concentration_plot_screen.add_widget(self.concentration_plot_layout())
		self.video_player_screen.add_widget(self.video_player_layout())
		self.video_file_screen.add_widget(self.load_video_file_layout())
		self.reference_screen.add_widget(self.reference_layout())
		self.load_data_screen.add_widget(self.load_data_layout())
		self.save_data_screen.add_widget(self.save_data_layout())
		self.save_record_screen.add_widget(self.save_record_layout())

		self.screen_manager.add_widget(self.home_screen)
		self.screen_manager.add_widget(self.levels_plot_screen)
		self.screen_manager.add_widget(self.concentration_plot_screen)
		self.screen_manager.add_widget(self.video_player_screen)
		self.screen_manager.add_widget(self.video_file_screen)
		self.screen_manager.add_widget(self.reference_screen)
		self.screen_manager.add_widget(self.load_data_screen)
		self.screen_manager.add_widget(self.save_data_screen)
		self.screen_manager.add_widget(self.save_record_screen)

		return self.screen_manager

if __name__ == '__main__':
	Main().run()