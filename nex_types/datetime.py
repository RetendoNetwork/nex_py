import datetime, time


class DateTime:
	def __init__(self, value):
		self.val = value
		
	def second(self): return self.val & 63
	def minute(self): return (self.val >> 6) & 63
	def hour(self): return (self.val >> 12) & 31
	def day(self): return (self.val >> 17) & 31
	def month(self): return (self.val >> 22) & 15
	def year(self): return self.val >> 26
	
	def value(self): return self.val

	def standard_datetime(self):
		return datetime.datetime(
			self.year(), self.month(), self.day(),
			self.hour(), self.minute(), self.second(),
			tzinfo=datetime.timezone.utc
		)
	
	def timestamp(self):
		return int(self.standard_datetime().replace(tzinfo=None).timestamp())
	
	def __repr__(self):
		return "%i-%i-%i %i:%02i:%02i" %(self.day(), self.month(), self.year(), self.hour(), self.minute(), self.second())
		
	@classmethod
	def never(cls):
		return cls(0)
	
	@classmethod
	def future(cls):
		return cls.make(9999, 12, 31, 23, 59, 59)
		
	@classmethod
	def make(cls, year, month=1, day=1, hour=0, minute=0, second=0):
		return cls(second | (minute << 6) | (hour << 12) | (day << 17) | (month << 22) | (year << 26))
		
	@classmethod
	def fromtimestamp(cls, timestamp):
		dt = datetime.datetime.fromtimestamp(timestamp)
		return cls.make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	
	@classmethod
	def now(cls):
		return cls.fromtimestamp(time.time())