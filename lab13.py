import math
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path


def ray_casting(edges, point):
    xp, yp = point
    crossed = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (x1 == xp and y1 == yp) or (x2 == xp and y2 == yp):
            crossed += 1
        elif (yp < y1) != (yp < y2) and xp < x1 + ((yp-y1)/(y2-y1))*(x2-x1):
            crossed += 1
    if crossed == 0:
        return False
    elif crossed % 2 == 1:
        return True
    else:
        return False


class Shape():
    def __init__(self, coords):
        self.coords = coords
        self.x_y_upper_right = (0, 0)
        self.x_y_lower_right = (0, 0)
        self.x_y_lower_left = (0, 0)
        self.x_y_upper_left = (0, 0)

    def get_x(self):
        points = self.list_points()
        l = [point[0] for point in points]
        return l

    def get_y(self):
        return [point[1] for point in self.list_points()]

    @staticmethod
    def draw(list_of_figures):
        for figure in list_of_figures:
            vertices = figure.list_points()
            vertices.append((0, 0))
            codes = [Path.MOVETO] + [Path.LINETO]*(len(figure.list_points())-1) + [Path.CLOSEPOLY]
            path = Path(vertices, codes)
            pathpatch = PathPatch(path, facecolor='none', edgecolor='green')
            fig, ax = plt.subplots()
            ax.add_patch(pathpatch)
            ax.autoscale_view()
            xs = figure.get_x()
            ys = figure.get_y()
            ax.fill(xs, ys, "b")
        plt.show()

    def list_edges(self):
        return [[self.x_y_upper_right, self.x_y_lower_right], [self.x_y_lower_right, self.x_y_lower_left], [self.x_y_lower_left, self.x_y_upper_left],\
                [self.x_y_upper_left, self.x_y_upper_right]]

    def list_points(self):
        return [self.x_y_upper_right, self.x_y_lower_right, self.x_y_lower_left, self.x_y_upper_left]

    def move(self, coord):
        self.coords = coord

    @staticmethod
    def is_intersect(x, y):
        edges_x = x.list_edges()
        points_y = y.list_points()
        for point in points_y:
            if ray_casting(edges_x, point):
                return True
        return False

    @staticmethod
    def is_include(x, y):
        edges_x = x.list_edges()
        points_y = y.list_points()
        for point in points_y:
            if not (ray_casting(edges_x, point)):
                return False
        return True

    @staticmethod
    def compare(x, y):
        square_x = x.square
        square_y = y.square
        diff = abs(square_x-square_y)
        if square_x > square_y:
            print("The first shape is bigger than the second")
        else:
            print("The second shape is bigger than the first")
        print("Square difference = " + str(diff))
        return diff

    def fill(self, hex):
        self.color = hex

    @property
    def square(self):
        return self.s

    @property
    def perimeter(self):
        return self.p

# trapezoid
class C1(Shape):
    def __init__(self, x_y_upper_right, x_y_lower_right, x_y_lower_left, x_y_upper_left):
        self.x_y_upper_right, self.x_y_upper_left = (x_y_upper_right, x_y_upper_left)
        self.x_y_lower_right, self.x_y_lower_left = (x_y_lower_right, x_y_lower_left)
        self.coords = x_y_lower_left

    def move(self, coord):
        x_dif = coord[0] - self.coords[0]
        y_dif = coord[1] - self.coords[1]
        self.x_y_lower_left = coord
        self.x_y_lower_right = (self.x_y_lower_right[0]+x_dif, self.x_y_lower_right[1]+y_dif)
        self.x_y_upper_right = (self.x_y_upper_right[0] + x_dif, self.x_y_upper_right[1] + y_dif)
        self.x_y_upper_left = (self.x_y_upper_left[0] + x_dif, self.x_y_upper_left[1] + y_dif)

    @property
    def top(self):
        return abs(self.x_y_upper_right[0]-self.x_y_upper_left[0])

    @property
    def base(self):
        return abs(self.x_y_lower_right[0] - self.x_y_lower_left[0])

    @property
    def height(self):
        return abs(self.x_y_upper_right[1]-self.x_y_lower_right[1])

    @property
    def side_left(self):
        return math.sqrt(((self.x_y_lower_left[0]-self.x_y_upper_left[0])**2 + (self.x_y_lower_left[1]-self.x_y_upper_left[1])**2))

    @property
    def side_right(self):
        return math.sqrt((self.x_y_lower_right[0] - self.x_y_upper_right[0]) ** 2 + (
                    self.x_y_lower_right[1] - self.x_y_upper_right[1]) ** 2)

    @property
    def square(self):
        return (self.top+self.base)*0.5*self.height

    @property
    def perimeter(self):
        return self.base+self.top+self.side_left+self.side_right

# square


class C2(Shape):
    # coordinate == lower left corner
    def __init__(self, a, coord):
        self.x_y_upper_right, self.x_y_upper_left = ((coord[0]+a, coord[1]+a), (coord[0], coord[1]+a))
        self.x_y_lower_right, self.x_y_lower_left = ((coord[0]+a, coord[1]), coord)
        self.coords = coord
        self.top = a
        self.base = a
        self.side_right = a
        self.side_left = a

    @property
    def square(self):
        return self.base**2

    @property
    def perimeter(self):
        return self.base*4


class C3(Shape):
    def __init__(self, coord, radius):
        self.coords = coord
        self.radius = radius
        vertices = []
        angle_offset = math.radians(72)

        for i in range(5):
            angle = i * angle_offset
            x = self.coord[0] + self.radius * math.cos(angle)
            y = self.coord[1] + self.radius * math.sin(angle)
            vertices.append((x, y))

        self.vertices = vertices

    def list_points(self):
        return self.vertices

    def list_edges(self):
        return [[self.vertices[0], self.vertices[1], [self.vertices[1], self.vertices[2]], [self.vertices[2], self.vertices[3]], [self.vertices[3], self.vertices[4]], [self.vertices[4], self.vertices[0]]]]

    @property
    def square(self):
        return (5/2)*self.radius**2*math.sin(math.radians(72))

    @property
    def perimeter(self):
        return 5*self.side

    @property
    def side(self):
        return 2*self.radius*math.sin(math.radians(36))


if __name__ == '__main__':
    trapezoid1 = C1((4, 4), (5, 1), (1, 1), (2, 4))
    trapezoid2 = C1((4, 4), (6, 1), (1, 1), (2, 4))
    trapezoid2.move((4, 4))
    Shape.draw([trapezoid2])
    print(trapezoid2.list_points())
    square1 = C2(2, (2, 1))
    print(trapezoid1.square)
    Shape.compare(trapezoid1, trapezoid2)
    print(Shape.is_intersect(trapezoid1, trapezoid2))
    print(Shape.is_intersect(trapezoid2, square1))
    print(Shape.is_include(trapezoid2, square1))



