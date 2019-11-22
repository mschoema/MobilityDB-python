from .temporal import TEMPORAL
from .temporalinst import TEMPORALINST


class TEMPORALINSTANTS:
	__slots__ = ['_instantList']

	def __init__(self, instantList=None):
		if instantList is not None and len(instantList) > 0:
			self._instantList = instantList
		else:
			raise Exception("ERROR: Could not parse temporal value")
		# Verify validity of the resulting list
		#if not self._valid():
		#	raise Exception("ERROR: Timestamps must be increasing")

	def _valid(self):
		return all(x._time < y._time for x, y in zip(self._instantList, self._instantList[1:]))

	def startValue(self):
		"""
		Start value
		"""
		return self._instantList[0]._value

	def endValue(self):
		"""
		Start value
		"""
		return self._instantList[len(self._instantList) - 1]._value

	def numInstants(self):
		"""
		Number of distinct instants
		"""
		return len(self._instantList)

	def startInstant(self):
		"""
		Start instant
		"""
		return self._instantList[0]

	def endInstant(self):
		"""
		End instant
		"""
		return self._instantList[len(self._instantList) - 1]

	def instantN(self, n):
		"""
		N-th instant
		"""
		# 1-based
		if 0 <= n < len(self._instantList):
			return self._instantList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def instants(self):
		"""
		Instants
		"""
		return self._instantList

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self._instantList)

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._instantList[0]

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._instantList[len(self._instantList) - 1]

	def timestampN(self, n):
		"""
		N-th timestamp
		"""
		# 1-based
		if 0 <= n < len(self._instantList):
			return self._instantList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Timestamps
		"""
		return [instant._time for instant in self._instantList]

	def __str__(self):
		return "{}".format(', '.join('{}'.format(instant.__str__().replace("'", ""))
			for instant in self._instantList))
