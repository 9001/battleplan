#NoEnv
#Persistent
#SingleInstance, Force
SendMode Input

en := false
ctr := 0

$F1::
	Sleep, 3000
	en := true
	while en {
		Send, 1
		Sleep 20
		Send, 1
		Sleep 20
		Send, 1
		Sleep 20
		Send, {Right}
		ctr += 1
		if (ctr >= 36) {
			ctr = 0
			Sleep 500
		}
		Sleep 20
	}
	return

$F2::
	en := false
	return

$F3::
	ExitApp
	return
