from tabulate     import tabulate
from threading    import Thread
from pprint       import pprint
from api_bay      import *

import humanize
import getpass
import msvcrt
import debug
import json
import time
import logo
import sys
import os

clear = lambda: sys.stdout.write("\033[H\033[J")

def main():
	user     = getpass.getuser()

	# filters = ["480p", "720p", "1080p", "2160p", "x264", "x265"]

	running = True
	while running:
		clear()
		debug.raw_info(f"Welcome to {debug.Fore.YELLOW}pirate-cli{debug.Fore.LIGHTBLACK_EX}, {user}!")

		print(logo.logo, end=debug.Style.RESET_ALL+"\n\n")

		settings = json.load(open("settings.json", "r"))
		debug.info("Settings have been loaded")

		try:
			### Get query ###
			debug.info("Please enter your search term")
			query = input("> ")

			### Search ###
			result  = findTorrents(query)

			# Cut off irrelevant results.
			result  = result[:settings["limit"]]

			max_len = len(str(len(result)))
			table   = []

			debug.info(f"Found {len(result)} torrent files")
			debug.info(f"Retrieving information for torrents")

			session = requests.Session()
			pb      = debug.ProgressBar("Collecting data", showAfter=1)
			pb.loopProgress(0, len(result))
			for i, torrent in enumerate(result):
				result[i]["info"]  = torrentInfo (torrent["id"], session=session)
				result[i]["files"] = torrentFiles(torrent["id"], session=session)

				pb.loopProgress(i+1, len(result))

				# if not "1080p" in torrent["name"]:
				# 	continue

				table.append([
					i+1,
					torrent["name"],
					torrent["id"],
					torrent["seeders"],
					torrent["leechers"],
					
					# torrent["size"],
					humanize.naturalsize(torrent["size"])

				])

			else:
				pb.loopProgress(len(result), len(result))
				sys.stdout.write("\n")


			# pprint(result)

			print(tabulate(
				table,
				headers=["Index", "Name", "ID", "Seeders", "Leechers", "Size"]
			))

			### Filter ###
			# print("Filters")
			# for i,option in enumerate(filters):
			# 	print(f"\t{i+1}. {option}")

			### Choose torrent ###

			sys.stdout.write("\n")
			debug.info("Please enter your preferred torrent's index.")
			choice = -1
			while True:
				try:
					choice = int(input("> "))-1
				except ValueError:
					choice = -1

				if 0 <= choice < len(result):
					break
				else:
					debug.error("Please choose an index from the table above.")

			### Display choice-data ###
			magnet = createMagnetlink(
				info_hash = result[choice]["info_hash"],
				name      = result[choice]["name"]
			)
			print("Here's your magnet link")
			print("=>", debug.Fore.LIGHTMAGENTA_EX + magnet + debug.Style.RESET_ALL)

			### Bottom menu ###
			print("\n[R etry] [Q uit]")
			char = msvcrt.getch().decode("utf-8").upper()
			if   char == "R":
				continue
			elif char == "Q":
				running = False
			else:
				debug.warning(f"Other character has been entered: {char!r}")
				debug.info("Exiting")
				running = False

		except KeyboardInterrupt:
			running = False
			break


if __name__ == "__main__":
	main()