'''
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
import requests


class MyskillSkill(MycroftSkill):
    def __init__(self):
        super(BitcoinSkill, self).__init__(name="MySkill")

    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', 'en-us'))

        #prefixes = ['bitcoin', 'bitcoin price']
        prefixes = ['cortana', 'cortana price']
        self.__register_prefixed_regex(prefixes, "(?P<Word>\w+)")

        intent = IntentBuilder("MyIntent").require("MyKeyword").require("Word").build()
        self.register_intent(intent, self.handle_intent)

    def __register_prefixed_regex(self, prefixes, suffix_regex):
        for prefix in prefixes:
            self.register_regex(prefix + ' ' + suffix_regex)

    def handle_intent(self, message):
        price = requests.get("https://api.bitcoinaverage.com/all").json()['USD']['averages']['24h_avg']
        self.speak("The current bitcoin price is "+str(price)+" dollars.")

    def stop(self):
        pass


def create_skill():
    return BitcoinSkill()
'''



# Copyright 2017 Willem Ligtenberg
#
# Coin flip skill is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coin flip skill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_mp3

import random

__author__ = 'Willem Ligtenberg'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class CoinFlipSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(CoinFlipSkill, self).__init__(name="MySkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        coin_flip_intent = IntentBuilder("CoinFlipIntent").\
            require("CoinFlipKeyword").build()
        self.register_intent(coin_flip_intent, self.handle_coin_flip_intent)

    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_coin_flip_intent(self, message):
        #self.speak_dialog("flip.coin")
        #self.process = play_mp3(join(dirname(__file__), "mp3", "coin-flip.mp3"))
        if bool(random.getrandbits(1)):
            #self.process.wait()
            self.speak_dialog("heads")
        else:
            #self.process.wait()
            self.speak_dialog("tails")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return CoinFlipSkill()