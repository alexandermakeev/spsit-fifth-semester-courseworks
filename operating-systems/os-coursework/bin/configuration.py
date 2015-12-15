from ConfigParser import ConfigParser

class Configuration:
	def __init__(self, cfg_file):
		config = ConfigParser()
		config.readfp(open(cfg_file))
		self.screen_manager_transition_duration = float(config.get('screen_manager_section', 
			'transition_duration'))
		self.plot_scalling_down=config.get('plot_section', 'scaling_down')
		self.plot_scalling_up=config.get('plot_section', 'scaling_up')
		self.plot_main_color = [float(color) for color 
			in config.get('plot_section', 'main_color').split(',')]
		self.plot_least_squares_color = [float(color) for color 
			in config.get('plot_section', 'least_squares_color').split(',')]
		self.plot_levels_label=config.get('plot_section', 'levels_plot_label')
		self.plot_concentration_label=config.get('plot_section', 'concentration_plot_label')
		self.video_path = config.get('video_player_screen_section', 'default_video_path')
		self.record_path = config.get('record_section', 'path')
		self.expense_label = config.get('data_section', 'expense_label')
		self.levels_label = config.get('data_section', 'levels_label')
		self.concentration_label = config.get('data_section', 'concentration_label')
		self.load_file_type = config.get('load_save_data_section', 'type')
		self.save_hidden_files = config.get('load_save_data_section', 'hidden')
		self.menu_plots = config.get('menu_section', 'plots')
		self.menu_video_player = config.get('menu_section', 'video_player')
		self.menu_make_record = config.get('menu_section', 'make_record')
		self.menu_data = config.get('menu_section', 'data')
		self.menu_reference = config.get('menu_section', 'reference')
		self.submenu_load_data = config.get('submenu_section', 'load_data')
		self.submenu_save_data = config.get('submenu_section', 'save_data')
		self.submenu_levels = config.get('submenu_section', 'levels')
		self.submenu_concentration = config.get('submenu_section', 'concentration')
		self.reference_about = config.get('reference_screen_section', 'about')
		self.reference_menu = config.get('reference_screen_section', 'menu')
		self.reference_plots = config.get('reference_screen_section', 'plots')
		self.reference_videoplayer = config.get('reference_screen_section', 'videoplayer')
		self.reference_data = config.get('reference_screen_section', 'data')
		self.reference_record = config.get('reference_screen_section', 'record')