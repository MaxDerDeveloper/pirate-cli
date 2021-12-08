logo = r"""           _            __                  ___ 
    ____  (_)________ _/ /____        _____/ (_)
   / __ \/ / ___/ __ `/ __/ _ \______/ ___/ / / 
  / /_/ / / /  / /_/ / /_/  __/_____/ /__/ / /  
 / .___/_/_/   \__,_/\__/\___/      \___/_/_/   
/_/                                             """

def rainbowify(data:str):
	from colorama import Fore
	from math import floor

	lines = data.replace("\r","").split("\n")

	x_len = max([len(line) for line in lines])
	y_len = len(lines)

	new = []
	for line in lines:
		new_line = line

		if x_len != len(line):
			diff      = x_len-len(line)
			new_line += chr(32)*diff
		
		new.append(new_line)

	array = list(map(list, new))

	colors = [
		Fore.RED,
		Fore.GREEN,
		Fore.BLUE,
		Fore.YELLOW,
		Fore.MAGENTA,
		Fore.CYAN
	]

	for y in range(y_len):
		for x in range(x_len):
			if array[y][x] == chr(32):
				continue

			idx = 4
			array[y][x] = colors[int(floor(idx))] + array[y][x]


	packed = "\n".join(["".join(line) for line in array])
	return packed

logo = rainbowify(logo)