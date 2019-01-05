import datetime

class volatileSet:
	def __init__(self):
		self._d = dict()
	def add(self, key, timeout=datetime.timedelta(days=1000)):
		self._d[key] = datetime.datetime.now()+timeout
	def getAll(self):
		l = list()
		s = list()
		n = datetime.datetime.now()
		for i in self._d:
			if n > self._d[i]:
				s.append(i)
			else:
				l.append(i)
		if len(s):
			self._d.pop(*s)
		return l