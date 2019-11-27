from tkinter import Tk, Canvas
from random import randint

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True

control_s1 = {'Down': (0, 1), 'Right': (1, 0),
			'Up': (0, -1), 'Left': (-1, 0)}

control_s2 = {'s': (0, 1), 'd': (1, 0),
			'w': (0, -1), 'a': (-1, 0)}


def create_block():
	global BLOCK
	posx = SEG_SIZE * randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
	posy = SEG_SIZE * randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
	BLOCK = c.create_oval(posx, posy,
						  posx+SEG_SIZE, posy+SEG_SIZE,
						  fill="red")


class Segment():
	def __init__(self, x, y, color):
		self.instance = c.create_rectangle(x, y,
										   x+SEG_SIZE, y+SEG_SIZE,
										   fill=color)
		

class Snake():
	def __init__(self, x, y, control, color):
		self.segments = [Segment(x+SEG_SIZE, y+SEG_SIZE, color),
						Segment(x+SEG_SIZE*2, y+SEG_SIZE, color),
						Segment(x+SEG_SIZE*3, y+SEG_SIZE, color)]
		self.control = control
		self.vector = (1, 0)
		self.color = color

	def move(self):
		for index in range(len(self.segments)-1):
			segment = self.segments[index].instance
			x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
			c.coords(segment, x1, y1, x2, y2)

		x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
		c.coords(self.segments[-1].instance,
				 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
				 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

	@staticmethod
	def change_direction(event):
		if event.keysym in s1.control:
			s1.vector = s1.control[event.keysym]
		if event.keysym in s2.control:
			s2.vector = s2.control[event.keysym]

	def get_head_coords(self):
		return c.coords(self.segments[-1].instance)

	def add_segment(self):
		last_seg = c.coords(self.segments[0].instance)
		x = last_seg[2] - SEG_SIZE
		y = last_seg[3] - SEG_SIZE
		self.segments.insert(0, Segment(x, y, self.color))

	def reset_segment(self):
		for segment in self.segments:
			c.delete(segment.instance)


def restart():
	global IN_GAME
	s1.reset_segment()
	s2.reset_segment()
	IN_GAME = True
	c.delete(BLOCK)
	start_game()


def start_game():
	global s1, s2
	s1 = Snake(40, 40, control_s1, 'red')
	s2 = Snake(40, 500, control_s2, 'blue')
	create_block()
	main()


def main():
	global IN_GAME
	if IN_GAME:
		c.bind("<KeyPress>", Snake.change_direction)
		s1.move()
		s2.move()
		for s in (s1, s2):
			x1, y1, x2, y2 = s.get_head_coords()
			if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
				IN_GAME = False
			elif s.get_head_coords() == c.coords(BLOCK):
				s.add_segment()
				c.delete(BLOCK)
				create_block()
			else:
				for index in range(len(s.segments)-1):
					if s.get_head_coords() == c.coords(s.segments[index].instance):
						IN_GAME = False
		root.after(100, main)
	else:
		restart()




if __name__ == '__main__':
	root = Tk()
	root.title("Snake")
	root.resizable(False, False)
	c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#DAA520")
	c.grid()
	c.focus_set()
	start_game()
	root.mainloop()	