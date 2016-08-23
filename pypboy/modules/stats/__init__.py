from pypboy import BaseModule
from pypboy.modules.stats import general
from pypboy.modules.stats import perks
from pypboy.modules.stats import skills
from pypboy.modules.stats import special
from pypboy.modules.stats import status


class Module(BaseModule):

	label = "STATS"
	GPIO_LED_ID = 22 #GPIO 22 #19

	def __init__(self, *args, **kwargs):
		self.submodules = [
			status.Module(self),
			special.Module(self),
			skills.Module(self),
			perks.Module(self),
			general.Module(self)
		]
		super(Module, self).__init__(*args, **kwargs)
