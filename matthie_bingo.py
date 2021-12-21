import tkinter as tk
import random as rd
import math as mt
from functools import partial
from tkinter.constants import FALSE, TRUE
import tkinter.messagebox as mb
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.mixer as pm


# Automatische Zeilenumbrüche
def zeilenumbruch(s, l):
    aus = ""
    while len(s) > l:
        p = l-1
        while p > 0 and s[p] not in " -":
            p -= 1
        if p == 0:
            p = l
        aus += s[:p+1] + "\n"
        s = s[p+1:]
    return aus+s


# Funktion für Knopfdruck
def click(num):
    global sounds
    global won
    if not values[num]:
        buttons[num].configure(bg = "green", activebackground="green")
        values[num] = TRUE
        print("Eintrag erreicht:", buttons[num].cget("text").replace("-\n", "").replace("\n", ""))
        if not sounds:
            sounds = initializeSounds()
        pm.music.load("sounds/" + sounds.pop())
        pm.music.play()
    else:
        buttons[num].configure(bg = "white", activebackground="white")
        values[num] = FALSE
    newwon = checkwin()
    if newwon > won:
        print("Du hast gewonnen!")
        mb.showinfo("Du hast gewonnen!", "Matthie hat mal wieder ihre alten Sprüche gebracht und dir damit einen Sieg im Bingo beschert.")
    won = newwon


# Prüft die Anzahl an gefüllten Reihen
def checkwin():
    wins = 0
    # Zeilen
    for i in range(0,25,5):
        if values[i] and values[i+1] and values[i+2] and values[i+3] and values[i+4]:
            wins += 1
    # Spalten
    for i in range(5):
        if values[i] and values[i+5] and values[i+10] and values[i+15] and values[i+20]:
            wins += 1
    # Diagonalen
    if values[0] and values[6] and values[18] and values[24]:
        wins += 1
    if values[4] and values[8] and values[16] and values[20]:
        wins += 1
    return wins


# Füllt Liste der Sounds
def initializeSounds():
    sounds = os.listdir('sounds/')
    rd.shuffle(sounds)
    return sounds


# Füllt Liste der Begriffe
def initializeList():
    list = open('begriffe.txt','r', encoding='utf-8').read().split('\n')
    titel = [zeilenumbruch(s, 15) for s in list]
    rd.shuffle(titel)
    return titel


# Erstellung des Fensters
def initializeGui():
    gui = tk.Tk()
    gui.title("Matthie-Bingo")
    gui.geometry("500x500")
    gui.resizable(0,0)
    buttons = []
    values = []
    for i in range(25):
        if i==12:
            but = tk.Button(text="Free Space", bg = "green", activebackground="green")
            but.place(x=(100*(i%5)), y=(100*(mt.floor(i/5))), height=100, width=100)
            buttons.append(but)
            values.append(TRUE)
        else:
            but = tk.Button(text=list.pop(), command=partial(click, i), bg = "white", activebackground="white")
            but.place(x=(100*(i%5)), y=(100*(mt.floor(i/5))), height=100, width=100)
            buttons.append(but)
            values.append(FALSE) 
    return buttons, values, gui


# Alles initialisieren
print("Viel Spaß beim Bingo zur Schwurbelprinzessin Matthie!")
list = initializeList()
sounds = initializeSounds()
won = 0
pm.init()
buttons, values, gui = initializeGui()
gui.mainloop()