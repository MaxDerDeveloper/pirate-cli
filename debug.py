from colorama import Fore, Style, init
from math import floor, ceil
import time
import sys

__version__ = "1.3"
# 1.3 ProgressBar now respects the showAfter parameter
# 1.2: _base added keyword func, _base is no lambda anymore
# 1.1: _base updated to convert color to string
# 1.0: _base updated to apply kwargs to entire output

init()

# _base    = lambda col, *args, **kwargs, func=print: [func(str(col)+str(args[0]), *args[1:], **kwargs),func(end=Style.RESET_ALL)]
def _base(col, *args, func=print, **kwargs):
	func(str(col)+str(args[0]), *args[1:], **kwargs)
	func(end=Style.RESET_ALL)

info     = lambda *args, **kwargs: _base(Fore.LIGHTBLACK_EX, "[*]", *args, **kwargs)
progress = lambda *args, **kwargs: _base(Fore.GREEN,         "[+]", *args, **kwargs)
error    = lambda *args, **kwargs: _base(Fore.RED,           "[-]", *args, **kwargs)
warning  = lambda *args, **kwargs: _base(Fore.YELLOW,        "[!]", *args, **kwargs)

raw_info = lambda *args, **kwargs: _base(Fore.LIGHTBLACK_EX, *args, **kwargs)

def formatSeconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes   = divmod(minutes, 60)
	return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def formatPercentage(p):
	strNumber = str(round(100*p, 2))
	
	digits, decimals = strNumber.split(".")

	digits   = digits.  rjust(3, " ")
	decimals = decimals.ljust(2, '0')

	return f"{digits}.{decimals} %"

class ProgressBar:
	def __init__(self, title, showAfter=5, ):
		self.title     = title
		self.showAfter = showAfter
		self.lastLen   = 0
		self.start     = None

		self.showCount = 0


	def loopProgress(self, index, totalLength, length=20, fill="#", empty=" ", sep=None):
		if self.showCount != self.showAfter:
			self.showCount += 1
			return
		else:
			self.showCount = 0

		percentage  = (index) / totalLength

		if self.start == None:
			self.start = time.time()

		filledChars  = int(floor(percentage * length))

		emptyChars   = length - filledChars
		filledString = filledChars*fill + (sep if sep!=None else "") + emptyChars*empty

		if percentage == 0.0 or index == 0:
			formattedEta = "--:--:--"
		else:
			timeTaken    = time.time() - self.start
			eta_sec      = timeTaken/percentage - timeTaken
			formattedEta = formatSeconds(int(ceil(eta_sec)))


		CarriageReturn  = "\r"*self.lastLen
		formattedString = f"{self.title}: [{filledString}] {formatPercentage(percentage)} | {formattedEta}"


		if index == totalLength and sep != None:
			formattedString = formattedString.replace(sep, fill)

		print(CarriageReturn+formattedString, end="")

		if len(formattedString) < self.lastLen:
			print(" "*(len(formattedString)-self.lastLen), end="")

		if index == totalLength:
			print()

		self.lastLen = len(formattedString)