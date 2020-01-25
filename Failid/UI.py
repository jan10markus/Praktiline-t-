from neat import Checkpointer

from Failid.UIdef import *

window = Tk()
window.title("AI")
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

def load_save():
    w = Tk()
    w.title("Lae salvestus")
    w.geometry("220x100")
    failinimi_label = ttk.Label(w, text="Salvustuse nimi:")
    failinimi_label.grid(row=0, column=0, sticky=(W, N))
    failinimi_entry = ttk.Entry(w)
    failinimi_entry.grid(row=0, column=1, sticky=(W, N))

    def failinimi():
        failinimi = failinimi_entry.get()
        pop = int(populatsioon.get())
        config_mainfile_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get())
        config_inputs("config.txt", calculate_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get()))
        config_fitness_threshold("config.txt", pop)
        p = Checkpointer.restore_checkpoint(failinimi)
        p.add_reporter(neat.StdOutReporter())
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(5))
        p.run(main, pop)
        winner = p.run(main, pop)
        print('\nBest genome:\n{!s}'.format(winner))

    failinimi_button = ttk.Button(w, text="Lae salvestus", command=failinimi)
    failinimi_button.grid(row=1,column=1,sticky=(W,N))

def run_main():
    pop = int(populatsioon.get())
    config_mainfile_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get())
    config_inputs("config.txt", calculate_inputs(kaugus.get(), e_asukoht.get(), p_asukoht.get()))
    config_fitness_threshold("config.txt", pop)
    window.destroy()
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

lae = ttk.Button(window, text="Lae salvestus", command=load_save)
lae.grid(row=11, column=0, sticky=W)

mainloop()
