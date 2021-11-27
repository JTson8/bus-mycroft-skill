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
        super().__init__()
        self.learning = True

    def initialize(self):
        my_setting = self.settings.get('my_setting')

    @intent_handler(IntentBuilder('BothBusesIntent')
                    .require('BusIntentKeyword'))
    def handle_both_buses_intent(self, message):
        eleven_speech = self.handle_bus_eleven()
        six_speech = self.handle_bus_six()
        self.speak_dialog(eleven_speech + " and " + six_speech)


    @intent_handler(IntentBuilder('BusElevenIntent')
                    .require('BusElevenIntentKeyword'))
    def handle_bus_eleven_intent(self, message):
        self.speak_dialog(self.handle_bus_eleven())

    @intent_handler(IntentBuilder('BusSixIntent')
                    .require('BusSixIntentKeyword'))
    def handle_bus_six_intent(self, message):
        self.speak_dialog(self.handle_bus_six())

    def handle_bus_eleven(self):
        url = 'https://v5.db.transport.rest/stops/785901/arrivals?duration=60&results=4'
        r = requests.get(url)
        output = r.json()
        times_eleven = []
        for bus in output:
            if bus["provenance"] == "Wernerwerkstraße, Regensburg":
                times_eleven.append(nice_time(datetime.strptime(bus["when"], '%Y-%m-%dT%X+01:00'), use_24hour=True))
        if len(times_eleven) > 1:
            eleven_speech = ("A bus eleven is arriving at " + times_eleven[0] + " and " + times_eleven[1])
        elif len(times_eleven) > 0:
            eleven_speech = ("A bus eleven is arriving at " + times_eleven[0])
        else:
            eleven_speech = "No bus elevens are available"
        return eleven_speech

    def handle_bus_six(self):
        url = 'https://v5.db.transport.rest/stops/785798/arrivals?duration=60&results=4'
        r = requests.get(url)
        output = r.json()
        times_six = []
        for bus in output:
            if bus["provenance"] == "Roter-Brach-Weg, Regensburg":
                times_six.append(nice_time(datetime.strptime(bus["when"], '%Y-%m-%dT%X+01:00'), use_24hour=True))
        if len(times_six) > 1:
            six_speech = ("A bus six is arriving at " + times_six[0] + " and " + times_six[1])
        elif len(times_six) > 0:
            six_speech = ("A bus six is arriving at " + times_six[0])
        else:
            six_speech = "No bus sixes are available"
        return six_speech

    def stop(self):
        pass


def create_skill():
    return HelloWorldSkill()
