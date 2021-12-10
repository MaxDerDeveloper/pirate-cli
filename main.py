from tabulate     import tabulate
from threading    import Thread
from pprint       import pprint
from getch        import getch
from api_bay      import *

import argparse
import humanize
import getpass
import debug
import time
import logo
import sys
import os

clear = lambda: sys.stdout.write("\033[H\033[J")

def parseArgs():
	parser = argparse.ArgumentParser(
		description="Pirate-cli is a simple tool to query 'The Pirate Bay'",
		allow_abbrev=False,
	)

	parser.add_argument(
		"--best", "-b", 
		help="selects the first torrent suggestion automatically",
		action="store_true"
	)

	parser.add_argument(
		"--silent", "-s", 
		help   = "outputs generated magnet-link only (implies '--best')",
		action = "store_true"
	)

	parser.add_argument(
		"--info", "-i", 
		help   = "obtains info about suggested torrent for query (implies '--silent')",
		action = "store_true"
	)

	parser.add_argument(
		"--limit", "-l", 
		help    = "limits the results for further requests",
		action  = "store",
		dest    = "limit",
		type    = int,
		default = 10
	)

	parser.add_argument(
		"queries",
		help="stores your queries",
		nargs="*"
	)

	args = parser.parse_args()

	print(args)

	if args.info:
		args.silent = True

	if args.silent:
		args.best = True

		if len(args.queries) < 1:
			debug.error("For '--silent' at least one query is needed.", file=sys.stderr)
			exit(1)

	return args.queries, {
		"best":   args.best,
		"silent": args.silent,
		"info":   args.info,
		"limit":  args.limit
	}


def main(query=None, silent=False, best=False, info=False, limit=None):
	if not limit:
		limit = 10

	running = True
	while running:
		if not silent:
			clear()
			user = getpass.getuser()
			debug.raw_info(f"Welcome to {debug.Fore.YELLOW}pirate-cli{debug.Fore.LIGHTBLACK_EX}, {user}!")
			print(logo.logo, end=debug.Style.RESET_ALL+"\n\n")

		if not silent:
			debug.info("Settings have been loaded")

		try:
			### Get query ###
			if not silent:
				debug.info("Please enter your search term")
				query = input("> ")
			else:
				# Just use query from kwargs
				pass

			### Search ###
			result  = findTorrents(query)

			# Cut off irrelevant results.
			if not best:
				result = result[:limit]
			else:
				# Only need best torrent (one only)
				result = result[:1]

			max_len = len(str(len(result)))
			table   = []

			if not silent:
				debug.info(f"Found {len(result)} torrent files")
				debug.info(f"Retrieving information for torrents")

			session = requests.Session()

			if not silent:
				pb = debug.ProgressBar("Collecting data", showAfter=1)
				pb.loopProgress(0, len(result))

			for i, torrent in enumerate(result):
				result[i]["info"]  = torrentInfo (torrent["id"], session=session)
				result[i]["files"] = torrentFiles(torrent["id"], session=session)

				if not silent:
					pb.loopProgress(i+1, len(result))

				# if not "1080p" in torrent["name"]:
				# 	continue

				table.append([
					i+1,
					torrent["name"],
					torrent["id"],
					torrent["seeders"],
					torrent["leechers"],
					
					humanize.naturalsize(torrent["size"])
				])

			else:
				if not silent:
					pb.loopProgress(len(result), len(result))
					sys.stdout.write("\n")

			if not silent:
				print(tabulate(
					table,
					headers=["Index", "Name", "ID", "Seeders", "Leechers", "Size"]
				))

			if info:
				# torrent info
				tinfo = result[0].copy()
				tinfo["magnet"] = createMagnetlink(
					tinfo["info_hash"],
					tinfo["name"]
				)
				dump = json.dumps(tinfo)
				sys.stdout.write(dump)

				# quit
				running = False
				continue

			### Choose torrent ###

			if not silent:
				sys.stdout.write("\n")

			if not best:
				debug.info("Please enter your preferred torrent's index. (0 to edit query)")
				choice = -1
				while True:
					try:
						choice = int(input("> "))-1
					except ValueError:
						choice = -1

					if (0 <= choice < len(result)) or choice+1==0:
						break
					else:
						if not silent:
							debug.error("Please choose an index from the table above.")

				# Retry, to edit query
				if choice+1 == 0:
					continue
			else:
				choice = 0

			### Display choice-data ###
			magnet = createMagnetlink(
				info_hash = result[choice]["info_hash"],
				name      = result[choice]["name"]
			)
			if not silent:
				print("Here's your magnet link")
				print("=>", debug.Fore.LIGHTMAGENTA_EX + magnet + debug.Style.RESET_ALL)
			else:
				sys.stdout.write(magnet)

			### Bottom menu ###
			if not silent:
				print("\n[R etry] [Q uit]")
				char = getch().upper()
				if   char == "R":
					continue
				elif char == "Q":
					running = False
				else:
					debug.warning(f"Other character has been entered: {char!r}")
					debug.info("Exiting")
					running = False
			else:
				running = False

		except KeyboardInterrupt:
			running = False
			break


if __name__ == "__main__":
	queries, kwargs = parseArgs()

	if kwargs.get("silent"):
		for i,query in enumerate(queries):
			main(query=query, **kwargs)

			# Line breaks between links
			if i != len(queries)-1:
				sys.stdout.write("\n")
	else:
		main(None, **kwargs)