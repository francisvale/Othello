import pygame
from copy import deepcopy

pygame.display.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 680
player_color = 2  
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Othello')


class Chessboard:

    def __init__(self):
        self.width = 60
        self.row = self.col = 8
        self.margin = 100
        self.chesses = [[0 for _ in range(self.col)] for _ in range(self.row)]
        self.stable = [[0 for _ in range(self.col)] for _ in range(self.row)]
        self.offense = 2
        self.chesses[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.chesses[self.row // 2][self.col // 2] = 1
        self.chesses[self.row // 2][self.col // 2 - 1] = 2
        self.chesses[self.row // 2 - 1][self.col // 2] = 2
        self.count_black = self.count_white = 2
        self.count_available = 4
        self.count_stable_black = 0
        self.count_stable_white = 0
        self.count_total_stable_direct_black = 0
        self.count_total_stable_direct_white = 0
        self.available = []
        self.updateAvailable()


    def updateAvailable(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.offense
        color_reverse = 3 - color
        self.available = []
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == -1:
                    self.chesses[i][j] = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == self.offense:
                    for dx, dy in directions:
                        checking_i = i + dy
                        checking_j = j + dx
                        find_one_reverse_color = False
                        while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                            chess = self.chesses[checking_i][checking_j]
                            if chess == color_reverse:
                                checking_i += dy
                                checking_j += dx
                                find_one_reverse_color = True
                            elif chess == 0 and find_one_reverse_color:
                                self.chesses[checking_i][checking_j] = -1
                                self.available.append((checking_i, checking_j))
                                break
                            else:
                                break

    def reverse(self, set_i, set_j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color_reverse = self.offense
        color = 3 - color_reverse
        for dx, dy in directions:
            checking_i = set_i + dy
            checking_j = set_j + dx
            while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                chess = self.chesses[checking_i][checking_j]
                if chess == color_reverse:
                    checking_i += dy
                    checking_j += dx
                elif chess == color:
                    reversing_i = set_i + dy
                    reversing_j = set_j + dx
                    while (reversing_i, reversing_j) != (checking_i, checking_j):
                        self.chesses[reversing_i][reversing_j] = color
                        reversing_i += dy
                        reversing_j += dx
                    break
                else:
                    break


    def updateStable(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        find_new_stable_chess = True
        while find_new_stable_chess:
            find_new_stable_chess = False
            self.count_total_stable_direct_black = 0
            self.count_total_stable_direct_white = 0
            for i in range(self.row):
                for j in range(self.col):
                    if (self.chesses[i][j] == 1 or self.chesses[i][j] == 2) and not self.stable[i][j]:
                        count_stable_direction = 0
                        for direction in directions:
                            if self.checkDirectionStable(i, j, direction):
                                count_stable_direction += 1
                        if count_stable_direction == 4:
                            find_new_stable_chess = True
                            self.stable[i][j] = 1
                        else:
                            if self.chesses[i][j] == 1:
                                self.count_total_stable_direct_white += count_stable_direction
                            elif self.chesses[i][j] == 2:
                                self.count_total_stable_direct_black += count_stable_direction


    def checkDirectionStable(self, i, j, direction):
        directions = [direction, (-direction[0], -direction[1])]
        color = self.chesses[i][j]
        color_reverse = 3 - color
        count_tmp = 0
        for dx, dy in directions:
            find_unstable_chess = False
            checking_i = i + dy
            checking_j = j + dx
            while True:
                if not (0 <= checking_i < self.row and 0 <= checking_j < self.col):
                    if find_unstable_chess:
                        count_tmp += 1
                        break
                    else:
                        return True
                if self.chesses[checking_i][checking_j] == color:
                    if self.stable[checking_i][checking_j]:
                        return True
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                elif self.chesses[checking_i][checking_j] == color_reverse:
                    if self.stable[checking_i][checking_j]:
                        count_tmp += 1
                        break
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                else:
                    break
        if count_tmp == 2:
            return True
        else:
            return False


    def updateCount(self):
        self.count_black = self.count_white = 0
        self.count_available = 0
        self.count_stable_white = self.count_stable_black = 0
        for i in range(self.row):
            for j in range(self.col):
                chess = self.chesses[i][j]
                if chess == 1:
                    self.count_white += 1
                elif chess == 2:
                    self.count_black += 1
                elif chess == -1:
                    self.count_available += 1
                if self.stable[i][j] == 1:
                    if self.chesses[i][j] == 1:
                        self.count_stable_white += 1
                    elif self.chesses[i][j] == 2:
                        self.count_stable_black += 1
    

    def copy(self):
        chessboard_new = Chessboard()
        chessboard_new.offense = self.offense
        chessboard_new.available = [item for item in self.available]
        for i in range(self.row):
            for j in range(self.col):
                chessboard_new.chesses[i][j] = self.chesses[i][j]
                chessboard_new.stable[i][j] = self.stable[i][j]
        chessboard_new.count_black = self.count_black
        chessboard_new.count_white = self.count_white
        chessboard_new.count_available = self.count_available
        chessboard_new.count_stable_black = self.count_stable_black
        chessboard_new.count_stable_white = self.count_stable_white
        chessboard_new.count_total_stable_direct_black = self.count_total_stable_direct_black
        chessboard_new.count_total_stable_direct_white = self.count_total_stable_direct_white
        return chessboard_new


def setChess(chessboard, px, py):

    set_i = (py - chessboard.margin) // chessboard.width
    set_j = (px - chessboard.margin) // chessboard.width

    chessboard_new = None

    if 0 <= set_i < chessboard.row and 0 <= set_j < chessboard.col and \
    chessboard.chesses[set_i][set_j] == -1:
        chessboard_new = chessboard.copy()
        chessboard_new.chesses[set_i][set_j] = chessboard.offense
        chessboard_new.offense = 3 - chessboard.offense
        chessboard_new.reverse(set_i, set_j)
        chessboard_new.updateAvailable()
        chessboard_new.updateStable()
        chessboard_new.updateCount()

        if chessboard_new.count_available == 0:
            chessboard_new.offense = 3 - chessboard_new.offense
            chessboard_new.updateAvailable()
            chessboard_new.updateCount()

    return chessboard_new


class Images:

    def __init__(self):
        self.width = 50
        self.background = pygame.image.load('images/background.png')
        self.black = pygame.image.load('images/black.png')
        self.white = pygame.image.load('images/white.png')
        self.available = pygame.image.load('images/available.png')
        self.blank = pygame.image.load('images/blank.png')
        # buttons
        self.undo = pygame.image.load('images/undo.png').convert_alpha()
        self.restart = pygame.image.load('images/restart.png').convert_alpha()

def draw(screen, images, chessboard):

    
    screen.blit(images.background, (0, 0))

    width = chessboard.width
    row = chessboard.row
    col = chessboard.col
    margin = chessboard.margin
    for i in range(row + 1):
        for j in range(col + 1):
            pygame.draw.line(screen, (0, 0, 0),
                             (margin + i * width, margin),
                             (margin + i * width, margin + col * width))
            pygame.draw.line(screen, (0, 0, 0),
                             (margin, margin + j * width),
                             (margin + row * width, margin + j * width))

    for i in range(row):
        for j in range(col):
            color = images.blank
            chess = chessboard.chesses[i][j]
            if chess == 1:
                color = images.white
            elif chess == 2:
                color = images.black
            elif chess == -1:
                color = images.available
            screen.blit(color, (margin + j * width + width // 2 - images.width // 2,
                                margin + i * width + width // 2 - images.width // 2))
    
    pos = margin * 2 + chessboard.width * col
    if chessboard.offense == 1:
        screen.blit(images.available, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.white, (pos, pos // 2 + images.width * 0.5))
    else:
        screen.blit(images.black, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.available, (pos, pos // 2 + images.width * 0.5))
    fontObj = pygame.font.Font(None, images.width)
    textSurfaceObj = fontObj.render(str(chessboard.count_black), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 - images.width)
    screen.blit(textSurfaceObj, textRectObj)
    textSurfaceObj = fontObj.render(str(chessboard.count_white), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    screen.blit(images.undo, (680,480))
    screen.blit(images.restart, (680,550))
    

    textSurfaceObj = fontObj.render("Othello Game: Player vs AI", True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (250, 40)
    screen.blit(textSurfaceObj, textRectObj)


class ChessboardTreeNode:

    def __init__(self, chessboard):
        self.parent = None
        self.kids = {}
        self.chessboard = chessboard

    def getScore(self):
        chessboard = self.chessboard
        return 100 * (chessboard.count_stable_white - chessboard.count_stable_black) \
            + (chessboard.count_total_stable_direct_white
               - chessboard.count_total_stable_direct_black)


class ChessboardTree:

    def __init__(self, node):
        self.root = node
        self.expandLayer = 5

    def expandTree(self):
        node = self.root
        for i, j in node.chessboard.available:
            if (i, j) not in node.kids:
                chessboard_new = setChessAI(node.chessboard, i, j)
                node_new = ChessboardTreeNode(chessboard_new)
                node.kids[(i, j)] = node_new
                node_new.parent = node

    def findBestChess(self, player_color):
        scores = {}
        alpha = -6400
        for key in self.root.kids:
            score = self.MaxMin(self.root.kids[key], player_color,
                                self.expandLayer - 1, alpha)
            scores.update({key: score})
            if alpha < score:
                alpha = score
        if not scores:
            return (-1, -1)
        max_key = max(scores, key=scores.get)
        min_key = min(scores, key=scores.get)
        #print(scores[min_key], scores[max_key])
        return max_key

    def MaxMin(self, node, player_color, layer, pruning_flag):
        if layer and node.chessboard.available:
            if node.chessboard.offense == player_color:
                beta = 6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, beta)
                    else:
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, beta)
                    if score <= pruning_flag:
                        beta = score
                        break
                    if beta > score:
                        beta = score
                return beta
            else:
                alpha = -6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, alpha)
                    else:
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, alpha)
                    if score >= pruning_flag:
                        alpha = score
                        break
                    if alpha < score:
                        alpha = score
                return alpha
        else:
            node.chessboard.updateStable()
            node.chessboard.updateCount()
            score = node.getScore()
            return score


def setChessAI(chessboard, set_i, set_j):

    chessboard_new = None

    if 0 <= set_i < chessboard.row and 0 <= set_j < chessboard.col and \
            chessboard.chesses[set_i][set_j] == -1:
        chessboard_new = chessboard.copy()
        chessboard_new.chesses[set_i][set_j] = chessboard.offense
        chessboard_new.offense = 3 - chessboard.offense
        chessboard_new.reverse(set_i, set_j)
        chessboard_new.updateAvailable()
        chessboard_new.updateCount()

        if chessboard_new.count_available == 0:
            chessboard_new.offense = 3 - chessboard_new.offense
            chessboard_new.updateAvailable()

    return chessboard_new

# To Make buttons
class Button():
    def __init__(self, x,y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()  [0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action





def main():

    

    images = Images()

    chessboard = Chessboard()

    node = ChessboardTreeNode(chessboard)
    chessboardTree = ChessboardTree(node)
    chessboardTree.expandTree()

    draw(screen, images, chessboard)
    undo_button = Button(700, 620, images.undo, 1)
    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                set_i = set_j = -1
                if chessboard.offense == player_color:
                    px, py = pygame.mouse.get_pos()
                    set_i = (py - chessboard.margin) // chessboard.width
                    set_j = (px - chessboard.margin) // chessboard.width
                if (set_i, set_j) in chessboard.available:
                    chessboardTree.root = chessboardTree.root.kids[(
                        set_i, set_j)]
                    chessboard = chessboardTree.root.chessboard
                    draw(screen, images, chessboard)
                    pygame.display.update()
                    chessboardTree.expandTree()
                hold = deepcopy(chessboardTree.root.parent)
                
            set_i = set_j = -1
            if chessboard.offense != player_color:
                set_i, set_j = chessboardTree.findBestChess(player_color)
            if (set_i, set_j) in chessboard.available:
                chessboardTree.root = chessboardTree.root.kids[(
                    set_i, set_j)]
                chessboard = chessboardTree.root.chessboard
                draw(screen, images, chessboard)
                pygame.display.update()
                chessboardTree.expandTree()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                if pos1[0] > 685 and pos1[0] < 795 and pos1[1] > 480 and pos1[1] < 530:
                    if chessboardTree.root.parent:
                        chessboardTree.root = hold
                        chessboard = chessboardTree.root.chessboard
                elif pos1[0] > 685 and pos1[0] < 795 and pos1[1] > 550 and pos1[1] < 600:
                    chessboard = Chessboard()
                    node = ChessboardTreeNode(chessboard)
                    chessboardTree = ChessboardTree(node)
                    chessboardTree.expandTree()
                draw(screen, images, chessboard)
                pygame.display.update()


if __name__ == "__main__":
    main()
