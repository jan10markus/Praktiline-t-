import pyglet

image_car = pyglet.resource.image("carnool.png")
image_car.anchor_x = image_car.width//2
image_car.anchor_y = image_car.height//2

image_wall = pyglet.resource.image("wall.png")
image_wall.anchor_x = image_wall.width//2
image_wall.anchor_y = image_wall.height//2

death = pyglet.resource.image("death.png")
death.anchor_x = death.width//2
death.anchor_y = death.height//2

class car(pyglet.sprite.Sprite):
    def __init__(self,name):
        self.points = 0
        self.l = False
        self.r = False
        self.alive = True
        self.name = name
        self.direction = 1
        super().__init__(x=150,y=450,img=image_car)
        self.rotation = 45

    def test_finish(self):
        if self.x > 600 and self.y < 201:
            self.rotation = 15
            self.points+=1
            self.x = 0
            self.y = 0
            self.alive = False

    def car_move(self):
        speed = 10
        if self.rotation%360 == 0:
            self.y+=speed
            self.direction=0
        if self.rotation%360 == 45:
            self.y+=(speed/2)+1
            self.x+=(speed/2)+1
            self.direction=1
        if self.rotation%360 == 90:
            self.x+=speed
            self.direction=2
        if self.rotation%360 == 135:
            self.y-=(speed/2)+1
            self.x+=(speed/2)+1
            self.direction=3
        if self.rotation%360 == 180:
            self.y-=speed
            self.direction=4
        if self.rotation%360 == 225:
            self.y-=(speed/2)+1
            self.x-=(speed/2)+1
            self.direction=5
        if self.rotation%360 == 270:
            self.x-=speed
            self.direction=6
        if self.rotation%360 == 315:
            self.x-=(speed/2)+1
            self.y+=(speed/2)+1
            self.direction=7

    def GetDirection(self):
        return self.direction

    def test_wall(self):
        if self.x < 125 or self.x > 675 or self.y < 125 or self.y > 475:
            self.rotation = 10
            self.alive = False
        if self.x < 625 and self.y > 325 and self.y < 425:
            self.rotation = 10
            self.alive = False
        if self.x > 175 and self.y < 275 and self.y > 175:
            self.rotation = 10
            self.alive = False

    def distance(self):
        if 100 < self.x < 600 and 400 < self.y < 500:
            return(self.x - 100, 700 - self.x, self.y - 400, 500 - self.y)
        elif 600 < self.x < 700 and 400 < self.y < 500:
            return(self.x - 100, 700 - self.x, self.y - 250, 500 - self.y)
        elif 600 < self.x < 700 and 350 < self.y < 400:
            return(self.x - 600, 700 - self.x, self.y - 250, 500 - self.y)
        elif 600 < self.x < 700 and 250 < self.y < 350:
            return(self.x - 100, 700 - self.x, self.y - 250, 500 - self.y)
        elif 200 < self.x < 600 and 250 < self.y < 350:
            return(self.x - 100, 700 - self.x, self.y - 250, 350 - self.y)
        elif 100 < self.x < 200 and 250 < self.y < 350:
            return(self.x - 100, 700 - self.x, self.y - 100, 350 - self.y)
        elif 100 < self.x < 200 and 200 < self.y < 250:
            return(self.x - 100, 200 - self.x, self.y - 100, 350 - self.y)
        elif 100 < self.x < 200 and 100 < self.y < 200:
            return(self.x - 100, 700 - self.x, self.y - 100, 350 - self.y)
        elif 200 < self.x < 700 and 100 < self.y < 200:
            return(self.x - 100, 700 - self.x, self.y - 100, 200 - self.y)
        else:
            return(0,0,0,0)

    def nearest_point(self, points):
        list = []
        for i in points:
            if i.x > self.x:
                a = i.x - self.x
            elif i.x < self.x:
                a = self.x - i.x
            else:
                a = 0
            if i.y > self.y:
                b = i.y - self.y
            elif i.y < self.y:
                b = self.y - i.y
            else:
                b = 0
            list.append(a + b)
        return(points[list.index(min(list))].x, points[list.index(min(list))].y)

    def neural_input(self, points):
        return(car.distance(self), self.x, self.y, car.nearest_point(self, points), self.points)

    def is_dead(self):
        if self.alive == False:
            self.image = death

    def car_main(self):
        car.test_wall(self)
        car.is_dead(self)
        car.test_finish(self)
        car.car_move(self)
        self.draw()

class point_pos(pyglet.sprite.Sprite):
    def __init__(self,xp,yp, image, car_name):
        self.existence = 1
        self.car_name = car_name
        super().__init__(x=xp,y=yp,img=image)

    def test_car_collision(self, car):
        if car.x > self.x-50 and car.x < self.x+50 and car.y > self.y-50 and car.y < self.y+50 and self.car_name == car.name:
            return(1)

    def add_point(self, car):
        car.points += 1
        self.existence = 0
        self.x = 0
        self.y = 0

#lisab punktid kaardile
def points_map1(cars, points):
    for j in cars:
        xa = 400
        #points.append(point_pos(650,375, image_wall, j.name))
        #points.append(point_pos(150, 225, image_wall, j.name))

        for i in range(0, 2):
            points.append(point_pos(xa, 450, image_wall, j.name))
            xa += 250

        xa = 150

        for i in range(0, 3):
            points.append(point_pos(xa, 300, image_wall, j.name))
            xa += 250

        xa = 150

        for i in range(0, 3):
            points.append(point_pos(xa, 150, image_wall, j.name))
            xa += 200

class Timer():
    def __init__(self, frames_in_second, frame, limit):
        self.frame = float(frame)
        self.frames_in_second = float(frames_in_second)
        self.limit = float(limit)

    def addTime(self):
        self.frame+=1

    def toSeconds(self):
        return(self.frame/self.frames_in_second)
