#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import csv
import gzip
import codecs
import operator
import romkan
import jaconv
import html
import unicodedata
import json


SJIS_WARN = False


all_rows = u'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺアイウエオカキクケコシサスセソタチツテトナニヌネノハパヒピフプヘペホポマミムメモヤユヨラリルレロあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめやゆもよらりれる'
e1 = u'ＢＣＤＥＦＧＨＩＪＫＬ'
e2 = u'ＡＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'  # a=wall
e3 = u'アイウエオカキクケコサ'
e6 = u'スセソタチツテトナニヌネ'
e5 = u'シノハパヒピフプヘペホポマ'  # tsu=wall
e4 = u'ミムメモヤユヨラリルレロ'
w1a = u'れにぬねのはひふへほまみむめも'  # re=wall 
w1b = u'やゆよらりる'
w2a = u'あくけこさしすせそたちつてとな'  # a=wall
w2b = u'いうえおかき'
all_halls = {"e1":e1,"e2":e2,"e3":e3,"e6":e6,"e5":e5,"e4":e4,"w1a":w1a,"w1b":w1b,"w2a":w2a,"w2b":w2b}
all_days = ['土','日','月']

genres = {
	'500': 'anime/other',
	'535': 'garupan',
	'511': 'anime/shoujo',
	'999': 'non-genre',
	'233': '>lovelive',
	'835': 'kekkai sensen',
	'831': 'hetalia',
	'400': 'SJump/other',
	'432': 'haikyu',
	'431': 'kuroko no basket',
	'531': 'gundam',
	'433': 'world trigger',
	'812': 'shoujo',
	'911': 'cosplay',
	'813': 'shoujo/seinen',
	'833': 'attack on titan',
	'811': 'novel',
	'532': 'tiger&bunny',
	'533': 'osomatsu-san',
	'534': 'yuuri (not yuri)',
	'832': 'yowamushi pedal',
	'116': 'merch',
	'700': 'tv shows',
	'711': 'music and male idols ??',
	'114': 'history, oc/novels',
	'113': 'oc/gay dudes',
	'112': 'oc/shoujo',
	'221': 'TYPE-MOON',
	'300': 'game/other',
	'321': 'squenix/rpg',
	'332': 'tokuen ranbu',
	'212': 'digital/other (ACTUALLY MUSIC)',
	'213': 'doujin software',
	'333': 'ansanburu stars',
	'315': 'games/for social girls',
	'314': 'games/dating sims',
	'313': 'games/rpg',
	'234': 'TOUHOU HIJACK LOL',
	'312': 'games/net/social',
	'334': 'azure lane',
	'331': 'kancolle',
	'311': 'games/analogue',
	'912': 'stuff for dudes',
	'600': 'info/criticism??',
	'111': 'oc/shonen',
	'211': 'galge',
	'232': 'IM@S',
	'115': 'academics',
	'611': 'i like trains'
}


class SPIRAL_KOMACHI_SPKM_0003(object):
	def __init__(self, binfile):
		self.binfile = binfile

	def __iter__(self):
		nline = 0
		for ln in self.binfile:
			nline += 1
			try:
				yield ln.decode('sjis').rstrip()
			except UnicodeDecodeError as uee:
				rv = ln.decode('sjis', 'backslashreplace').rstrip()
				yield rv

				if SJIS_WARN:
					print('WARNING: csv decode error line {} byte {}'.format(nline, uee.start))
					try:
						ofs = len(ln[:uee.start].decode('sjis', 'backslashreplace'))
						print('{}\033[1;37;41m{}\033[0m{}'.format(
							rv[:ofs], rv[ofs:ofs+3], rv[ofs+3:]))
					except:
						print(rv)


wbuf = u''
def p(msg):
	global wbuf
	wbuf += msg + '\n'
	print(msg)


def main():
	global wbuf
	r = []
	print('loading csv')
	with gzip.open('../raw-data/everything-csv-ver2.csv.gz', 'rb') as fgz:
		#fu8 = codecs.iterdecode(fgz, 'sjis')
		fu8 = SPIRAL_KOMACHI_SPKM_0003(fgz)
		fcsv = csv.reader(fu8, delimiter=',')
		for cr in fcsv:
			if cr[0] != 'Circle':
				#print('skipping; cr[0] =', cr[0])
				continue

			if len(cr) != 29:
				raise Exception('unexpected num fields {}'.format(len(cr)))

			v = {
				'imageid': cr[1],
				'ccc-gui-color-probably': cr[2],
				'ccc-gui-page-number': cr[3],
				'ccc-gui-page-offset': cr[4],
				'day':     cr[5],
				'hall':    cr[6],
				'row':     cr[7],
				'col':     cr[8],
				'ngenre':  cr[9],
				'cirnam1': cr[10],
				'cirnam2': cr[11],
				'authnam': cr[12],
				'prodnam': cr[13],
				'urlmain': cr[14],
				'mail':    cr[15],
				'desc':    cr[16],
				'x7':      cr[17],  # always blank
				'x':       cr[18],
				'y':       cr[19],
				'x10':     cr[20],
				'subcol':  'ab'[int(cr[21])],
				'x12':     cr[22],  # always blank
				'urlcata': cr[23],
				'urlcirc': cr[24],
				'x13':     cr[25],  # always blank
				'urltwit': cr[26],
				'urlpxiv': cr[27],
				'x14':     cr[28]   # always blank
			}
			v['loc'] = ''.join([v['hall'], v['row'], str(v['col']).rjust(2, '0'), v['subcol']])
			r.append(v)

	for nday, cday in enumerate(all_days, 1):
		print('writing day {}'.format(nday))
		ret = []
		rd = [x for x in r if x['day'] == cday]
		for hallname, rows in sorted(all_halls.items()):
			for row in rows:
				for v in [x for x in rd if x['row'] == row]:
					romaji = jaconv.h2z(v['cirnam2'])
					romaji = romkan.to_roma(romaji)
					entry = {
						"loc": str(nday) + v['loc'],
						"kan": v['cirnam1'],
						"rom": romaji,
						"x": v['x'],
						"y": v['y']
					}

					if v['x12'] or v['x13'] or v['x14']:
						print('\n   !!!!!!!!!!!!!!!!!!!\n')

					urls = []
					for k in ['urlmain','urlcata','urlcirc','urltwit','urlpxiv']:
						url = v[k]
						if '://webcatalog.circle.ms/Circle/' in url \
						or '://portal.circle.ms/Circle/Index' in url \
						or len(url) < 5 \
						or url in urls:
							continue

						urls.append(url)
						
					if urls:
						entry["url"] = urls

					ret.append(entry)
			
		with open('../json/lkrxy{}.json'.format(nday), 'wb') as f:
			f.write(json.dumps(ret, sort_keys=True).replace('"}, {"kan": "', '"},\n{"kan": "').encode('utf-8'))

main()

