import socket
from pickle import dumps, loads
from random import randint

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
S1_COLOR = 'red'
S2_COLOR = 'blue'


def new_block_coords():
	global BLOCK
	posx = SEG_SIZE * randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
	posy = SEG_SIZE * randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
	BLOCK = [posx, posy, posx+SEG_SIZE, posy+SEG_SIZE]
	return posx, posy


def send_block_coords():
	pos = dumps(new_block_coords())
	conn_s1.send(pos)
	conn_s2.send(pos)

def start():
	global GAME
	GAME = True
	s1_start_pos = (40, 40, S1_COLOR)
	s2_start_pos = (40, 500, S2_COLOR)
	start_pos = [s1_start_pos, s2_start_pos]
	conn_s1.send(dumps(start_pos))
	start_pos.reverse()
	conn_s2.send(dumps(start_pos))
	send_block_coords()
	main()


def main():
	global GAME
	while GAME:
		data_s1 = loads(conn_s1.recv(2048))
		data_s2 = loads(conn_s2.recv(2048))
		for data_s in (data_s1, data_s2):
			x1, y1, x2, y2 = data_s['coords'][-1] #Head coords
			if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
				GAME = data_s1['game'] = data_s2['game'] = False
			elif data_s['coords'][-1] == BLOCK:
				last_seg = data_s['coords'][0]
				add_seg = [last_seg[0]-data_s['vector'][0]*SEG_SIZE,
							last_seg[1]-data_s['vector'][1]*SEG_SIZE,
							last_seg[2]-data_s['vector'][0]*SEG_SIZE,
							last_seg[3]-data_s['vector'][1]*SEG_SIZE,]
				data_s['coords'].insert(0, add_seg)
				data_s1['block'] = data_s2['block'] = new_block_coords()
			else:
				for index in range(len(data_s['coords'])-1):
					if data_s['coords'][-1] == data_s['coords'][index]:
						GAME = data_s1['game'] = data_s2['game'] = False
		conn_s1.send(dumps(data_s2))
		conn_s2.send(dumps(data_s1))
	else:
		conn_s1.close()
		conn_s2.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 14900))
sock.listen(2)

conn_s1, addr_s1 = sock.accept()
print('Connect:', addr_s1[0])
conn_s2, addr_s2 = sock.accept()
print('Connect:', addr_s2[0])

start()






