from datetime import datetime


class ConsumeParams:
    def __init__(self):
        self.db_generation_option = 0
        self.count_countries_names = 0
        self.airlines_names = []
        self.avail_flights = None
        self.start_time = datetime.now()

