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
				'col':     cr[8].rjust(2, '0'),
				'ngenre':  cr[9],
				'cirnam1': cr[10],
				'cirnam2': cr[11],
				'authnam': cr[12],
				'prodnam': cr[13],
				'urlmain': cr[14],
				'mail':    cr[15],
				'desc':    cr[16],
				'x7':      cr[17],  # always blank
				'x8':      cr[18],
				'x9':      cr[19],
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
			v['loc'] = ''.join([v['hall'], v['row'], v['col'], v['subcol']])
			r.append(v)

			#ptab = [ 'day', 'loc', 'ngenre', 'x8', 'x9', 'x10', 'cirnam1' ]
			#for kn in ptab:
			#	print('\033[36m{}\033[33m{:<8}\033[0m '.format(kn, v[kn][:8]), end='')
			#print()
	
			#if False:  # all rows
			#	print()
			#	print(cr)
			#	for n, v in enumerate(cr):
			#		print('  {} {}'.format(n, v))

	#print('counting genres per day')
	wbuf = u''
	for day in all_days:
		p('\nday {}:'.format(day))
		count = {}
		for v in r:
			if v['day'] != day:
				continue
			
			genre = genres[v['ngenre']]
			try:
				count[genre] += 1
			except:
				count[genre] = 1
		
		for k, v in sorted(count.items(), key=operator.itemgetter(1)):
			p('  {:>4} circles: {}'.format(v, k))
	
	with open('../number-of-circles-in-each-genre-per-day.txt', 'wb') as f:
		f.write(wbuf.encode('utf-8'))

	seen = []
	for v in r:
		row = v['row']
		if row not in seen:
			seen.append(row)
	
	#print('rows:', ''.join(seen))
	for row in seen:
		if row not in all_rows:
			raise Exception('row not in all_rows: {}'.format(row))
	
	for x, rowset in all_halls.items():
		for row in rowset:
			if row not in all_rows:
				raise Exception('hallrow not in all_rows: {}'.format(row))
	
	for row in all_rows:
		found = False
		for x, rowset in all_halls.items():
			if row in rowset:
				found = True
				break
		
		if not found:
			raise Exception('row not found in hall: {}'.format(row))
	
	with open('csv2html-01-by-day-and-hall.html', 'rb') as f:
		header = f.read()
	
	if False:
		# debug: show info about a particular row
		for nday, cday in enumerate(all_days, 1):
			for v in r:
				if v['day'] != cday:
					continue

				if v['row'] != e1[1]:
					continue

				ptab = [ 'day', 'loc', 'ngenre', 'x8', 'x9', 'x10', 'cirnam1' ]
				for kn in ptab:
					print('\033[36m{}\033[33m{:<8}\033[0m '.format(kn, v[kn][:8]), end='')
				print()

	loc_ckanji_map = {}
	loc_cromaji_map = {}
	for nday, cday in enumerate(all_days, 1):
		rd = [x for x in r if x['day'] == cday]
		for hallname, rows in sorted(all_halls.items()):
			print('writing day {} hall {}'.format(nday, hallname))
			for row in rows:
				#row_fn = jaconv.z2h(row, kana=False)
				#row_fn = jaconv.h2z(row_fn, ascii=False)
				row_fn = unicodedata.normalize('NFKC', row)
				#row_fn = row
				with open('../html/by-day-and-hall/day{}-{}-{}.html'.format(nday, hallname, row_fn), 'wb') as f:
					f.write(header)
					rdh = [x for x in rd if x['row'] == row]
					if not rdh:
						f.write(b'<img class="nothing" src="/ed/c95/img2/nothing.png" />')

					for v in rdh:
						#romaji = romkan.to_hepburn(v['cirnam2'])
						romaji = jaconv.h2z(v['cirnam2'])
						#romaji = jaconv.kata2hira(romaji)
						#romaji = jaconv.kana2alphabet(romaji)
						romaji = romkan.to_roma(romaji)
						#f.write(u'<tr><td>{}</td><td>{}</td></tr>'.format(v['cirnam1'], romaji).encode('utf-8'))
						loc_ckanji_map['{}{}'.format(nday, v['loc'])] = v['cirnam1']
						loc_cromaji_map['{}{}'.format(nday, v['loc'])] = romaji
						urls = []
						for k in ['urlmain','urltwit','urlpxiv']:
							if k in v and len(v[k]) > 0:
								url = html.escape(v[k])
								urls.append('<span class="url">{}: <a href="{}">{}</a></span>'.format(
									k[3:], url, url))

						f.write(u'<div class="c"><img src="/ed/c95/img/{}.png"><h1>{}</h1><h2>{} | {}</h2><span class="genre">{}</span>{}</div>\n'.format(
							v['imageid'], html.escape(v['cirnam1']), v['loc'], romaji, genres[v['ngenre']], '\n'.join(urls)).encode('utf-8'))
	
	with open('csv2html-basic-table.html', 'rb') as f:
		head = f.read()
	
	for nday in range(1,4):
		with open('../html/sorted-by-location/day{}.html'.format(nday), 'wb') as f:
			f.write(head)
			for k, v in sorted(loc_ckanji_map.items()):
				if k[0] != str(nday):
					continue

				f.write('<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(loc_cromaji_map[k], k, v).encode('utf-8'))
			f.write(b'</table></body></html>')
	
	with open('../html/sorted-by-circle-romaji.html', 'wb') as f:
		f.write(head)
		for k, v in sorted(loc_cromaji_map.items(), key=operator.itemgetter(1)):
			f.write('<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(loc_cromaji_map[k], k, loc_ckanji_map[k]).encode('utf-8'))
		f.write(b'</table></body></html>')
	
	with open('../html/sorted-by-circle-kanji.html', 'wb') as f:
		f.write(head)
		for k, v in sorted(loc_ckanji_map.items(), key=operator.itemgetter(1)):
			f.write('<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(loc_cromaji_map[k], k, loc_ckanji_map[k]).encode('utf-8'))
		f.write(b'</table></body></html>')

	#for v in r:
	#	print(v['day'])

main()

