#Autor Jan Markus Rokka
#Mõningane eeskuju https://neat-python.readthedocs.io/en/latest/

import time as t
import neat
import os
from Failid.objects import *

#genoomide sobilikkust arvutav funktsioon
def main(genomes, config):
    nets = []
    ge = []
    cars = []
    points = []
    time = Timer(60, 1, 50)
    result = []
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(car(g))
        g.fitness = 0
        ge.append(g)
    carsamount = Timer(60, len(ge), 50)
    window = pyglet.window.Window(800, 600)
    window.set_location(100,100)
    image_bg = pyglet.resource.image("map.png")
    points_map1(cars, points)
    integer = 0

    @window.event
    def update(dt):
        if time.frame >= 189:
            window.close()

    @window.event
    def on_draw():
        window.clear()
        image_bg.blit(0, 0)
        for x,i in enumerate(cars):
            if time.frame%5 == 0:
                output = nets[x].activate([car.distance(i)[0], car.distance(i)[1], car.distance(i)[2], car.distance(i)[3],time.frame])
                if output[0] > 0.5:
                    i.l = True
                if output[1] > 0.5:
                    i.r = True
            car.car_main(i)
            if i.l == True:
                i.rotation+=45
                i.l = False
            if i.r == True:
                i.rotation-=45
                i.r = False
            if i.rotation == 10:
                result.append(i.points)
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)
        for i in points:
            for x, j in enumerate(cars):
                if point_pos.test_car_collision(i, j) == 1:
                    point_pos.add_point(i, j)
                    ge[x].fitness+=1
                if j.points >= 17:
                    ge[x].fitness = 17
            if i.existence == 1:
                i.draw()
            if i.existence == 0:
                points.remove(i)
        if integer == 0:
            carsamount.frame = len(cars)
            Timer.addTime(time)
            if time.frame > 190:
                carsamount.frame = -1
                time.frame = -100000
                pyglet.app.exit()
                time.frame = 1

    pyglet.clock.schedule_interval(update, 0.01)
    pyglet.app.run()

#algoritmi käivitamine
def runn(config_file, pop):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter())
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    winner = p.run(main, pop)
    print('\nBest genome:\n{!s}'.format(winner))
def run_file(popul):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    runn(config_path, popul)