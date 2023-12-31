import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

matplotlib.use("TkAgg")

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

matplotlib.use("TkAgg")


class Shape():
    def __init__(self, coords, color=""):
        self.coords = coords
        self.x_y_upper_right = (0, 0)
        self.x_y_lower_right = (0, 0)
        self.x_y_lower_left = (0, 0)
        self.x_y_upper_left = (0, 0)
        self.color = color

    def get_x(self):
        points = self.list_points()
        l = [point[0] for point in points]
        return l

    def get_y(self):
        return [point[1] for point in self.list_points()]

    @staticmethod
    def draw(list_of_figures):
        codes = []
        vertices = []
        x = []
        y = []
        colors = []

        for figure in list_of_figures:
            vertices += figure.list_points()
            vertices.append((0, 0))
            codes += [Path.MOVETO] + [Path.LINETO]*(len(figure.list_points())-1) + [Path.CLOSEPOLY]
            x.append(figure.get_x())
            y.append(figure.get_y())
            colors.append(figure.color)
        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='none', edgecolor='green')
        fig, ax = plt.subplots()
        ax.add_patch(pathpatch)
        ax.autoscale_view()
        ax.add_patch(pathpatch)
        ax.autoscale_view()
        for i in range(len(x)):
            ax.fill(x[i], y[i], colors[i])
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
    type = "trapezoid"

    def __init__(self, x_y_upper_right, x_y_lower_right, x_y_lower_left, x_y_upper_left, color=""):
        self.x_y_upper_right, self.x_y_upper_left = (x_y_upper_right, x_y_upper_left)
        self.x_y_lower_right, self.x_y_lower_left = (x_y_lower_right, x_y_lower_left)
        self.coords = x_y_lower_left
        self.color = color

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
    type="square"

    # coordinate == lower left corner
    def __init__(self, a, coord, color=""):
        self.x_y_upper_right, self.x_y_upper_left = ((coord[0]+a, coord[1]+a), (coord[0], coord[1]+a))
        self.x_y_lower_right, self.x_y_lower_left = ((coord[0]+a, coord[1]), coord)
        self.coords = coord
        self.top = a
        self.base = a
        self.side_right = a
        self.side_left = a
        self.color = color

    def move(self, coord):
        x_dif = coord[0] - self.coords[0]
        y_dif = coord[1] - self.coords[1]
        self.x_y_lower_left = coord
        self.x_y_lower_right = (self.x_y_lower_right[0]+x_dif, self.x_y_lower_right[1]+y_dif)
        self.x_y_upper_right = (self.x_y_upper_right[0] + x_dif, self.x_y_upper_right[1] + y_dif)
        self.x_y_upper_left = (self.x_y_upper_left[0] + x_dif, self.x_y_upper_left[1] + y_dif)

    @property
    def square(self):
        return self.base**2

    @property
    def perimeter(self):
        return self.base*4


class C3(Shape):
    type = "pentagon"

    def __init__(self, coord, radius, color=""):
        self.coords = coord
        self.radius = radius
        vertices = []
        angle_offset = 72

        for i in range(5):
            angle = math.radians((90 - angle_offset / 2 + i * angle_offset)+180)
            x = self.coords[0] + self.radius * math.cos(angle)
            y = self.coords[1] + self.radius * math.sin(angle)
            vertices.append((x, y))

        self.vertices = vertices
        self.color = color

    def list_points(self):
        return self.vertices

    def list_edges(self):
        return [[self.vertices[0], self.vertices[1]], [self.vertices[1], self.vertices[2]], [self.vertices[2], self.vertices[3]], [self.vertices[3], self.vertices[4]], [self.vertices[4], self.vertices[0]]]

    def move(self, coord):
        self.coords = coord
        vertices = []
        angle_offset = 72

        for i in range(5):
            angle = math.radians((90 - angle_offset / 2 + i * angle_offset) + 180)
            x = self.coords[0] + self.radius * math.cos(angle)
            y = self.coords[1] + self.radius * math.sin(angle)
            vertices.append((x, y))

        self.vertices = vertices

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
    trapezoid3 = C1((15, 15), (19, 10), (8, 10), (10, 15))
    trapezoid4 = C1((2, 4), (4, 0), (0, 0), (0, 4))
    trapezoid5 = C1((20, 25), (25, 20), (15, 20), (15, 25))
    square1 = C2(2, (2, 1))
    square2 = C2(3, (20, 20))
    square3 = C2(1, (8, 4))
    square4 = C2(1, (10, 10))
    square5 = C2(2, (10, 18))
    pentagon1 = C3((1, 1), 1, "#16a085")
    pentagon2 = C3((8, 8), 4, "#ffc300")
    pentagon3 = C3((5, 3), 1, "#ffc300")
    pentagon4 = C3((10, 20), 2, "#ffc300")
    pentagon5 = C3((12, 10), 3, "#ffc300")
    trapezoid2.fill("#ff5733")
    shapes = [trapezoid1, trapezoid2, trapezoid3, trapezoid4, trapezoid5, square1, square2, square3, square4, square5, pentagon1, pentagon2, pentagon3, pentagon4, pentagon5]
    trapezoid2.move((4, 4))
    trapezoid2.fill("#ff5733")
    Shape.draw(shapes)
    i=0
    j=0
    for shape_x in shapes:
        i+=1
        print(f"Shape №{i}, type: {shape_x.type}")
        print(f"Square = {shape_x.square}")
        print(f"Color = {shape_x.color}")
        print(f"Perimeter = {shape_x.perimeter}")
        for shape_y in shapes:
            j+=1
            if (shape_x!=shape_y):
                Shape.compare(trapezoid1, trapezoid2)
                print(f"Intersection between shape№{i} and shape№{j}: {Shape.is_intersect(shape_x, shape_y)}")
                print(f"Shape№{i} includes shape№{j}: {Shape.is_include(shape_x, shape_y)}")
        j=0


