from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import neat
import os

from Failid.main_file import run_file
from Failid.objects import *
from Failid.main_file import *
from Failid.UIdef import *

window = Tk()
window.title("Tehisintelligentsi asi lmao")
window.geometry("150x250")

sisendid_label = ttk.Label(window, text="Sisendid neuronitele:")
sisendid_label.grid(row=0, column=0, sticky=(W,N))

kaugus = IntVar()
Checkbutton(window, text="Enda kaugus seintest", variable=kaugus).grid(row=1,column=0, sticky=W)
e_asukoht = IntVar()
Checkbutton(window, text="Enda asukoht", variable=e_asukoht).grid(row=2, column=0, sticky=W)
p_asukoht = IntVar()
Checkbutton(window, text="Lähima punkti asukoht", variable=p_asukoht).grid(row=3, column=0, sticky=W)

tühi = ttk.Label(window, text="")
tühi.grid(row=5,column=0,sticky=W)

populatsioon_label = ttk.Label(window, text="Populatsiooni suurus:")
populatsioon_label.grid(row=6,column=0, sticky=W)
populatsioon = ttk.Entry(window)
populatsioon.grid(row=7,column=0, sticky=W)

tühi1 = ttk.Label(window, text="")
tühi1.grid(row=8,column=0,sticky=W)

def run_main():
    pop = int(populatsioon.get())
    config_mainfile_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get())
    config_inputs("config.txt", calculate_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get()))
    config_fitness_threshold("config.txt", pop)
    run_file(pop)

    """"try:
        pop = int(populatsioon.get())
        config_inputs("config.txt", calculate_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get()))
        config_fitness_threshold("config.txt", pop)
        run_file(pop)
    except:
        messagebox.showinfo(message="Viga")"""""

run = ttk.Button(window, text="Käivita", command=run_main)
run.grid(row=9, column=0, sticky=W)

mainloop()
