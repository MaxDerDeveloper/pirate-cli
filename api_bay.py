from urllib.parse import quote
# from pprint import pprint
from typing import List

import requests
# import json

import debug

trackers = [
	"udp://tracker.coppersurfer.tk:6969/announce",
	"udp://tracker.openbittorrent.com:6969/announce",
	"udp://9.rarbg.to:2710/announce",
	"udp://9.rarbg.me:2780/announce",
	"udp://9.rarbg.to:2730/announce",
	"udp://tracker.opentrackr.org:1337",
	"http://p4p.arenabg.com:1337/announce",
	"udp://tracker.torrent.eu.org:451/announce",
	"udp://tracker.tiny-vps.com:6969/announce",
	"udp://open.stealth.si:80/announce"
]

def __base_request(script:str, params:dict, scheme="https", host="apibay.org", proxy={}, session=None):
	if not session:
		session = requests

	url  = "{0}://{1}/{2}".format(scheme, host, script,)
	resp = session.get(url, params=params, proxies={scheme:proxy})

	if resp.ok:
		return resp.json()

def findTorrents(term:str, **kwargs) -> List[dict]:
	return __base_request("q.php", {"q":term}, **kwargs)

def torrentInfo(id:int, **kwargs) -> dict:
	return __base_request("t.php", {"id":id}, **kwargs)

def torrentFiles(id:int, **kwargs) -> dict:
	return __base_request("f.php", {"id":id}, **kwargs)

def createMagnetlink(info_hash:str, name:str, algo:str="btih")->str:
	f = lambda x: quote(x, safe="")

	magnet  = "magnet:?xt=urn:{algo}:{info_hash}&dn={name}".format(
		algo      = algo,
		info_hash = info_hash,
		name      = f(name)
	)

	for tracker in trackers:
		magnet += "&tr=" + f(tracker)

	return magnet


if __name__ == '__main__':
	episode = findTorrents("The Walking Dead S11E01")
	id      = int(episode[0]["id"])
	
	print(id)
	pprint(torrentInfo (id))
	pprint(torrentFiles(id))