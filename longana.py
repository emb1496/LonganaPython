#     ************************************************************
#     * Name:  Elliott Barinberg                                 *
#     * Project:  Longana in Python					             *
#     * Class:  OPL                                              *
#     * Date:  12/16/17                                          *
#     ************************************************************
import random, sys, os

#Tile Data structure class
class Tile:
	def __init__(self, l, r):
		self.left = l
		self.right = r
	def __repr__(self):
		s = str(self.left) + " - " + str(self.right)
		return s
	def setLeft(self, num):
		self.left = num
	def setRight(self, num):
		self.right = num
	def getLeft(self):
		return self.left
	def getRight(self):
		return self.right

#Player data structure class
class Player:
	def __init__(self, tiles, score):
		self.hand = tiles
		self.score = score
	def addToScore(self, roundScore):
		self.score = self.score + roundScore
	def getHand(self):
		return self.hand
	def __repr__(self):
		s = ""
		for tile in self.hand:
			s += tile.__repr__()
		return s
	def insert(self, tiles):
		self.hand = self.hand + tiles
	def getScore(self):
		return self.score
	def sumPips(self):
		sum = 0
		for tile in self.hand:
			sum = sum + tile.getLeft() + tile.getRight()
		return sum 

#human inherits from player
class Human(Player):
	def __init__(self, tiles, score):
		Player.__init__(self, tiles, score)
	def isComputer(self):
		return False

#computer inherits from player
class Computer(Player):
	def __init__(self, tiles, score):
		Player.__init__(self, tiles, score)
	def isComputer(self):
		return True

#boneyard data structure class
class Boneyard:
	def __init__(self, tiles):
		self.tiles = tiles
	def getTopN(self, n):
		if(n > 1):
			return [self.tiles.pop()] + self.getTopN(n-1)
		if(n == 1):
			return [self.tiles.pop()]

#board data structure class
class Board:
	def __init__(self, board = []):
		self.left = []
		self.right = []
		self.top = []
		self.bottom = []
		self.engine = board
	def __repr__(self):
		s = ""
		s += "   "
		for tile in self.left:
			s+= "    "
		s += "P2"
		s += '\n'
		for tile in reversed(self.top):
			if(tile.getRight() != tile.getLeft()):
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += str(tile.getRight())
				s += "\n"
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += "|"
				s += "\n"
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += str(tile.getLeft())
				s += '\n'
			else:
				s += "   "
				for a_tile in self.left:
					s+= "    "
				s += str(tile.getLeft())
				s += "-"
				s += str(tile.getRight())
				s += "\n"
		s += "   "
		for tile in reversed(self.left):
			if(tile.getLeft() == tile.getRight()):
				s += " "
				s += str(tile.getLeft())
				s += "  "
			else:
				s += "    "
		s += " "
		s += str(self.engine.getRight())
		s += "  "
		for tile in self.right:
			if(tile.getLeft() == tile.getRight()):
				s += " "
				s += str(tile.getLeft())
				s += "  "
			else:
				s += "    "
		s += "\n"
		s += "P1 "
		for tile in reversed(self.left):
			if(tile.getLeft() == tile.getRight()):
				s += " |  "
			else:
				s += str(tile.getRight())
				s += "-"
				s += str(tile.getLeft())
				s += " "
		s += " |  "
		for tile in self.right:
			if(tile.getLeft() == tile.getRight()):
				s += " |  "
			else:
				s += str(tile.getLeft())
				s += "-"
				s += str(tile.getRight())
				s += " "
		s += "P3"
		s += "\n"
		s += "   "
		for tile in reversed(self.left):
			if(tile.getLeft() == tile.getRight()):
				s += " "
				s += str(tile.getLeft())
				s += "  "
			else:
				s += "    "
		s += " "
		s += str(self.engine.getRight())
		s += "  "
		for tile in self.right:
			if(tile.getLeft() == tile.getRight()):
				s += " "
				s += str(tile.getLeft())
				s += "  "
			else:
				s += "    "
		s += "\n"
		for tile in self.bottom:
			if(tile.getRight() != tile.getLeft()):
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += str(tile.getLeft())
				s += "\n"
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += "|"
				s += "\n"
				s += "    "
				for a_tile in self.left:
					s += "    "
				s += str(tile.getRight())
				s += '\n'
			else:
				s += "   "
				for a_tile in self.left:
					s+= "    "
				s += str(tile.getLeft())
				s += "-"
				s += str(tile.getRight())
				s += "\n"
		s += "   "
		for tile in self.left:
			s += "    "
		s += "P4"
		s += '\n'
		return s
	def insert(self, tile):
		self.engine = tile
	def insertLeft(self, tile):
		length = len(self.left)
		if(length == 0):
			if(tile.getLeft() == self.engine.getLeft()) :
				self.left.insert(0, tile)
			elif(tile.getRight() == self.engine.getLeft()):
				l = tile.getLeft()
				r = tile.getRight()
				self.left.insert(0, Tile(r,l))
		elif(self.left[length-1].getRight() == tile.getLeft()):
			self.left.append(tile)
		elif(self.left[length-1].getRight() == tile.getRight()):
			newTile = Tile(tile.getRight(), tile.getLeft())
			self.left.append(newTile)
	def insertTop(self, tile):
		length = len(self.top)
		if(length == 0):
			if(self.engine.getLeft() == tile.getRight()):
				l = tile.getLeft()
				r = tile.getRight()
				self.top.append(Tile(r, l))
			elif(self.engine.getLeft() == tile.getLeft()):
				self.top.insert(0, tile)
		elif(self.top[length-1].getRight() == tile.getLeft()):
			self.top.append(tile)
		elif(self.top[length-1].getRight() == tile.getRight()):
			newTile = Tile(tile.getRight(), tile.getLeft())
			self.top.append(newTile)
	def insertRight(self, tile):
		length = len(self.right)
		if(length == 0):
			if(self.engine.getLeft() == tile.getLeft()):
				self.right.insert(0, tile)
			elif(self.engine.getLeft() == tile.getRight()):
				l = tile.getLeft()
				r = tile.getRight()
				self.right.append(Tile(r, l))
		elif(self.right[length-1].getRight() == tile.getLeft()):
			self.right.append(tile)
		elif(self.right[length-1].getRight() == tile.getRight()):
			newTile = Tile(tile.getRight(), tile.getLeft())
			self.right.append(newTile)
	def insertBottom(self, tile):
		length = len(self.bottom)
		if(length == 0):
			if(self.engine.getLeft() == tile.getLeft()):
				self.bottom.insert(0, tile)
			elif(self.engine.getLeft() == tile.getRight()):
				l = tile.getLeft()
				r = tile.getRight()
				self.bottom.append(Tile(r, l))
		elif(self.bottom[length-1].getRight() == tile.getLeft()):
			self.bottom.append(tile)
		elif(self.bottom[length-1].getRight() == tile.getRight()):
			newTile = Tile(tile.getRight(), tile.getLeft())
			self.bottom.append(newTile)
	def getLeftMostPip(self):
		if(len(self.left) == 0):
			return self.engine.getLeft()
		return self.left[len(self.left)-1].getRight()
	def getTopMostPip(self):
		if(len(self.top) == 0):
			return self.engine.getLeft()
		return self.top[len(self.top)-1].getRight()
	def getRightMostPip(self):
		if(len(self.right) == 0):
			return self.engine.getLeft()
		return self.right[len(self.right)-1].getRight()
	def getBottomMostPip(self):
		if(len(self.bottom) == 0):
			return self.engine.getLeft()
		return self.bottom[len(self.bottom)-1].getRight()

#/* ********************************************************************* 
#Function Name: createTiles 
#Purpose: To return a list of tiles for the game 
#Parameters: 
#            left
#			 right
#Return Value: A tile and recursive call 
#Local Variables: 
#            none 
#Algorithm: 
#            1) If left and right are zero return 0, 0 
#            2) If right is not 0 return the tile and call create tiles with left and right-1
#			 3) If right is 0 call create tiles with left-1,left-1 
#Assistance Received: none 
#********************************************************************* */
def createTiles(left, right):
	if(left == 0 and right == 0):
		return [Tile(left, right)]
	if(left >= 0):
		if(right >= 0):
			return [Tile(left, right)] + (createTiles(left, right-1))
		else:
			return createTiles(left - 1, left - 1)

#/* ********************************************************************* 
#Function Name: drawForEngine 
#Purpose: To have players draw until someone has the engine and set playNext accordingly 
#Parameters: 
#            left
#			 right
#Return Value: [humanplayers, computerplayers, stock, playNExt] 
#Local Variables: 
#            i - counter
#			 humanPlayer - iterator
#			 tile - iterator
#			 computerPlayer - iterator 
#Algorithm: 
#            1) check if human players have the engine, if so set play next and return
#            2) check if computer players have the engine, if so sete playnext and return
#			 3) Loop through players and get 1 tile each from the stock and call draw for engine with the new players and stock
#Assistance Received: none 
#********************************************************************* */
def drawForEngine(engine, humanPlayers, computerPlayers, stock, playNext):
	i = 0
	for humanPlayer in humanPlayers:
		i=i+1
		for tile in humanPlayer.getHand():
			if(tile.getRight() == engine.getRight() and tile.getLeft() == engine.getLeft()):
				print("Human ", i, " has the engine he will place it and the player clockwise will be next to play.")
				if len(humanPlayers) == i:
					playNext = "computer1"
					humanPlayer.getHand().remove(tile)
					return [humanPlayers, computerPlayers, stock, playNext]
				else:
					playNext = "human"+str(i+1)
					humanPlayer.getHand().remove(tile)
					return [humanPlayers, computerPlayers, stock, playNext]
	i = 0
	for computerPlayer in computerPlayers:
		i=i+1
		for tile in computerPlayer.getHand():
			if(tile.getLeft() == engine.getLeft() and tile.getRight() == engine.getRight()):
				print("Computer ", i, " has the engine he will place it and the player clockwise will be next to play.")
				if len(computerPlayers) == i:
					playNext = "human1"
					computerPlayer.getHand().remove(tile)
					return [humanPlayers, computerPlayers, stock, playNext]
				else:
					playNext = "computer"+str(i+1)
					computerPlayer.getHand().remove(tile)
					return [humanPlayers, computerPlayers, stock, playNext]
	for humanPlayer in humanPlayers:
		if(len(stock.tiles) > 0):
			humanPlayer.insert(stock.getTopN(1))
	for computerPlayer in computerPlayers:
		if(len(stock.tiles) > 0):
			computerPlayer.insert(stock.getTopN(1))
	return drawForEngine(engine, humanPlayers, computerPlayers, stock, playNext)

#/* ********************************************************************* 
#Function Name: generateEngine 
#Purpose: To return the Engine based on round number 
#Parameters: 
#            RoundNo
#			 numPlayers
#			 numComputers
#Return Value: A tile 
#Local Variables: 
#            num - variable for the left and right sides of the engine 
#Algorithm: 
#            1) numcomputers+numPlayers is 2 then mod number is 7, otherwise its 10 
#            2) num is roundNo % mod number
#			 3) create tile with left and right being num and return it 
#Assistance Received: none 
#********************************************************************* */
def generateEngine(roundNo, numPlayers, numComputers):
	if(numComputers + numPlayers == 2):
		num = roundNo%7
		num = 7 - num
	else:
		num = roundNo%10
		num = 10 - num
	center = Tile(num, num)
	return center

#/* ********************************************************************* 
#Function Name: validateMove 
#Purpose: To determine if the move is legal and then play it 
#Parameters: 
#            gamestate
#			 playSide - side the player is supposed to be playing on
#			 index - index of tile in player hand to play 
#			 side - side player wants to play on
#Return Value: True - if move success, False - otherwise 
#Local Variables: 
#            Broken douwn gamestate 
#Algorithm: 
#            1) determine who is player then determine if the move is allowed by the rules of the game 
#            2) play the move if it is allowed and if the player is a computer output what the move was
#			 3) return True/False
#Assistance Received: none 
#********************************************************************* */
def validateMove(gameState, playSide, index, side):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	if(playNext == "human1"):
		player = humanPlayers[0]
	elif(playNext == "human2"):
		player = humanPlayers[1]
	elif(playNext == "human3"):
		player = humanPlayers[2]
	elif(playNext == "computer1"):
		player = computerPlayers[0]
	elif(playNext == "computer2"):
		player = computerPlayers[1]
	elif(playNext == "computer3"):
		player = computerPlayers[2]
	tile = player.getHand()[index-1]
	if(len(humanPlayers) == 1 and len(computerPlayers) == 1):
		if(tile.getRight() == tile.getLeft()):
			if(side == 'l'):
				if(tile.getLeft() == board.getLeftMostPip()):
					player.getHand().remove(tile)
					board.insertLeft(tile)
					if(player.isComputer()):
						print("Computer moves ", tile, " to the left")
					return True
			elif(side == 'r'):
				if(tile.getRight() == board.getRightMostPip()):
					player.getHand().remove(tile)
					board.insertRight(tile)
					if(player.isComputer()):
						print("Computer moves ", tile, " to the right")
					return True
		else:
			if(side == playSide):
				if(side == 'l'):
					if(tile.getLeft() == board.getLeftMostPip() or tile.getRight() == board.getLeftMostPip()):
						player.getHand().remove(tile)
						board.insertLeft(tile)
						if(player.isComputer()):
							print("Computer moves ", tile, " to the left")
						return True
				elif(side == 'r'):
					if(tile.getLeft() == board.getRightMostPip() or tile.getRight() == board.getRightMostPip()):
						player.getHand().remove(tile)
						board.insertRight(tile)
						if(player.isComputer()):
							print("Computer moves ", tile, " to the right")
						return True
			else:
				if(passCount > 1):
					if(side == 'l'):
						if(tile.getLeft() == board.getLeftMostPip() or tile.getRight() == board.getLeftMostPip()):
							player.getHand().remove(tile)
							board.insertLeft(tile)
							if(player.isComputer()):
								print("Computer moves ", tile, " to the left")
							return True
					elif(side == 'r'):
						if(tile.getLeft() == board.getRightMostPip() or tile.getRight() == board.getRightMostPip()):
							player.getHand().remove(tile)
							board.insertRight(tile)
							if(player.isComputer()):
								print("Computer moves ", tile, " to the right")
							return True
		return False
	if(tile.getLeft() == tile.getRight()):
		if(side == 'l'):
			if(tile.getLeft() == board.getLeftMostPip()):
				player.getHand().remove(tile)
				board.insertLeft(tile)
				if(player.isComputer()):
					print("Computer moves ", tile, " to the left")
				return True
		elif(side == 't'):
			if(tile.getLeft() == board.getTopMostPip()):
				player.getHand().remove(tile)
				board.insertTop(tile)
				if(player.isComputer()):
					print("Computer moves ", tile, " to the top")
				return True
		elif(side == 'r'):
			if(tile.getLeft() == board.getRightMostPip()):
				player.getHand().remove(tile)
				board.insertRight(tile)
				if(player.isComputer()):
					print("Computer moves ", tile, " to the right")
				return True
		elif(side == 'b'):
			if(tile.getLeft() == board.getBottomMostPip()):
				player.getHand().remove(tile)
				board.insertBottom(tile)
				if(player.isComputer()):
					print("Computer moves ", tile, " to the bottom")
				return True
	if(side == playSide):
		if(side == 'l'):
			print(tile.getRight())
			print(tile.getLeft())
			print(board.getLeftMostPip())
			if(tile.getRight() == board.getLeftMostPip() or tile.getLeft() == board.getLeftMostPip()):
				player.getHand().remove(tile)
				board.insertLeft(tile)
				if(player.isComputer() == True):
					print("Computer moves ", tile, " to the left")
				return True
		elif(side == 't'):
			leftPip = tile.getLeft()
			rightPip = tile.getRight()
			topPip = board.getTopMostPip()
			if(rightPip == topPip or leftPip == topPip):
				player.getHand().remove(tile)
				board.insertTop(tile)
				if(player.isComputer() == True):
					print("Computer moves ", tile, " to the top")
				return True
		elif(side == 'r'):
			if(tile.getRight() == board.getRightMostPip() or tile.getLeft() == board.getRightMostPip()):
				player.getHand().remove(tile)
				board.insertRight(tile)
				if(player.isComputer() == True):
					print("Computer moves ", tile, " to the right")				
				return True
		else:
			if(tile.getRight() == board.getBottomMostPip() or tile.getLeft() == board.getBottomMostPip()):
				player.getHand().remove(tile)
				board.insertBottom(tile)
				if(player.isComputer() == True):
					print("Computer moves ", tile, " to the bottom")
				return True
	else:
		if(passCount >= 3):
			if(side == 'l'):
				if(tile.getRight() == board.getLeftMostPip() or tile.getLeft() == board.getLeftMostPip()):
					player.getHand().remove(tile)
					board.insertLeft(tile)
					if(player.isComputer() == True):
						print("Computer moves ", tile, " to the left")
					return True
			elif(side == 't'):
				if(tile.getRight() == board.getTopMostPip() or tile.getLeft() == board.getTopMostPip()):
					player.getHand().remove(tile)
					board.insertTop(tile)
					if(player.isComputer() == True):
						print("Computer moves ", tile, " to the top")
					return True
			elif(side == 'r'):
				if(tile.getRight() == board.getRightMostPip() or tile.getLeft() == board.getRightMostPip()):
					player.getHand().remove(tile)
					board.insertRight(tile)
					if(player.isComputer() == True):
						print("Computer moves ", tile, " to the right")
					return True
			else:
				if(tile.getRight() == board.getBottomMostPip() or tile.getLeft() == board.getBottomMostPip()):
					player.getHand().remove(tile)
					board.insertBottom(tile)
					if(player.isComputer() == True):
						print("Computer moves ", tile, " to the bottom")
					return True
		if(passCount == 2):
			if(playSide == 'l'):
				if(side == 'b'):
					if(tile.getRight() == board.getBottomMostPip() or tile.getLeft() == board.getBottomMostPip()):
						player.getHand().remove(tile)
						board.insertBottom(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the bottom")
						return True
				elif(side == 'r'):
					if(tile.getRight() == board.getRightMostPip() or tile.getLeft() == board.getRightMostPip()):
						player.getHand().remove(tile)
						board.insertRight(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the right")
						return True
			elif(playSide == 't'):
				if(side == 'l'):
					if(tile.getRight() == board.getLeftMostPip() or tile.getLeft() == board.getLeftMostPip()):
						player.getHand().remove(tile)
						board.insertLeft(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the left")
						return True
				elif(side == 'b'):
					if(tile.getRight() == board.getBottomMostPip() or tile.getLeft() == board.getBottomMostPip()):
						player.getHand().remove(tile)
						board.insertBottom(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the bottom")
						return True
			elif(playSide == 'r'):
				if(side == 't'):
					if(tile.getRight() == board.getTopMostPip() or tile.getLeft() == board.getTopMostPip()):
						player.getHand().remove(tile)
						board.insertTop(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the top")
						return True
				elif(side == 'l'):
					if(tile.getRight() == board.getLeftMostPip() or tile.getLeft() == board.getLeftMostPip()):
						player.getHand().remove(tile)
						board.insertLeft(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the left")
						return True
			else:
				if(side == 'r'):
					if(tile.getRight() == board.getRightMostPip() or tile.getLeft() == board.getRightMostPip()):
						player.getHand().remove(tile)
						board.insertRight(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the right")
						return True
				elif(side == 't'):
					if(tile.getRight() == board.getTopMostPip() or tile.getLeft() == board.getTopMostPip()):
						player.getHand().remove(tile)
						board.insertTop(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the top")
						return True
		elif(passCount == 1):
			if(playSide == 'l'):
				if(side == 'b'):
					if(tile.getRight() == board.getBottomMostPip() or tile.getLeft() == board.getBottomMostPip()):
						player.getHand().remove(tile)
						board.insertBottom(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the bottom")
						return True
			elif(playSide == 't'):
				if(side == 'l'):
					if(tile.getRight() == board.getLeftMostPip() or tile.getLeft() == board.getLeftMostPip()):
						player.getHand().remove(tile)
						board.insertLeft(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the left")
						return True
			elif(playSide == 'r'):
				if(side == 't'):
					if(tile.getRight() == board.getTopMostPip() or tile.getLeft() == board.getTopMostPip()):
						player.getHand().remove(tile)
						board.insertTop(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the top")
						return True
			else:
				if(side == 'r'):
					if(tile.getRight() == board.getRightMostPip() or tile.getLeft() == board.getRightMostPip()):
						player.getHand().remove(tile)
						board.insertRight(tile)
						if(player.isComputer() == True):
							print("Computer moves ", tile, " to the right")
						return True
	return False

#/* ********************************************************************* 
#Function Name: humanHasLegalMove 
#Purpose: To determine if a human player has a legal move 
#Parameters: 
#            humanPlayer
#			 playSide - side the player is supposed to be playing on
#			 board - the Board 
#			 passCount - how many players have passed in the lead up
#			 stock - the boneyard
#Return Value: True - if has move, False - otherwise 
#Local Variables: 
#            top, left, right, bottom - the edges of the board 
#Algorithm: 
#            1) check all possible moves in the human hand 
#            2) if any move is allowed return True
#			 3) return false
#Assistance Received: none 
#********************************************************************* */
def humanHasLegalMove(humanPlayer, board, stock, passCount, playSide):
	top=board.getTopMostPip()
	left = board.getLeftMostPip()
	right = board.getRightMostPip()
	bottom = board.getBottomMostPip()
	for tile in humanPlayer.getHand():
		if(tile.getLeft() == tile.getRight()):
			if(tile.getLeft() == top or tile.getLeft() == left or tile.getLeft() == right or tile.getLeft() == bottom):
				return True
		if(playSide == 'l'):
			if(tile.getLeft() == left or tile.getRight() == left):
				return True
			if(passCount >= 3):
				if(tile.getLeft() == right or tile.getLeft() == bottom or tile.getLeft() == top):
					return True
				elif(tile.getRight() == right or tile.getRight() == bottom or tile.getRight() == top):
					return True
			elif(passCount == 2):
				if(tile.getLeft() == right or tile.getLeft() == bottom):
					return True
				elif(tile.getRight() == right or tile.getRight() == bottom):
					return True
			elif(passCount == 1):
				if(tile.getLeft() == bottom):
					return True
				elif(tile.getRight() == bottom):
					return True
		elif(playSide == 't'):
			if(tile.getLeft() == top or tile.getRight() == top):
				return True
			if(passCount >= 3):
				if(tile.getLeft() == right or tile.getLeft() == bottom or tile.getLeft() == left):
					return True
				elif(tile.getRight() == right or tile.getRight() == bottom or tile.getRight() == left):
					return True
			elif(passCount == 2):
				if(tile.getLeft() == bottom or tile.getLeft() == left):
					return True
				elif(tile.getRight() == bottom or tile.getRight() == left):
					return True
			elif(passCount == 1):
				if(tile.getLeft() == left):
					return True
				elif(tile.getRight() == left):
					return True
		elif(playSide == 'r'):
			if(tile.getLeft() == right or tile.getRight() == right):
				return True
			if(passCount >= 3):
				if(tile.getLeft() == top or tile.getLeft() == bottom or tile.getLeft() == left):
					return True
				elif(tile.getRight() == top or tile.getRight() == bottom or tile.getRight() == left):
					return True
			elif(passCount == 2):
				if(tile.getLeft() == top or tile.getLeft() == left):
					return True
				elif(tile.getRight() == top or tile.getRight() == left):
					return True
			elif(passCount == 1):
				if(tile.getLeft() == top):
					return True
				elif(tile.getRight() == top):
					return True
	return False

#/* ********************************************************************* 
#Function Name: getHelp 
#Purpose: To give the human a hint 
#Parameters: 
#            gamestate
#			 whichHuman - index of which human is trying to play
#Return Value: none
#Local Variables: 
#            Broken douwn gamestate
#			 Best order - rearranged list of human tiles
#  			 top, left, right, bottom - edges of the board
#Algorithm: 
#            1) determine who is player 
#			 2) rearrange their tiles into the bestOrder
#			 3) iterate through the new order andd see if you can play the tile, if so inform the user and return
#Assistance Received: none 
#********************************************************************* */
def getHelp(gameState, whichHuman):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	humanPlayer = humanPlayers[whichHuman]
	if(playNext == "human1"):
		playSide = 'l'
	elif(playNext == "human2"):
		playSide = 't'
	elif(playNext == "human3"):
		playSide = 'r'
	top=board.getTopMostPip()
	left = board.getLeftMostPip()
	right = board.getRightMostPip()
	bottom = board.getBottomMostPip()
	bestOrder = bestTilesToPlay(humanPlayer.getHand())
	for tile in bestOrder:
		if(tile.getRight() == tile.getLeft()):
			if(tile.getLeft() == left):
				print("Play ", tile, " on the left, it is a double and so it is advantageous to you to get rid of it")
				print("It also is the heaviest double you could play")
				return
			elif(tile.getLeft() == top):
				print("Play ", tile, " to the top, it is a double and so it is advantageous to you to get rid of it")
				print("It is also the heaviest double you could play")
				return
			elif(tile.getLeft() == right):
				print("Play ", tile, " to the right, it is a double and so it is advantageous to you to get rid of it")
				print("It is also the heaviest double you could play")
				return
			elif(tile.getLeft() == bottom):
				print("Play ", tile, " to the bottom, it is a double and so it is advantageous to you to get rid of it")
				print("It is also the heaviest double you could play")
				return
		if(playSide == 'l'):
			if(tile.getLeft() == left or tile.getRight() == left):
				print("Play ", tile, " on the left, it is the heaviest non-double which you can play")
				print("The strategy is to build up your own side so put it on the left for the move")
				print("Which does maximum strategical advantage according to the computer")
				return
			if(passCount >= 3):
				if(tile.getLeft() == top or tile.getRight() == top):
					print("Play ", tile, " on the top, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("Which does maximum strategical advantage according to the computer")
					return
				elif(tile.getLeft() == right or tile.getRight() == right):
					print("Play ", tile, " on the right, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("Which does maximum strategical advantage according to the computer")
					return
				elif(tile.getLeft() == bottom or tile.getRight() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return
			elif(passCount == 2):
				if(tile.getLeft() == right or tile.getRight() == right):
					print("Play ", tile, " on the right, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("Which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getRight() == bottom or tile.getLeft() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
			elif(passCount == 1):
				if(tile.getLeft() == bottom or tile.getRight() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
		elif(playSide == 't'):
			if(tile.getLeft() == top or tile.getRight() == top):
				print("Play ", tile, " on the top, it is the heaviest non-double which you can play")
				print("The strategy is to build up your own side so put it on the top for the move")
				print("Which does maximum strategical advantage according to the computer")
				return 
			if(passCount >= 3):
				if(tile.getLeft() == right or tile.getRight() == right):
					print("Play ", tile, " on the right, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("Which does maximum strategical advantage according to the computer")
					return
				elif(tile.getLeft() == bottom or tile.getRight() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getLeft() == left or tile.getRight() == top):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
			elif(passCount == 2):
				if(tile.getLeft() == bottom or tile.getRight() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getRight() == left or tile.getLeft() == left):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
			elif(passCount == 1):
				if(tile.getLeft() == left or tile.getRight() == left):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
		elif(playSide == 'r'):
			if(tile.getLeft() == right or tile.getRight() == right):
				print("Play ", tile, " on the right, it is the heaviest non-double which you can play")
				print("The strategy is to build up your own side so put it on the right for the move")
				print("Which does maximum strategical advantage according to the computer")
				return 
			if(passCount >= 3):
				if(tile.getLeft() == bottom or tile.getRight() == bottom):
					print("Play ", tile, " on the bottom, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getRight() == left or tile.getLeft() == left):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getRight() == top or tile.getLeft() == top):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return
			elif(passCount == 2):
				if(tile.getRight() == left or tile.getLeft() == left):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("The strategy is to try not to play on the board of someone who may pass again right before you")
					print("which does maximum strategical advantage according to the computer")
					return 
				elif(tile.getRight() == top or tile.getLeft() == top):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
			elif(passCount == 1):
				if(tile.getLeft() == top or tile.getRight() == top):
					print("Play ", tile, " on the left, is is the heaviest non-double which you can play")
					print("You have no other side to place the tile on so this will be the one")
					print("which does maximum strategical advantage according to the computer")
					return 
	print("Something went wrong")
	return


#/* ********************************************************************* 
#Function Name: getSideToPlay 
#Purpose: To do user input with try and catch 
#Parameters: 
#            none
#Return Value: side to play  
#Local Variables: 
#            side 
#Algorithm: 
#            1) ask user for input and validate and return
#			 2) if input is wrong type catch the error
#Assistance Received: none 
#********************************************************************* */
def getSideToPlay():
	side = 'f'
	try:
		while(side != 'l' and side != 't' and side != 'r' and side != 'b'):
			side = input("Please enter which side to play on(l/r/t/b): ").lower()
		return side
	except TypeError:
		print("A valid character must be entered.")
		return getSideToPlay()

#/* ********************************************************************* 
#Function Name: saveAndExit 
#Purpose: to create the save file and exit program 
#Parameters: 
#            gamestate
#Return Value: none 
#Local Variables: 
#            Broken douwn gamestate
#			 filename
# 			 savefile 
#Algorithm: 
#            1) input filename to save to and append to it .txt 
#            2) parse through gamestate and save it to file then exit
#Assistance Received: none 
#********************************************************************* */
def saveAndExit(gameState):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	filename = input("Please enter the filename to save to: ")
	filename += ".txt"
	saveFile = open(filename, 'w')
	saveFile.write("Tournament Score: ")
	saveFile.write(str(tournScore))
	saveFile.write("\n")
	saveFile.write("Players: ")
	saveFile.write(str(len(humanPlayers) + len(computerPlayers)))
	saveFile.write("\n")
	saveFile.write("Round No.: ")
	saveFile.write(str(roundNo))
	saveFile.write("\n")
	saveFile.write("\n")
	saveFile.flush()
	players = []
	for player in humanPlayers:
		players.append(player)
	for player in computerPlayers:
		players.append(player)
	for i in range(0, len(players)):
		saveFile.write("Player ")
		saveFile.flush()
		saveFile.write(str(i+1))
		saveFile.flush()
		saveFile.write(":\n")
		saveFile.flush()
		saveFile.write("\tType: ")
		saveFile.flush()
		if(players[i].isComputer()):
			saveFile.write("Computer\n")
			saveFile.flush()
		else:
			saveFile.write("Human\n")
			saveFile.flush()
		saveFile.write("\tHand: ")
		saveFile.flush()
		for tile in players[i].getHand():
			saveFile.write(str(tile.getLeft()))
			saveFile.flush()
			saveFile.write("-")
			saveFile.flush()
			saveFile.write(str(tile.getRight()))
			saveFile.flush()
			saveFile.write(" ")
			saveFile.flush()
		saveFile.write("\n\tScore: ")
		saveFile.flush()
		saveFile.write(str(players[i].getScore()))
		saveFile.flush()
		saveFile.write("\n\n")
		saveFile.flush()
	saveFile.write("Layout:\n")
	s = ""
	s += "   "
	for tile in board.left:
		s+= "    "
	s += "P2"
	s += '\n'
	for tile in reversed(board.top):
		s += "   "
		for a_tile in board.left:
			s += "    "
		s += str(tile.getLeft())
		s += "-"
		s += str(tile.getRight())
		s += '\n'
	s += "P1 "
	for tile in reversed(board.left):
		s += str(tile.getRight())
		s += "-"
		s += str(tile.getLeft())
		s += " "
	s += str(board.engine.getLeft())
	s += "-"
	s += str(board.engine.getRight())
	s += " "
	for tile in board.right:
		s += str(tile.getLeft())
		s += "-"
		s += str(tile.getRight())
		s += " "
	s += "P3"
	s += '\n'
	for tile in board.bottom:
		s += "   "
		for a_tile in board.left:
			s += "    "
		s += str(tile.getLeft())
		s += "-"
		s += str(tile.getRight())
		s += '\n'
	s += "   "
	for tile in board.left:
		s += "    "
	s += "P4"
	s += '\n'
	saveFile.write(s)
	saveFile.write("\n")
	saveFile.write("Boneyard: \n")
	for tile in stock.tiles:
		saveFile.write(str(tile.getLeft()))
		saveFile.write("-")
		saveFile.write(str(tile.getRight()))
		saveFile.write(" ")
	saveFile.write("\n\n")
	saveFile.write("Previous Players Passed: ")
	saveFile.write(str(passCount))
	saveFile.write("\n\n")
	saveFile.write("Next Player: ")
	if(playNext == "human1"):
		saveFile.write("Player 1")
	elif(playNext == "human2"):
		saveFile.write("Player 2")
	elif(playNext == "human3"):
		saveFile.write("Player 3")
	elif(playNext == "computer1"):
		if(len(humanPlayers) == 1):
			saveFile.write("Player 2")
		elif(len(humanPlayers) == 2):
			saveFile.write("Player 3")
		else:
			saveFile.write("Player 4")
	elif(playNext == "computer2"):
		if(len(humanPlayers) == 1):
			saveFile.write("Player 3")
		else:
			saveFile.write("Player 4")
	elif(playNext == "computer3"):
		saveFile.write("Player 4")
	saveFile.flush()
	saveFile.close()
	os._exit(0)

#/* ********************************************************************* 
#Function Name: loadGame 
#Purpose: To load state from file 
#Parameters: 
#            none
#Return Value: none
#Local Variables: 
#            filename, line, gamestate
#Algorithm: 
#            1) parse the file and load in each part of gameState
#			 2) call playRound
#Assistance Received: none 
#********************************************************************* */
def loadGame():
	filename = input("Please enter filename to load from: ")
	filename += ".txt"
	try:
		loadFile = open(filename, 'r')
	except FileNotFoundError:
		print("File not found")
		return loadGame()
	line1 = loadFile.readline()
	tournScore = int(line1[18:])
	line2 = loadFile.readline()
	numPlayers = int(line2[9:])
	line3 = loadFile.readline()
	roundNo = int(line3[11:])
	line4 = loadFile.readline()
	players = []
	humanPlayers = []
	computerPlayers = []
	for i in range(0, numPlayers):
		line = loadFile.readline()
		line = loadFile.readline()
		playerType = line[7:]
		line = loadFile.readline()
		playTiles = line[7:]
		line = loadFile.readline()
		playerScore = line[8:]
		line = loadFile.readline()
		if(playerType == "Human\n"):
			count = 0
			tiles = []
			l = -1
			r = -1
			for i in range(0, len(playTiles)):
				if(playTiles[i].isdigit()):
					if(count%2 == 0):
						l = int(playTiles[i])
					else:
						r = int(playTiles[i])
						tiles.append(Tile(l,r))
					count += 1					
			humanPlayers.append(Human(tiles, int(playerScore)))
			players.append(Human(tiles, int(playerScore)))
		else:
			count = 0
			tiles = []
			l = -1
			r = -1
			for i in range(0, len(playTiles)):
				if(playTiles[i].isdigit()):
					if(count%2 == 0):
						l = int(playTiles[i])
					else:
						r = int(playTiles[i])
						tiles.append(Tile(l,r))
					count += 1
			computerPlayers.append(Computer(tiles, int(playerScore)))
			players.append(Computer(tiles, int(playerScore)))
	line = loadFile.readline()
	line = loadFile.readline()
	listTop = []
	while(line[0] != 'P'):
		line = loadFile.readline()
		if(line[0] == 'P'):
			break
		for i in range(0, len(line)):
			if(line[i].isdigit()):
				l = int(line[i])
				r = int(line[i+2])
				listTop.append(Tile(l, r))
				break
	engine = generateEngine(roundNo, len(humanPlayers), len(computerPlayers))
	listLeft = []
	listRight = []
	rightSide = False
	for i in range(0, len(line)):
		if(line[i].isdigit() and line[i+1] == '-'):
			if(int(line[i]) == engine.getLeft() and int(line[i+2]) == engine.getRight()):
				rightSide = True
			else:
				l = int(line[i])
				r = int(line[i+2])
				if(rightSide == False):
					listLeft.append(Tile(l,r))
				else:
					listRight.append(Tile(l,r))
	done = False
	listBottom = []
	while(done == False):
		line = loadFile.readline()
		for i in range(0, len(line)):
			if(line[i] == 'P'):
				done = True
				break
			elif(line[i].isdigit()):
				l = int(line[i])
				r = int(line[i+2])
				listBottom.append(Tile(l,r))
				break
	line = loadFile.readline()
	line = loadFile.readline()
	line = loadFile.readline()
	stockList = []
	stockList2 = []
	for i in range(0, len(line)-1):
		if(line[i].isdigit and line[i+1] == '-'):
			l = int(line[i])
			r = int(line[i+2])
			stockList.append(Tile(l,r))
	for tile in reversed(stockList):
		stockList2.append(tile)
	line = loadFile.readline()
	line = loadFile.readline()
	if(len(listTop) == 0 and len(listLeft) == 0 and len(listRight) == 0 and len(listBottom) == 0):
		board = Board([])
		board.insert(engine)
		stock = Boneyard(stockList2)
		playNext = "none"
		[humanPlayers, computerPlayers, stock, playNext] = drawForEngine(engine, humanPlayers, computerPlayers, stock, playNext)
		gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, 0]
		playRound(gameState)
	passCount = int(line[25:])
	line = loadFile.readline()
	line = loadFile.readline()
	nextPlay = line[13:]
	if(nextPlay == "Player 1\n" or nextPlay == "Player 1"):
		if(players[0].isComputer()):
			nextPlay = "computer1"
		else:
			nextPlay = "human1"
	elif(nextPlay == "Player 2" or nextPlay == "Player 2\n"):
		if(players[1].isComputer() and players[0].isComputer()):
			nextPlay = "computer2"
		elif(players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "computer1"
		elif(not players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "human2"
		elif(not players[1].isComputer() and players[0].isComputer()):
			nextPlay = "human1"
	elif(nextPlay == "Player 3" or nextPlay == "Player 3\n"):
		if(players[2].isComputer() and players[1].isComputer() and players[0].isComputer()):
			nextPlay = "computer3"
		elif(players[2].isComputer() and players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "computer2"
		elif(players[2].isComputer() and not players[1].isComputer() and players[0].isComputer()):
			nextPlay = "computer2"
		elif(players[2].isComputer() and not players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "computer1"
		elif(not players[2].isComputer() and not players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "human3"
		elif(not players[2].isComputer() and players[1].isComputer() and not players[0].isComputer()):
			nextPlay = "human2"
		elif(not players[2].isComputer() and not players[1].isComputer() and players[0].isComputer()):
			nextPlay = "human2"
		elif(not players[2].isComputer() and players[1].isComputer() and players[0].isComputer()):
			nextPlay = "human3"
	elif(nextPlay == "Player 4" or nextPlay == "Player 4\n"):
		if(players[3].isComputer()):
			nextPlay = "computer" + str(len(computerPlayers))
		else:
			nextPlay = "human" + str(len(humanPlayers))
	board = Board([])
	board.insert(engine)
	for tile in reversed(listLeft):
		board.insertLeft(tile)
	for tile in listRight:
		board.insertRight(tile)
	for tile in reversed(listTop):
		board.insertTop(tile)
	for tile in listBottom:
		board.insertBottom(tile)
	stock = Boneyard(stockList2)
	gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, nextPlay, passCount]
	playRound(gameState)

#/* ********************************************************************* 
#Function Name: humanPlay 
#Purpose: To allow a human player to play a move 
#Parameters: 
#            gamestate
#			 whichHuman - index of which human is playing
#			 playerPassCount - count of how many times the human has passed in this turn
#Return Value: none 
#Local Variables: 
#            Broken douwn gamestate 
# 			 index - tile to play
#			 Playside - humans side to play on
#Algorithm: 
#            1) determine who is player then print out board and let the human enter where to play 
#            2) call the appropriate function based on input
#			 3) let the human play the move or pass or save or get help
#Assistance Received: none 
#********************************************************************* */
def humanPlay(gameState, whichHuman, playerPassCount):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	humanPlayer = humanPlayers[whichHuman]
	if(whichHuman == 0):
		playSide = 'l'
	elif(whichHuman == 1):
		playSide = 't'
	elif(whichHuman == 2):
		playSide = 'r'
	print(board)
	print(humanPlayer.getHand())
	for i in range (1, len(humanPlayer.getHand())+1):
		if(i < 10):
			print("  ",i,"  ", end='')
		else:
			print(" ", i,"  ", end='')
	index=-1
	try:
		while(index < 0 or index > len(humanPlayer.getHand())):
			print()
			index = input("Please enter which tile you would like to move, or enter 'p' to pass, 'h' for hint, or 's' to save: ")
			if(index.lower() == 'p' and playerPassCount == 0):
				if(humanHasLegalMove(humanPlayer, board, stock, passCount, playSide) == False):
					if(len(stock.tiles) > 0):
						print("You have drawn a tile, if you pass again the next player will play")
						humanPlayer.insert(stock.getTopN(1))
						return humanPlay(gameState, whichHuman, 1)
					else:
						print("Stock is empty, next player will play")
						return
				else:
					print("You have a legal move, try again")
					return humanPlay(gameState, whichHuman, playerPassCount)
			elif(index.lower() == 'p' and playerPassCount == 1):
				if(humanHasLegalMove(humanPlayer, board, stock, passCount, playSide) == False):
					print("You have passed again, next player will play")
					return
				else:
					print("You have a legal move, try again")
					return humanPlay(gameState, whichHuman, playerPassCount)
			elif(index.lower() == 'h'):
				if(humanHasLegalMove(humanPlayer, board, stock, passCount, playSide) == False):
					print("You have no legal moves, press 'p' to pass")
					return humanPlay(gameState, whichHuman, playerPassCount)
				else:
					getHelp(gameState, whichHuman)
					return humanPlay(gameState, whichHuman, playerPassCount)
			elif(index.lower() == 's' and playerPassCount == 0):
				saveAndExit(gameState)
			elif(index.lower() == 's'):
				print("You cannot save mid-way through your turn")
				return humanPlay(gameState, whichHuman, playerPassCount)
			else:
				index = int(index)
	except TypeError:
		print("Invalid option")
		return humanPlay(gameState, whichHuman, playerPassCount)
	except ValueError:
		print("Invalid option")
		return humanPlay(gameState, whichHuman, playerPassCount)
	side = getSideToPlay()
	if(validateMove(gameState, playSide, index, side) == False):
		print("Invalid move, try again")
		return humanPlay(gameState, whichHuman, playerPassCount)

#/* ********************************************************************* 
#Function Name: bestTilesToPlay 
#Purpose: To sort a hand into the best play order by tile 
#Parameters: 
#            tiles - a list of tiles
#Return Value: sorted list of tiles 
#Local Variables: 
#            doubles, signles, tile, tilesSum, bestTiles
#Algorithm: 
#            1) parse the tiles, if tile is a double it goes into the doubles list by sum of pips
#			 2) if tile is a single then it goes into the singles list
#			 3) append the singles to doubles in bestTiles
#			 4) return bestTiles
#Assistance Received: none 
#********************************************************************* */
def bestTilesToPlay(tiles):
	doubles = []
	singles = []
	for tile in tiles:
		tileSum = tile.getLeft() + tile.getRight()
		if(tile.getLeft() == tile.getRight()):
			if(len(doubles) == 0):
				doubles.insert(0, tile)
			else:
				i = 0
				for a_tile in doubles:
					if(tile.getLeft() > doubles[i].getLeft()):
						doubles.insert(i, tile)
						break
					elif(i == len(doubles)-1 and tile.getLeft() <= doubles[i].getLeft()):
						doubles.append(tile)
						break
					i += 1
		else:
			if(len(singles) == 0):
				singles.append(tile)
			elif(len(singles) == 1):
				singleSum = singles[0].getLeft()+singles[0].getRight()
				if(tileSum > singleSum):
					singles.insert(0, tile)
				else:
					singles.append(tile)
			else:
				i = 0
				for a_tile in singles:
					singleSum = singles[i].getLeft() + singles[i].getRight()
					if(tileSum > singleSum):
						singles.insert(i, tile)
						break
					elif (tileSum <= (singles[len(singles)-1].getLeft() + singles[len(singles)-1].getRight()) and i == len(singles) - 1):
						singles.append(tile)
						break
					i += 1
	bestTiles = []
	for tile in doubles:
		bestTiles.append(tile)
	for tile in singles:
		bestTiles.append(tile)
	return bestTiles

#/* ********************************************************************* 
#Function Name: computerPlay 
#Purpose: to allow the computer to make a move 
#Parameters: 
#            gamestate
#			 playSide - side the player is supposed to be playing on
#			 playerPassCount - how many times the computer has already passed this move
#Return Value: none 
#Local Variables: 
#            Broken douwn gamestate 
#			 testlen - length of player hand
# 			 weightedHand - ordered hand by best tiles to play algorithm
#Algorithm: 
#            1) determine who is player then rearrange their tiles into weighted hand 
#            2) for every tile try to play the move first on playSide then going counterClockWise
#			 3) if playable break out, if all tiles are exhausted pass
#Assistance Received: none 
#********************************************************************* */
def computerPlay(gameState, playSide, playerPassCount):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	if(playNext == "computer1"):
		computerPlayer = computerPlayers[0]
	elif(playNext == "computer2"):
		computerPlayer = computerPlayers[1]
	elif(playNext == "computer3"):
		computerPlayer = computerPlayers[2]
	testLen = len(computerPlayer.getHand())
	weightedhand = bestTilesToPlay(computerPlayer.getHand())
	for tile in weightedhand:
		index = (computerPlayer.getHand().index(tile))+1
		if(playSide == 't'):
			if(validateMove(gameState, playSide, index, 't') == True):
				break
			if(validateMove(gameState, playSide, index, 'l') == True):
				break
			if(validateMove(gameState, playSide, index, 'b') == True):
				break
			if(validateMove(gameState, playSide, index, 'r') == True):
				break
		elif(playSide == 'r'):
			if(validateMove(gameState, playSide, index, 'r') == True):
				break
			if(validateMove(gameState, playSide, index, 't') == True):
				break
			if(validateMove(gameState, playSide, index, 'l') == True):
				break
			if(validateMove(gameState, playSide, index, 'b') == True):
				break
		elif(playSide == 'b'):
			if(validateMove(gameState, playSide, index, 'b') == True):
				break
			if(validateMove(gameState, playSide, index, 'r') == True):
				break
			if(validateMove(gameState, playSide, index, 't') == True):
				break
			if(validateMove(gameState, playSide, index, 'l') == True):
				break
	newHand = computerPlayer.getHand()
	if(len(newHand) == testLen and playerPassCount == 0):
		if(len(stock.tiles) != 0):
			print("Computer has drawn a tile, he will try to play it now")
			computerPlayer.insert(stock.getTopN(1))
			computerPlay(gameState, playSide, 1)
		else:
			print("Computer player has no legal moves, and the stock is empty, next player will play")
	elif(len(newHand) == testLen and playerPassCount == 1):
		print("After passing computer still has no legal moves")
	
#/* ********************************************************************* 
#Function Name: generateNewRound 
#Purpose: To make a new round after one has ended 
#Parameters: 
#            gamestate
#Return Value: none 
#Local Variables: 
#            Broken douwn gamestate 
#			 engine tile
#Algorithm: 
#            1) regenerate the tiles and put them into the stock 
#            2) clear the player hands and insert 8 tiles from the stock into each player  hand
#			 3) figure out who plays next
#			 4) recreate gameState and call playRound
#Assistance Received: none 
#********************************************************************* */
def generateNewRound(gameState):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	roundNo += 1
	if(len(humanPlayers) + len(computerPlayers) == 2):
		tiles = createTiles(6, 6)
	else:
		tiles = createTiles(9, 9)
	#create the stock
	random.shuffle(tiles)
	stock = Boneyard(tiles)
	for humanPlayer in humanPlayers:
		humanPlayer.getHand().clear()
	for computerPlayer in computerPlayers:
		computerPlayer.getHand().clear()
	for i in range(0, len(humanPlayers)):
		humanPlayers[i].insert(stock.getTopN(8))
	for i in range(0, len(computerPlayers)):
		computerPlayers[i].insert(stock.getTopN(8))
	engine = generateEngine(roundNo, len(computerPlayers), len(humanPlayers))
	board = Board([])
	board.insert(engine)
	playNext = "none"
	passCount = 0
	#offer serialization prior to center placement
	[humanPlayers, computerPlayers, stock, playNext] = drawForEngine(engine, humanPlayers, computerPlayers, stock, playNext)
	gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
	playRound(gameState)

#/* ********************************************************************* 
#Function Name: playRound 
#Purpose: To play the round and the tournament is in this 
#Parameters: 
#            gamestate
#Return Value: none 
#Local Variables: 
#            Broken douwn gamestate 
#Algorithm: 
#			 1) check if round is over by empty stock and passCount if determine winner and make new round
#            2) determine who is next player
#			 3) let them play their move
#			 4) check if they won the round, if not change playNext and call playRound
#			 5) add the appropriate scores
#			 6) check if they surpassed the tournament, if so exit
#			 7) if not create a new round
#Assistance Received: none 
#********************************************************************* */
def playRound(gameState):
	[tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount] = gameState
	print("Next player is: ", playNext)
	gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
	if(len(stock.tiles) == 0 and passCount >= len(humanPlayers) + len(computerPlayers)):
		print("Stock is empty and all players have passed, therefore the round is over, the player with the least amount of points will win")
		players = []
		for player in humanPlayers:
			players.append(player)
		for player in computerPlayers:
			players.append(player)
		scores = []
		for player in players:
			scores.append(player.sumPips())
		lowestScore = scores[0]
		for score in scores:
			if score < lowestScore:
				lowestScore = score
		count = scores.count(lowestScore)
		for i in range(0, len(scores) -1):
			print("P", str(i+1), " finished with ", str(scores[i]), " points")
		if(count > 1):
			for i in range(0, len(scores)-1):
				if(scores[i] == lowestScore):
					print("P", str(i+1), " has tied with ", lowestScore, " points")
			print("No one will get points added due to the tie")
		else:
			for i in range(0, len(scores)-1):
				if(scores[i] == lowestScore):
					print("P", str(i+1), " has won this round with ", lowestScore, " points")
					print("The points totals were: ")
					for score in scores:
						print(score, " points,")
					print("He will get ", max(scores), " added to his score")

					if(i < len(humanPlayers)):
						humanPlayers[i].addToScore(max(scores))
						print("P", str(i+1), " now has ", humanPlayers[i].getScore(), " points")
						if(humanPlayers[i].getScore() >= tournScore):
							print("P", str(i+1), " has more points than the tournament. Game Over. The tournament score was ", tournScore)
							os._exit(0)
					else:
						index = i - len(humanPlayers)
						computerPlayers[index].addToScore(max(scores))
						print("P", str(i+1), " now has ", computerPlayers[index].getScore(), " points")
						if(computerPlayers[index].getScore() >= tournScore):
							print("P", str(i+1), " has more points than the tournament. Game Over. The tournament score was ", tournScore)
		generateNewRound(gameState)
	if(playNext[0] == 'h'):
		if(playNext[5] == '1'):
			testlength = len(humanPlayers[0].getHand())
			humanPlay(gameState, 0, 0)
			if(len(humanPlayers[0].getHand()) > testlength):
				passCount += 1
			elif(len(humanPlayers[0].getHand()) == testlength and len(stock.tiles) == 0):
				passCount += 1
			else:
				passCount = 0
			if(len(humanPlayers) > 1):
				playNext = "human2"
			else:
				playNext = "computer1"
			if(len(humanPlayers[0].getHand()) == 0):
				highestScore = 0
				print("Human1 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
				print("The players ended with: ")
				for humanPlayer in humanPlayers:
					print(humanPlayer.sumPips(), " points,")
					if(humanPlayer.sumPips() > highestScore):
						highestScore = humanPlayer.sumPips()
				for computerPlayer in computerPlayers:
					print(computerPlayer.sumPips(), " points,")
					if(computerPlayer.sumPips() > highestScore):
						highestScore = computerPlayer.sumPips()
				print("Human1 had ", humanPlayers[0].getScore(), " and will have ", highestScore, " points added to his hand.")
				humanPlayers[0].addToScore(highestScore)
				print("Human1's score is now ", humanPlayers[0].getScore())
				if(humanPlayers[0].getScore() >= tournScore):
					print("Human1 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
					os._exit(0)
				generateNewRound(gameState)
			gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
			playRound(gameState)
		elif(playNext[5] == '2'):
			testlength = len(humanPlayers[1].getHand())
			humanPlay(gameState, 1, 0)
			if(len(humanPlayers[1].getHand()) > testlength):
				passCount += 1
			elif(len(humanPlayers[1].getHand()) == testlength and len(stock.tiles) == 0):
				passCount += 1
			else:
				passCount = 0
			if(len(humanPlayers) > 2):
				playNext = "human3"
			else:
				playNext = "computer1"
			if(len(humanPlayers[1].getHand()) == 0):
				highestScore = 0
				print("Human2 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
				print("The players ended with: ")
				for humanPlayer in humanPlayers:
					print(humanPlayer.sumPips(), " points,")
					if(humanPlayer.sumPips() > highestScore):
						highestScore = humanPlayer.sumPips()
				for computerPlayer in computerPlayers:
					print(computerPlayer.sumPips(), " points,")
					if(computerPlayer.sumPips() > highestScore):
						highestScore = computerPlayer.sumPips()
				print("Human2 had ", humanPlayers[1].getScore(), " and will have ", highestScore, " points added to his hand.")
				humanPlayers[1].addToScore(highestScore)
				print("Human2's score is now ", humanPlayers[1].getScore())
				if(humanPlayers[1].getScore() >= tournScore):
					print("Human2 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
					os._exit(0)
				generateNewRound(gameState)
			gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
			playRound(gameState)
		else:
			testlength = len(humanPlayers[2].getHand())
			humanPlay(gameState, 2, 0)
			if(len(humanPlayers[2].getHand()) > testlength):
				passCount += 1
			elif(len(humanPlayers[2].getHand()) == testlength and len(stock.tiles) == 0):
				passCount += 1
			else:
				passCount = 0
			playNext = "computer1"
			if(len(humanPlayers[2].getHand()) == 0):
				highestScore = 0
				print("Human3 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
				print("The players ended with: ")
				for humanPlayer in humanPlayers:
					print(humanPLayer.sumPips(), " points,")
					if(humanPlayer.sumPips() > highestScore):
						highestScore = humanPlayer.sumPips()
				for computerPlayer in computerPlayers:
					print(computerPlayer.sumPips(), " points,")
					if(computerPlayer.sumPips() > highestScore):
						highestScore = computerPlayer.sumPips()
				print("Human3 had ", humanPlayers[2].getScore(), " and will have ", highestScore, " points added to his score.")
				humanPlayers[2].addToScore(highestScore)
				print("Human3's score is now ", humanPlayers[2].getScore())
				if(humanPlayers[2].getScore() >= tournScore):
					print("Human3 now has more points that the tournament. Game Over. The tournament score was ", tournScore)
					exit(1)
				generateNewRound(gameState)
			gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
			playRound(gameState)
			#third human to play
	else:
		print(board)
		try:
			yorn = '\0'
			while(yorn != 'y' and yorn != 'n'):
				yorn = input("Would you like to save before the computer move(y/n): ").lower()
			if(yorn == 'y'):
				saveAndExit(gameState)
		except ValueError:
			print("Invalid input, try again")
			playRound(gameState)
		if(playNext[8] == '1'):
			if(len(humanPlayers) == 1):
				testlength = len(computerPlayers[0].getHand())
				if(len(computerPlayers) == 1):
					computerPlay(gameState, 'r', 0)
				else:
					computerPlay(gameState, 't', 0)
				if(len(computerPlayers[0].getHand()) > testlength):
					passCount += 1
				elif(len(computerPlayers[0].getHand()) == testlength and len(stock.tiles) == 0):
					passCount += 1
				else:
					passCount = 0
				if(len(computerPlayers) == 1):
					playNext = "human1"
				else:
					playNext = "computer2"
				if(len(computerPlayers[0].getHand()) == 0):
					highestScore = 0
					print("Computer1 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
					print("The players ended with: ")
					for humanPlayer in humanPlayers:
						print(humanPlayer.sumPips(), " points,")
						if(humanPlayer.sumPips() > highestScore):
							highestScore = humanPlayer.sumPips()
					for computerPlayer in computerPlayers:
						print(computerPlayer.sumPips(), " points,")
						if(computerPlayer.sumPips() > highestScore):
							highestScore = computerPlayer.sumPips()
					print("Computer1 had ", computerPlayers[0].getScore(), " and will have ", highestScore, " points added to his score.")
					computerPlayers[0].addToScore(highestScore)
					print("Computer1's score is now ", computerPlayers[0].getScore())
					if(computerPlayers[0].getScore() >= tournScore):
						print("Computer1 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
						exit(1)
					generateNewRound(gameState)
				gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
				playRound(gameState)
			elif(len(humanPlayers) == 2):
				testlength = len(computerPlayers[0].getHand())
				computerPlay(gameState, 'r', 0)
				if(len(computerPlayers[0].getHand()) > testlength):
					passCount += 1
				elif(len(computerPlayers[0].getHand()) == testlength and len(stock.tiles) == 0):
					passCount += 1
				else:
					passCount = 0
				if(len(computerPlayers) == 1):
					playNext = "human1"
				else:
					playNext = "computer2"
				if(len(computerPlayers[0].getHand()) == 0):
					highestScore = 0
					print("Computer1 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
					print("The players ended with: ")
					for humanPlayer in humanPlayers:
						print(humanPlayer.sumPips(), " points")
						if(humanPlayer.sumPips() > highestScore):
							highestScore = humanPlayer.sumPips()
					for computerPlayer in computerPlayers:
						print(computerPlayer.sumPips(), " points")
						if(computerPlayer.sumPips() > highestScore):
							highestScore = computerPlayer.sumPips()
					print("Computer1 had ", computerPlayers[0].getScore(), " and will have ", highestScore, " points added to his score.")
					computerPlayers[0].addToScore(highestScore)
					print("Computer1's score is now ", computerPlayers[0].getScore())
					if(computerPlayers[0].getScore() >= tournScore):
						print("Computer1 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
						exit(1)
					generateNewRound(gameState)
				gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
				playRound(gameState)
			else:
				testlength = len(computerPlayers[0].getHand())
				computerPlay(gameState, 'b', 0)
				if(len(computerPlayers[0].getHand()) > testlength):
					passCount += 1
				elif(len(computerPlayers[0].getHand()) == testlength and len(stock.tiles) == 0):
					passCount += 1
				else:
					passCount = 0
				if(len(computerPlayers) == 1):
					playNext = "human1"
				else:
					playNext = "computer2"
				if(len(computerPlayers[0].getHand()) == 0):
					highestScore = 0
					print("Computer1 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
					print("The players ended with: ")
					for humanPlayer in humanPlayers:
						print(humanPlayer.sumPips(), " points,")
						if(humanPlayer.sumPips() > highestScore):
							highestScore = humanPlayer.sumPips()
					for computerPlayer in computerPlayers:
						print(computerPlayer.sumPips(), " points,")
						if(computerPlayer.sumPips() > highestScore):
							highestScore = computerPlayer.sumPips()
					print("Computer1 had ", computerPlayers[0].getScore(), " and will have ", highestScore, " points added to his score.")
					computerPlayers[0].addToScore(highestScore)
					print("Computer1's score is now ", computerPlayers[0].getScore())
					if(computerPlayers[0].getScore() >= tournScore):
						print("Computer1 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
						exit(1)
					generateNewRound(gameState)
				gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
				playRound(gameState)
		elif(playNext[8] == '2'):
			if(len(humanPlayers) == 2):
				testlength = len(computerPlayers[1].getHand())
				computerPlay(gameState, 'b', 0)
				if(len(computerPlayers[1].getHand()) > testlength):
					passCount += 1
				elif(len(computerPlayers[1].getHand()) == testlength and len(stock.tiles) == 0):
					passCount += 1
				else:
					passCount = 0
				if(len(computerPlayers) == 2):
					playNext = "human1"
				else:
					playNext = "computer3"
				if(len(computerPlayers[1].getHand()) == 0):
					highestScore = 0
					print("Computer2 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
					print("The players ended with: ")
					for humanPlayer in humanPlayers:
						print(humanPlayer.sumPips(), " points, ")
						if(humanPlayer.sumPips() > highestScore):
							highestScore = humanPlayer.sumPips()
					for computerPlayer in computerPlayers:
						print(computerPlayer.sumPips(), " points, ")
						if(computerPlayer.sumPips() > highestScore):
							highestScore = computerPlayer.sumPips()
					print("Computer2 had ", computerPlayers[1].getScore(), " and will have ", highestScore, " points added to his score")
					computerPlayers[1].addToScore(highestScore)
					print("Computer2's score is now ", computerPlayers[1].getScore())
					if(computerPlayers[1].getScore() >= tournScore):
						print("Computer2 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
						exit(1)
					generateNewRound(gameState)
				gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
				playRound(gameState)
			elif(len(humanPlayers) == 1):
				testlength = len(computerPlayers[1].getHand())
				computerPlay(gameState, 'r', 0)
				if(len(computerPlayers[1].getHand()) > testlength):
					passCount += 1
				elif(len(computerPlayers[1].getHand()) == testlength and len(stock.tiles) == 0):
					passCount += 1
				else:
					passCount = 0
				if(len(computerPlayers) == 2):
					playNext = "human1"
				else:
					playNext = "computer3"
				if(len(computerPlayers[1].getHand()) == 0):
					highestScore = 0
					print("Computer2 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
					print("The players ended with: ")
					for humanPlayer in humanPlayers:
						print(humanPlayer.sumPips(), " points,")
						if(humanPlayer.sumPips() > highestScore):
							highestScore = humanPlayer.sumPips()
					for computerPlayer in computerPlayers:
						print(computerPlayer.sumPips(), " points,")
						if(computerPlayer.sumPips() > highestScore):
							highestScore = computerPlayer.sumPips()
					print("Computer2 had ", computerPlayers[1].getScore(), " and will have ", highestScore, " points added to his score")
					computerPlayers[1].addToScore(highestScore)
					print("Computer2's score is now ", computerPlayers[1].getScore())
					if(computerPlayers[1].getScore() >= tournScore):
						print("Computer2 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
						exit(1)
					generateNewRound(gameState)
				gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
				playRound(gameState)
		else:
			testlength = len(computerPlayers[2].getHand())
			computerPlay(gameState, 'b', 0)
			if(len(computerPlayers[2].getHand()) > testlength):
				passCount += 1
			elif(len(computerPlayers[2].getHand()) == testlength and len(stock.tiles) == 0):
				passCount += 1
			else:
				passCount = 0
			playNext = "human1"
			if(len(computerPlayers[2].getHand()) == 0):
				highestScore = 0
				print("Computer3 has won this round by emptying their hand, he will get the highest sum of pips added to his score")
				print("The playeres ended with: ")
				for humanPlayer in humanPlayers:
					print(humanPlayer.sumPips(), " points, ")
					if(humanPlayer.sumPips() > highestScore):
						highestScore = humanPlayer.sumPips()
				for computerPlayer in computerPlayers:
					print(computerPlayer.sumPips(), " points, ")
					if(computerPlayer.sumPips() > highestScore):
						highestScore = computerPlayer.sumPips()
				print("Computer3 had ", computerPlayers[2].getScore(), " and will have ", highestScore, "points added to his score")
				computerPlayers[2].addToScore(highestScore)
				print("Comptuer3's score is now ", computerPlayers[2].getScore())
				if(computerPlayers[2].getScore() >= tournScore):
					print("Computer3 now has more points than the tournament. Game Over. The tournament score was ", tournScore)
					exit(1)
				generateNewRound(gameState)
			gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
			playRound(gameState)

#/* ********************************************************************* 
#Function Name: getNumHumans 
#Purpose: To do user input with try except block for numHumans 
#Parameters: 
#            none
#Return Value: number of humans 
#Local Variables: 
#            numPlayers 
#Algorithm: 
#            1) input number of players and validate and return it
#			 2) if it throws an exception recursively call getNumHumans()
#Assistance Received: none 
#********************************************************************* */
def getNumHumans():
	try:
		numPlayers = 0
		while(numPlayers < 1 or numPlayers > 3):
			numPlayers = int(input("How many human players(1 - 3): "))
		return numPlayers
	except ValueError:
		print("Invalid input, try again")
		return getNumHumans()

#/* ********************************************************************* 
#Function Name: getNumComputers 
#Purpose: To do user input with try except block for numComputers 
#Parameters: 
#            numPlayers - how many humans are playing
#Return Value: number of computers 
#Local Variables: 
#            numComputers 
#Algorithm: 
#            1) input number of computers and validate and return it
#			 2) if it throws an exception recursively call getNumComputers()
#Assistance Received: none 
#********************************************************************* */
def getNumComputers(numPlayers):
	try:
		numComputers = 0
		#input number of computers 
		while(numComputers < 1 or numComputers > 3 or (numPlayers + numComputers > 4)):
			numComputers = int(input("How many computer players(max 4 total players): "))
		return numComputers
	except ValueError:
		return getNumComputers(numPlayers)

#/* ********************************************************************* 
#Function Name: startNewTournament 
#Purpose: To start a new tournament 
#Parameters: 
#            none
#Return Value: none 
#Local Variables: 
#            tournScore, broken down GameState, number of each player 
#Algorithm: 
#            1) input tournament score and number of players 
#			 2) generate gameState and call playRound 
#Assistance Received: none 
#********************************************************************* */
def startNewTournament():
	tournScore = 0
	try:
		while(tournScore < 1):
			tournScore = int(input("Please enter the tournament score: "))
	except ValueError:
		print("Invalid input, try again")
		startNewTournament()
	numPlayers = getNumHumans()

	humanPlayers = []
	
	for i in range(0, numPlayers):
		humanPlayers.append(Human([], 0))
	
	numComputers = getNumComputers(numPlayers)

	
	computerPlayers = []
	for i in range(0, numComputers):
		computerPlayers.append(Computer([], 0))	
	
	if(numPlayers + numComputers == 2):
		tiles = createTiles(6, 6)
	else:
		tiles = createTiles(9, 9)
	#create the stock
	random.shuffle(tiles)
	stock = Boneyard(tiles)

	#create the initial hands
	for i in range(0, numPlayers):
		humanPlayers[i].insert(stock.getTopN(8))
	for i in range(0, numComputers):
		computerPlayers[i].insert(stock.getTopN(8))
	roundNo = 1
	engine = generateEngine(roundNo, numComputers, numPlayers)
	board = Board([])
	board.insert(engine)
	playNext = "none"
	passCount = 0
	#offer serialization prior to center placement
	[humanPlayers, computerPlayers, stock, playNext] = drawForEngine(engine, humanPlayers, computerPlayers, stock, playNext)
	gameState = [tournScore, roundNo, humanPlayers, computerPlayers, board, stock, playNext, passCount]
	playRound(gameState)

#/* ********************************************************************* 
#Function Name: startGame 
#Purpose: To start the game from new or saves 
#Parameters: 
#            none
#Return Value: none 
#Local Variables: 
#            yorn - yes or no input 
#Algorithm: 
#            1) input if player wants to load or start new tournament
#			 2) call the appropriate function
#Assistance Received: none 
#********************************************************************* */
def startGame():
	yorn = '\0'
	while(yorn != 'y' and  yorn != 'n'):
		yorn = input("Would you like to load a game from saves(y/n): ").lower()
		#yorn = 'y'
	if(yorn == 'n'):
		startNewTournament()
	else:
		loadGame()

startGame()