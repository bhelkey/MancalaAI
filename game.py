import pickle
from random import randint
def heuristic(gameState, maxPlayer):
	dif = gameState.board[gameState.get_goal(maxPlayer)]
	dif -= gameState.board[gameState.get_goal(not maxPlayer)]

	active = 0
	for i in gameState.get_side(not maxPlayer):
		active -= gameState.board[i]
			
	for i in gameState.get_side(maxPlayer):
		active += gameState.board[i]
		
	activeMod = .3
	modifier = 1 if maxPlayer else -1
	if len(gameState.get_moves(maxPlayer)) == 0:
		modifier = 100 if maxPlayer else -100
		activeMod = 1

	return modifier * (dif + active * activeMod)

def alphabeta(gameState, depth, alpha, beta, maxPlayer):
	
	if str(gameState.board) + str(maxPlayer) in storedResults:
		d, v, m = storedResults[str(gameState.board) + str(maxPlayer)]
		if d > depth:
			return v, m
				
	result = None	
	bestMove = None
	
	if depth == 0 or len(gameState.get_moves(maxPlayer)) == 0:
		result = heuristic(gameState, maxPlayer), bestMove
		
	elif maxPlayer:
		value = -1000000
		for curMove in gameState.get_moves(maxPlayer):
			child = gameState.make_move(curMove)

			moveValue, altMove = alphabeta(child, depth - 1, alpha, beta, False)
			
			if moveValue > value:
				value = moveValue
				bestMove = curMove
				
			alpha = max(alpha, moveValue)
			if beta <= alpha:
				break
		result = value, bestMove
	else:
		value = 1000000
		for curMove in gameState.get_moves(maxPlayer):
			child = gameState.make_move(curMove)

			moveValue, altMove = alphabeta(child, depth - 1, alpha, beta, True)
			
			if moveValue < value:
				value = moveValue
				bestMove = curMove
				
			beta = min(beta, moveValue)
			if beta <= alpha:
				break
		result = value, bestMove
	if depth > 5:
		storedResults[str(gameState.board) + str(maxPlayer)] = depth, result[0], result[1]
	return result

class GameState:
	def __init__(self, gameState = None):
		self.new_game()
		if gameState != None:
			self.board = gameState.board[:]

	def new_game(self):
		self.spacing = 3
		self.set_board_to_start()
		
	def set_board_to_start(self):
		self.board = [0]
		for i in range(6):
			self.board.append(4)
		self.board.append(0)
		for i in range(6):
			self.board.append(4)

	def get_goal(self, maxPlayer):
		return 7 if maxPlayer else 0
	
	def get_side(self, maxPlayer):
		side = []
		start = self.get_goal(maxPlayer) + 1
		for i in range(start, start + 6):
			side.append(i)
		return side

	def get_moves(self, maxPlayer):
		moves = []
		for i in self.get_side(maxPlayer):
			if not self.board[i] == 0:
				moves.append(i)
		return moves

	def make_move(self, move):
		maxSide = self.get_side(True)
		minSide = self.get_side(False)

		maxPlayer = move in maxSide
		playerSide = maxSide if maxPlayer else minSide
		
		child = GameState(self)
		if(move < 0 or len(child.board) <= move or child.board[move] == 0):
			print("move invalid")
			return child
		
		piecesLeft = child.board[move]
		child.board[move] = 0
		position = move
		while piecesLeft > 0:
			position = (position - 1) % len(child.board)
			child.board[position] += 1
			piecesLeft -= 1

		if position in playerSide and child.board[position] == 1 and child.board[14 - position] != 0:
			child.board[child.get_goal(maxPlayer)] += child.board[position] + child.board[14 - position]
			child.board[14 - position] = 0
			child.board[position] = 0
			
		return child

	def print_board_w_label(self):
		self.print_board(self.board)
		
		print()
		
		self.print_board(range(len(self.board)))

	def format_character(self, length, charater):
		line = ""
		for i in range(length):
			line += charater
		return line

	def format_line(self, length):
		return self.format_character(length, '-')

	def format_cell(self, toPrintLine, value):
		toPrintLine += '|' + repr(value).center(self.spacing)
		return toPrintLine 

	def format_long_cell(self, toPrintArray, value):
		toPrintArray[0] += '|' + self.format_character(self.spacing, ' ')
		toPrintArray[1] += '|' + repr(value).center(self.spacing)
		toPrintArray[2] += '|' + self.format_character(self.spacing, ' ')
		return toPrintArray
	
	def print_board(self, board):
		toPrintArray = ["", "", ""]

		toPrintArray = self.format_long_cell(toPrintArray, board[0])

		for i in range(1, 7):
			toPrintArray[0] = self.format_cell(toPrintArray[0], board[i])
			
		toPrintArray[1] += '|'
		while len(toPrintArray[1]) < len(toPrintArray[0]):
			toPrintArray[1] += '-'

		for i in reversed(range(8, 14)):
			toPrintArray[2] = self.format_cell(toPrintArray[2], board[i])

		toPrintArray = self.format_long_cell(toPrintArray, board[7])

		for i in range(len(toPrintArray)):
			toPrintArray[i] += '|'

		print(self.format_line(len(toPrintArray[0])))
		for i in range(len(toPrintArray)):
			print(toPrintArray[i])
		print(self.format_line(len(toPrintArray[0])))

		
try:		
	with open("storedResults.txt", "rb") as myFile:
	    storedResults = pickle.load(myFile)
except:
	storedResults = {}
	
move = input("(f)irst or (s)econd?: ")
if move == "f":
	delay = True
else:
	delay = False

running = True
gameState = GameState()

if False:
	for i in range(1000):
		print(i)
		v, bestMove = alphabeta(gameState, i, -1000000, 1000000, True)
		with open("storedResults.txt", "wb") as myFile:
		    pickle.dump(storedResults, myFile)

		v, bestMove = alphabeta(gameState, i, -1000000, 1000000, False)
		with open("storedResults.txt", "wb") as myFile:
		    pickle.dump(storedResults, myFile)

if False:
	TestDepth = 11
	for j in range(50):
		print("loop " + str(j))
		gameState = GameState()
		if j % 2 == 1:
			v, bestMove = alphabeta(gameState, TestDepth, -1000000, 1000000, False)
			gameState = gameState.make_move(bestMove)
		for i in range(28):
			print("   step " + str(i))
			v, bestMove = alphabeta(gameState, TestDepth, -1000000, 1000000, True)
			if bestMove is None:
				break
			gameState = gameState.make_move(bestMove)
			
			bestMove = gameState.get_moves(False)
			if bestMove is None:
				break
			if not randint(0,4) == 2:
				moves = gameState.get_moves(False)
				bestMove = moves[randint(0,len(moves) - 1)]
			else:
				v, bestMove = alphabeta(gameState, TestDepth, -1000000, 1000000, False)
			gameState = gameState.make_move(bestMove)
		with open("storedResults.txt", "wb") as myFile:
			pickle.dump(storedResults, myFile)

gameState.print_board_w_label()
while running:
	if delay:
		v, bestMove = alphabeta(gameState, 11, -1000000, 1000000, True)
		print("Best Move: " + str(bestMove))
	newGameState = None
	back = False
	while newGameState is None:
		try:
			move = input("Enter a move: ")
			if move == "q":
				running = False
				newGameState = gameState
			elif move == "wipe":
				storedResults = {}
			elif move == "b":
				back = True
				newGameState = oldGameState
			else:
				newGameState = gameState.make_move(int(move))
		except:
			pass
	if not back:
		oldGameState = gameState
	gameState = newGameState
	gameState.print_board_w_label()
	delay = not delay
	
with open("storedResults.txt", "wb") as myFile:
    pickle.dump(storedResults, myFile)
