#SingleInstance Force
#c:: {
;MsgBox(WinExist("A"))
A_Clipboard := WinGetTitle("A")
MsgBox("Window Title Copied")
return
}