
import neat
import os
from Failid.objects import *
def main(genomes, config):
    nets = []
    ge = []
    cars = []
    points = []
    time = Timer(60, 1, 200)
    result = []
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(car(g))
        g.fitness = 0
        ge.append(g)
    window = pyglet.window.Window(800, 600)
    image_bg = pyglet.resource.image("map.png")
    points_map1(cars, points)
    @window.event
    def update(dt):
        window.clear()
        Timer.addTime(time)
        if time.frame >= time.limit:
            time.frame = 1
            window.close()
            pyglet.app.exit()
            results = open("results.txt", "r")
            res = results.read()
            results.close()
            resultss = open("results.txt", "w")
            resultss.write(res + "\n" + str(sum(result) / len(result)))
            resultss.close()
    @window.event
    def on_draw():
        window.clear()
        image_bg.blit(0, 0)
        for x,i in enumerate(cars):
            if time.frame%5 == 0:
                output = nets[x].activate((car.distance(i)[0], car.distance(i)[1], car.distance(i)[2], car.distance(i)[3]))
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
                ge[x].fitness-=1
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
    pyglet.clock.schedule_interval(update, 1/30.0)
    pyglet.app.run()
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