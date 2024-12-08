import datetime
import time


class DateTime:
    def __init__(self, timestamp_value):
        self.timestamp_value = timestamp_value
        
    def get_second(self): 
        return self.timestamp_value & 63
    
    def get_minute(self): 
        return (self.timestamp_value >> 6) & 63
    
    def get_hour(self): 
        return (self.timestamp_value >> 12) & 31
    
    def get_day(self): 
        return (self.timestamp_value >> 17) & 31
    
    def get_month(self): 
        return (self.timestamp_value >> 22) & 15
    
    def get_year(self): 
        return self.timestamp_value >> 26
    
    def get_timestamp_value(self): 
        return self.timestamp_value

    def to_standard_datetime(self):
        return datetime.datetime(
            self.get_year(), self.get_month(), self.get_day(),
            self.get_hour(), self.get_minute(), self.get_second(),
            tzinfo=datetime.timezone.utc
        )
    
    def get_unix_timestamp(self):
        return int(self.to_standard_datetime().replace(tzinfo=None).timestamp())
    
    def __repr__(self):
        return f"{self.get_day():02}-{self.get_month():02}-{self.get_year()} {self.get_hour():02}:{self.get_minute():02}:{self.get_second():02}"
    
    @classmethod
    def never(cls):
        return cls(0)
    
    @classmethod
    def far_future(cls):
        return cls.create(9999, 12, 31, 23, 59, 59)
    
    @classmethod
    def create(cls, year, month=1, day=1, hour=0, minute=0, second=0):
        return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
    
    @classmethod
    def from_unix_timestamp(cls, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp)
        return cls.create(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
    @classmethod
    def current_time(cls):
        return cls.from_unix_timestamp(time.time())