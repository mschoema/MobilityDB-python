from MobilityDB.TimeTypes.period import Period
from MobilityDB.TimeTypes.periodset import PeriodSet
from MobilityDB.TemporalTypes.temporalinst import TemporalInst
from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS


class TemporalSeq(TEMPORALINSTANTS):
	"""
	Abstract class for temporal types of sequence duration
	"""
	__slots__ = ['_lower_inc', '_upper_inc', '_interp']

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None):
		# Constructor with a single argument of type string
		self._instantList = []
		if isinstance(instantList, str):
			ts = instantList.strip()
			if (ts.startswith('Interp=Stepwise;')):
				self._interp = 'Stepwise'
				ts = ts.replace('Interp=Stepwise;','')
			else:
				self._interp = 'Linear'
			if (ts[0] == '[' or ts[0] == '(') and (ts[-1] == ']' or ts[-1] == ')'):
				if ts[0] == '[':
					self._lower_inc = True
				else:
					self._lower_inc = False
				if ts[-1] == ']':
					self._upper_inc = True
				else:
					self._upper_inc = False
				ts = ts[1:-1]
				instants = ts.split(",")
				for inst in instants:
					self._instantList.append(TemporalSeq.ComponentClass(inst.strip()))
			else:
				raise Exception("ERROR: Could not parse temporal sequence value")
		# Constructor with a first argument of type list and two optional arguments for the bounds
		elif isinstance(instantList, list):
			# List of strings representing instant values
			if all(isinstance(arg, str) for arg in instantList):
				for arg in instantList:
					self._instantList.append(TemporalSeq.ComponentClass(arg))
			# List of instant values
			elif all(isinstance(arg, TemporalSeq.ComponentClass) for arg in instantList):
				for arg in instantList:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal sequence value")
			self._lower_inc = True if lower_inc == None or lower_inc == True else False
			self._upper_inc = True if upper_inc == True else False
			self.interp = True if upper_inc == True else False
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if len(self._instantList) == 1 and (not self._lower_inc or not self._lower_inc):
			raise Exception("ERROR: The lower and upper bounds must be inclusive for an instant temporal sequence")
		if any(x._time >= y._time for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: The timestamps of a temporal sequence must be increasing")
		if (self._interp == 'Stepwise' and len(self._instantList) > 1 and not self._upper_inc and
			self._instantList[-1]._value != self._instantList[-2]._value):
			raise Exception("ERROR: The last two values of a temporal sequence with exclusive upper bound and stepwise interpolation must be equal")
		return True

	@classmethod
	def duration(cls):
		return "Sequence"

	def lower_inc(self):
		"""
		Is the lower bound of the temporal sequence inclusive?
		"""
		return self._lower_inc

	def upper_inc(self):
		"""
		Is the upper bound of the temporal sequence inclusive?
		"""
		return self._upper_inc

	def getTime(self):
		"""
		Timestamp
		"""
		return PeriodSet([Period(self.startTimestamp(), self.endTimestamp(), self._lower_inc, self._upper_inc)])

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return Period(self.startTimestamp(), self.endTimestamp(), self.lower_inc(), self.upper_inc())

	def numSequences(self):
		"""
		Number of sequences
		"""
		return 1

	def startSequence(self):
		"""
		Start sequence
		"""
		return self

	def endSequence(self):
		"""
		End sequence
		"""
		return self

	def sequenceN(self, n):
		"""
		N-th sequence
		"""
		# 1-based
		if n == 1:
			return self
		else:
			raise Exception("ERROR: Out of range")

	def sequences(self):
		"""
		Sequences
		"""
		return [self]

	def intersectsTimestamp(self, timestamp):
		"""
		Intersects timestamp
		"""
		return ((self.lower_inc and self._instantList[0]._time == timestamp) or
			(self.upper_inc and self._instantList[-1]._time == timestamp) or
			(self._instantList[0]._time < timestamp < self._instantList[-1]._time))

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set
		"""
		return any(self.intersectsTimestamp(timestamp) for timestamp in timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects period
		"""
		return self.period().overlap(period)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects timestamp set
		"""
		return any(self.intersectsPeriod(period) for period in periodset._periodList)

	def __str__(self):
		lower_str = '[' if self._lower_inc else '('
		upper_str = ']' if self._upper_inc else ')'
		return "'" + lower_str + TEMPORALINSTANTS.__str__(self) + upper_str + "'"

