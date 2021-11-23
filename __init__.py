# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime

import requests
from adapt.intent import IntentBuilder
from lingua_franca.format import nice_date, nice_date_time, nice_time
from mycroft import MycroftSkill, intent_handler


class HelloWorldSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')

    @intent_handler(IntentBuilder('BusIntent')
                    .require('BusIntentKeyword'))
    def handle_hello_world_intent(self, message):
        """ Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        url = 'https://v5.db.transport.rest/stops/785901/arrivals?duration=30&results=4'
        r = requests.get(url)
        json_output = r.json()
        output = json_output["data"]
        times = []
        for bus in output:
            if bus.provenance == "Wernerwerkstraße, Regensburg":
                times.append(nice_time(datetime.strptime(bus.when, '%Y-%m-%dT%X')))

        if len(times) > 1:
            self.speak_dialog("There will be a bus eleven arriving at " + times[0] + " and " + times[1])
        elif len(times) > 0:
            self.speak_dialog("There will be a bus eleven arriving at " + times[0])
        else:
            self.speak_dialog("No buses are available")
        self.log.info("There are five types of log messages: "
                      "info, debug, warning, error, and exception.")

    def stop(self):
        pass


def create_skill():
    return HelloWorldSkill()