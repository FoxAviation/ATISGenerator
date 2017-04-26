from datetime import datetime
import random
from enum import Enum


class RunwayIdentifier(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3
    NONE = 4

    def to_string(self):
        if self == RunwayIdentifier.LEFT:
            return "left"
        if self == RunwayIdentifier.RIGHT:
            return "right"
        if self == RunwayIdentifier.CENTER:
            return "center"
        return ""

    def to_short_string(id):
        if id == RunwayIdentifier.LEFT:
            return "L"
        if id == RunwayIdentifier.RIGHT:
            return "R"
        if id == RunwayIdentifier.CENTER:
            return "C"
        return ""

    def reverse_identifier(id):
        if id == RunwayIdentifier.LEFT:
            return RunwayIdentifier.RIGHT
        if id == RunwayIdentifier.RIGHT:
            return RunwayIdentifier.LEFT
        else:
            return id


class GeneralWeatherCondition(Enum):
    CLEAR = 0
    CLOUDY = 1
    THUNDERSTORM = 2

    def get_random_condition(self):
        lst = []
        for c in self:
            lst.append(c)
        return lst[random.randint(0, len(lst))]


class Airport:
    def __init__(self, name, runways):
        self.name = name
        self.runways = runways

    # TODO: Debug (NoneType)
    def get_current_runways(self, wind_dir=0):
        selection = []
        for r in self.runways:
            if abs(r.direction - (wind_dir / 10)) < 18:
                selection.append(r)
        if len(selection) == 0:
            print("Failed")
        return selection


class Runway:
    def __init__(self, heading, identifier=RunwayIdentifier.NONE):
        self.direction = heading
        self.identifier = identifier

    def from_string(raw_string):
        if raw_string[-1] == "R" or raw_string[-1] == "r":
            return Runway(int(raw_string[:-1]), RunwayIdentifier.RIGHT)
        if raw_string[-1] == "L" or raw_string[-1] == "l":
            return Runway(int(raw_string[:-1]), RunwayIdentifier.LEFT)
        if raw_string[-1] == "C" or raw_string[-1] == "c":
            return Runway(int(raw_string[:-1]), RunwayIdentifier.CENTER)
        return Runway(int(raw_string), RunwayIdentifier.NONE)

    def to_string(self):
        if self.identifier == RunwayIdentifier.NONE:
            return str(self.direction)
        else:
            return str(self.direction) + " " + self.identifier.to_string()


class EnvironmentData:
    def __init__(self, wind, temperature, dewpoint, cavok):
        self.dewpoint = dewpoint
        self.wind = wind
        self.temperature = temperature
        self.cavok = cavok

    @staticmethod
    def create_data(condition):
        if condition == GeneralWeatherCondition.CLEAR:
            pass
        elif condition == GeneralWeatherCondition.CLOUDY:
            pass
        else:
            pass


def get_atis_time():
    c_time = datetime.utcnow()
    minute = 50
    if 20 <= c_time.minute < 50:
        minute = 20
    return c_time.hour, minute


def create_random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def input_runways():
    runways_raw = (input("Available runways (one direction only): ")).split(" ")

    # Process string
    runways = []
    for r in runways_raw:
        runways.append(Runway.from_string(r))

    output = []
    # Add reverse runways
    for r in runways:
        new = Runway((r.direction + 18) % 36, RunwayIdentifier.reverse_identifier(r.identifier))
        output.append(new)
        output.append(r)

    return output


def input_airport():
    return input("Type airport name: ")


def create_atis(info_letter):
    time = get_atis_time()
    wind = [create_random_int(0, 360), create_random_int(0, 20)]
    airport = Airport(input_airport(), input_runways())
    info_h = airport.name + " information " + info_letter
    time_h = "Met report time " + str(time[0]) + ":" + str(time[1]) + "Z"

    # Create runways string
    runway_string = ""
    for r in airport.get_current_runways(wind[0]):  # TODO: Remove once fixed
        runway_string += r.to_string() + " and "
    rwy_h = "Runways in use " + runway_string[:-5]

    tl_h = "Transition level 6 0"
    wind_h = "Wind " + str(wind[0]) + " degrees " + str(wind[1]) + " knots"
    # TODO: Add CAVOK & clouds
    temperature = create_random_int(-10, 30)
    temp_h = "Temperature " + str(temperature) + ", dewpoint " + str(create_random_int(temperature - 20, temperature))
    qnh_h = "QNH " + str(create_random_int(995, 1035))
    trend_h = "Trend NOSIG"
    final_h = "Information " + info_letter + "\n" + "OUT"
    # Output final string
    return info_h + "\n" + time_h + "\n" + rwy_h + "\n" + tl_h + "\n" + wind_h + "\n" + temp_h + "\n" + qnh_h + "\n" + trend_h + "\n" + final_h


print(create_atis("Lima"))
