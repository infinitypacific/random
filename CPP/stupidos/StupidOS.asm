;Stupid OS
;Made by PACIFIKY!!!
[org 0x7c00]
mov bp, 0x8000
mov sp, bp
push [inputname + 0x7c00]
push [nameo + 0x7c00]
jmp prints
inputname:
push [outj + 0x7c00]
push [namei + 0x7c00]
jmp inps
outj:
push [outc + 0x7c00]
push [namei + 0x7c00]
jmp prints
outc:
push [hltj + 0x7c00]
push [outo + 0x7c00]
hltj:
jmp $

;data:

nameo:
  db "Enter your name>", 0
nami:
  times 255 db 0
outo:
  db " is stupid.", 0

;print string function

prints:
  mov [temp+0x7c00], bx
  pop bx
  push ax
  mov ah, 0x0e
plop:
  mov al, [bx]
  cmp al, 0
  je deinitprints
  int 0x10
  inc bx
  jmp plop
deinitprints:
  mov bx, [temp+0x7c00]
  pop ax
  ret

;Input function

inps:
  mov [temp+0x7c00], bx
  pop bx
  push ax
  mov ah, 0x0e
inplop:
  int 0x16
  cmp al, 10
  je deinitlop
  int 0x10
  mov [bx], al
  inc bx
  jmp implop
deinitinp:
  mov bx, [temp+0x7c00]
  pop ax
  ret

temp:
  db 0

times 510-($-$$) db 0
db 0x55 0xaa