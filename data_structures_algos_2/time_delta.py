from datetime import time, timedelta, date, datetime


class Time:
    def __init__(self, hrs, minutes):
        self.time_delta = time(hrs, minutes, 0)
        self.clock_time = datetime.combine(date.today(), self.time_delta).strftime("%H:%M %p")

    def add(self, _minutes_):
        self.time_delta = (datetime.combine(date.today(), self.time_delta) + timedelta(minutes=_minutes_)).time()
        self.clock_time = datetime.combine(date.today(), self.time_delta).strftime("%H:%M %p")
        print(self.clock_time)
