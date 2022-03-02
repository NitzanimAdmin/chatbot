class Button:

    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

    def print_details(self):
        print(self.x_pos, self.y_pos, self.width, self.height)
