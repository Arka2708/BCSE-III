.model small
.data
  keyScancode db 0
  cursorPos dw 0
  videoMode db 3

  ; Create a mapping table for Bangla characters (limited)
  banglaMap db 'abcdefghijklmnopqrstuvwxyz', 'অবকডইজহ', 0

.code
  org 100h  ; Entry point

start:
  ; Initialize data segment
  mov ax, @data
  mov ds, ax

  ; Set up interrupt vector for keyboard (IRQ1)
  mov ax, 2501h
  mov dx, offset keyboard_isr
  int 21h

  ; Set video mode
  mov ah, 0
  mov al, videoMode
  int 10h

  ; Infinite loop to wait for keyboard input
keyboard_loop:
  ; Wait for a key press
  mov ah, 0
  int 16h

  ; Display scancode
  mov ah, 0Eh  ; Teletype output
  mov al, keyScancode
  add al, 48
  int 10h

  ; Map the scancode to Bangla character
  mov si, ax  ; Use SI register for indexing
  mov al, [banglaMap + si]

  ; Display Bangla character
  mov ah, 9
  lea dx, [banglaMap + si + 26]  ; Adjust the offset for Bangla characters
  int 21h

  ; Update cursor position (if necessary)
  mov ah, 2
  mov bh, 0
  mov dh, 0
  mov dl, cursorPos
  int 10h

  ; Repeat the loop
  jmp keyboard_loop

  ; Keyboard interrupt handler
keyboard_isr:
  push ax
  in al, 60h  ; Read scancode from the keyboard controller

  ; Handle other keyboard input and character mapping here

  pop ax
  iret

  ; End of program
  int 20h

end start
