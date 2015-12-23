from enum import Enum

class Type(Enum):
	aperiodic_first_order = -20
	aperiodic_second_order = -40
	oscillatory = -40 
	differentiating = 20
	forsing_first_order = 20
	forsing_second_order = 40