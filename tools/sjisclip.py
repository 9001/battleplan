#!/usr/bin/env python3
# coding: utf-8

# sjisclip.py
# 2018, ed <irc.rizon.net>, MIT-licensed
# takes a shift-jis clipboard and turns it into utf-16le
# (which is what windows prefers i think)

import ctypes

CF_TEXT = 1
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x2
GMEM_ZEROINIT = 0x40

k32 = ctypes.windll.kernel32
u32 = ctypes.windll.user32

def fix():
	u32.OpenClipboard(0)
	if not u32.IsClipboardFormatAvailable(CF_TEXT):
		print('no text on clipboard')
		return u32.CloseClipboard()
	
	sjis = u32.GetClipboardData(CF_TEXT)
	lsjis = k32.GlobalLock(sjis)
	text = ctypes.c_char_p(lsjis).value[:]
	k32.GlobalUnlock(lsjis)
	
	print('\n# bytes:\n{}'.format(text))
	text = text.decode('sjis')
	utf16 = text.encode('utf-16le')
	print('\n# text:\n{}'.format(text))
	
	u32.EmptyClipboard()
	alloc_args = GMEM_MOVEABLE | GMEM_ZEROINIT
	handle = k32.GlobalAlloc(alloc_args, len(utf16) + 2)
	pcontents = k32.GlobalLock(handle)
	ctypes.memmove(pcontents, utf16, len(utf16))
	k32.GlobalUnlock(handle)
	u32.SetClipboardData(CF_UNICODETEXT, handle)
	u32.CloseClipboard()

def main():
	print('press enter to translate clipboard from sjis to unicode')
	while True:
		input()
		fix()

main()
