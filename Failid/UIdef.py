from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import neat
import os

from Failid.main_file import run_file
from Failid.objects import *
from Failid.main_file import *

def config_fitness_threshold(name, num):
    file = open(name, "r")
    f = file.read()
    final = ""
    for i in f.split("\n"):
        if "[NEAT]" in i.split():
            final = final + i.split()[0]
        elif "pop_size" in i.split():
            final = final + "\n" + i.split()[0] + " " + i.split()[1] + " " + str(num)
        else:
            final = final + "\n" + i

    file.close()
    filew = open(name, "w")
    filew.write(final)
    filew.close()

def calculate_inputs(distance, self, closest_point, direction, points, time):
    result = 0

    if distance > 0:
        result+=4
    if self > 0:
        result+=2
    if closest_point > 0:
        result+=2
    if direction > 0:
        result+=1
    if points > 0:
        result+=1
    if time > 0:
        result+=1
    return(result)

def config_inputs(name, num):
    file = open(name, "r")
    f = file.read()
    final = ""
    for i in f.split("\n"):
        if "num_inputs" in i.split():
            final = final + "\n" + i.split()[0] + " " + i.split()[1] + " " + str(num)
        else:
            final = final + "\n" + i

    file.close()
    filew = open(name, "w")
    filew.write(final)
    filew.close()

def config_mainfile_inputs(distance, self, closest_point, direction, points, time):
    file = open("main_file.py", "r")
    f = file.read()
    final = ""
    add = ""
    for i in f.split("\n"):
        if "output" in i.split():
            if distance > 0:
                add+="car.distance(i)[0], car.distance(i)[1], car.distance(i)[2], car.distance(i)[3]"
            if self > 0:
                if distance == 0:
                    add+="i.x,i.y"
                if distance == 1:
                    add+=",i.x,i.y"
            if closest_point > 0:
                if add == "":
                    add+="car.nearest_point(i, points)[0],car.nearest_point(i, points)[1]"
                else:
                    add+=",car.nearest_point(i, points)[0], car.nearest_point(i, points)[1]"
            if direction > 0:
                if add == "":
                    add+="i.direction"
                else:
                    add+=",i.direction"
            if points > 0:
                if add == "":
                    add+="i.points"
                else:
                    add+=",i.points"
            if time > 0:
                if add == "":
                    add+="time.frame"
                else:
                    add+=",time.frame"
            print(add)
            final = final + "\n" + "                output = nets[x].activate([" + add +  "])"
        elif f.split("\n").index(i) == 0:
            final = final + i
        else:
            final = final + "\n" + i

    file.close()
    filew = open("main_file.py", "w")
    filew.write(final)
    filew.close()
