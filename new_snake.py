from tkinter import *
from tkinter.messagebox import showerror
import socket
from pickle import loads, dumps
from re import fullmatch

ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
data = {'coords':None, 'vector':None, 'block':None, 'game':True}

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20



def connection_menu():
	menu = Toplevel()
	menu.title('Connect')
	menu.geometry('300x80')
	menu.resizable(False, False)
	menu.wm_attributes("-topmost", 1)
	up_label = Label(menu, text='Введите IP компьютера на котором\nзапущен сервер или запустите свой.')
	label = Label(menu, text='IP сервера')
	entry = Entry(menu, width=15)

	def connect():
		ip = entry.get()
		if fullmatch(ip_pattern, ip):
			try:
				conn.connect((ip, 14900))
				menu.destroy()
			except socket.error:
				showerror(title='Упс...', message='Ошибка подключения')
		else:
			showerror(title='Упс...', message='Некорректный IP')

	button = Button(menu, text="Connect", command=connect)
	up_label.pack(expand=1)
	label.pack(side=LEFT, expand=1)
	entry.pack(side=LEFT, expand=1)
	button.pack(side=LEFT, expand=1)
	menu.mainloop()

def create_block(block_coords):
	global BLOCK
	if block_coords is not None:
		posx, posy = block_coords
		BLOCK = c.create_oval(posx, posy,
							posx+SEG_SIZE, posy+SEG_SIZE,
							fill="red")
		data['block'] = None

class Segment():
	def __init__(self, x, y, color):
		self.instance = c.create_rectangle(x, y,
										   x+SEG_SIZE, y+SEG_SIZE,
										   fill=color)

class Snake():
	def __init__(self, x, y, color):
		self.segments = [Segment(x+SEG_SIZE*i, y+SEG_SIZE, color) for i in range(1, 4)]
		self.control = {'Down': (0, 1), 'Right': (1, 0),
						'Up': (0, -1), 'Left': (-1, 0)}
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


	def move_in(self, coords):
		for i in range(len(coords)):
			x1, y1, x2, y2 = coords[i]
			segment = self.segments[i].instance
			c.coords(segment, x1, y1, x2, y2)

	def change_direction(self, event):
		if event.keysym in self.control:
			self.vector = self.control[event.keysym]

	def reset_segment(self):
		for segment in self.segments:
			c.delete(segment.instance)

	def my_add_segment(self):
		last_seg = c.coords(self.segments[0].instance)
		x = last_seg[2] - SEG_SIZE
		y = last_seg[3] - SEG_SIZE
		self.segments.insert(0, Segment(x, y, self.color))



	def enemy_add_segment(self, coord):
		x = coord[2]
		y = coord[3]
		self.segments.insert(0, Segment(x, y, self.color))



def send_data():
	data['coords'] = [c.coords(i.instance) for i in my_snake.segments]
	data['vector'] = my_snake.vector
	conn.send(dumps(data))
	

def main():
	global data
	if data['game']:
		c.bind("<KeyPress>", my_snake.change_direction)
		my_snake.move()
		send_data()
		data = loads(conn.recv(2048))
		if data['block'] is not None:
			c.delete(BLOCK)
			create_block(data['block'])
			if len(data['coords']) > len(enemy_snake.segments):
				enemy_snake.enemy_add_segment(data['coords'][0])
			else:
				my_snake.my_add_segment()
		enemy_snake.move_in(data['coords'])

		root.after(100, main)
	else:
		root.destroy()



def restart():
	my_snake.reset_segment()
	enemy_snake.reset_segment()
	c.delete(BLOCK)
	data['game'] = True
	start()



def start():
	global my_snake, enemy_snake
	my_start, enemy_start = loads(conn.recv(64))
	my_snake = Snake(*my_start)
	enemy_snake = Snake(*enemy_start)
	create_block(loads(conn.recv(64)))
	main()

if __name__ == '__main__':
	root = Tk()
	root.title("Snake")
	root.resizable(False, False)
	c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#DAA520")
	c.grid()
	c.focus_set()
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# connection_menu()
	conn.connect(("127.0.0.1", 14900)) #FIXME
	start()
	root.mainloop()
	

