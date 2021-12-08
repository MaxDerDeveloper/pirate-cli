logos = [
"""                 .                                  s
                @88>                               :8                                    .d88"    @88>  
 .d``           %8P      .u    .                  .88                                   5888R     %8P   
 @8Ne.   .u      .     .d88B :@8c        u       :888ooo      .u                   .    '888R      .    
 %8888:u@88N   .@88u  ="8888f8888r    us888u.  -*8888888   ud8888.            .udR88N    888R    .@88u  
  `888I  888. ''888E`   4888>'88"  .@88 "8888"   8888    :888'8888.          <888'888k   888R   ''888E` 
   888I  888I   888E    4888> '    9888  9888    8888    d888 '88%"          9888 'Y"    888R     888E  
   888I  888I   888E    4888>      9888  9888    8888    8888.+"             9888        888R     888E  
 uW888L  888'   888E   .d888L .+   9888  9888   .8888Lu= 8888L      88888888 9888        888R     888E  
'*88888Nu88P    888&   ^"8888*"    9888  9888   ^%888*   '8888c. .+ 88888888 ?8888u../  .888B .   888&  
~ '88888F`      R888"     "Y"      "888*""888"    'Y"     "88888%             "8888P'   ^*888%    R888" 
   888 ^         ""                 ^Y"   ^Y'               "YP'                "P'       "%       ""   
   *8E                                                                                                  
   '8>                                                                                                  
    "                                                                                                   

""",

r"""           _            __                  ___ 
    ____  (_)________ _/ /____        _____/ (_)
   / __ \/ / ___/ __ `/ __/ _ \______/ ___/ / / 
  / /_/ / / /  / /_/ / /_/  __/_____/ /__/ / /  
 / .___/_/_/   \__,_/\__/\___/      \___/_/_/   
/_/                                             """
]

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
			# n = len(colors)
			# a = 35
			# idx = (x*y/a) % n
			idx = 4
			array[y][x] += colors[int(floor(idx))]


	packed = "\n".join(["".join(line) for line in array])
	return packed


i = 1
logos[i] = rainbowify(logos[i])