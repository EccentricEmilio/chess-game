import pygame
import os
from sys import exit
pygame.init()


# The main class for a piece
class Piece:
    def __init__(self, team, cords, pic, alive, clicked=False, released=False):
        # 0 = White team, 1 = Black team
        # the cords is a tuple with two numbers 0-7, on a 8 by 8 board starting at top left
        # Pic is the pictures file name
        self.clicked = clicked
        self.released = released
        self.team = team
        self.rect = pygame.Rect((cords[0] * 100, cords[1] * 100), (100, 100))
        self.pic = pygame.transform.scale(
            pygame.image.load(os.path.join('Pieces', pic)).convert_alpha(),
            (100, 100),
        )
        self.alive = alive
        self.cords = cords

    def draw(self):
        WIN.blit(self.pic, (self.rect.x, self.rect.y))

    def follow_cursor(self, pos, pressed, movement):
        self.released = False
        new_x = self.rect.x + movement[0]
        new_y = self.rect.y + movement[1]
        wiggle_room = 15

        # pos_pres = is the mouse cursor in the right place
        pos_pres = self.rect.collidepoint(pos) and pressed[0]

        if pos_pres:
            # Checks that no other piece is being dragged
            # Limits it to drag on piece at a time
            self.clicked = True
            for piece in pieces:
                if piece.clicked and piece != self:
                    self.clicked = False

            if self.clicked and \
                    new_y + 100 - wiggle_room < HEIGHT and \
                    new_y + wiggle_room > 0 and \
                    new_x + 100 - wiggle_room < WIDTH and \
                    new_x + wiggle_room > 0:
                self.rect.x += movement[0]
                self.rect.y += movement[1]

        elif self.clicked:
            self.clicked = False
            self.released = True

    def get_new_cords(self, pos):
        if self.released:
            # Creating a rect from the point of the mouse so i know which rectangle on the board collides with
            temp_point = pygame.Rect((pos[0], pos[1]), (1, 1))
            collided = temp_point.collidelist(list_rect)
            # The cords of the rectangle i try to move to
            collided_rect = list_rect[collided]
            new_cords = (collided_rect[0]//100, collided_rect[1]//100)
            return new_cords

    # Checks if the cords the function gets is currently occupied
    # This is used in move() so that you cant have several pieces in the same rectangle
    def check_rect(self):
        pass


# The different classes for all pieces
# I used subclasses for this, in these subclasses i programme the moves
# I had to do King and Knight manually, with a list for possible moves
class Queen(Piece):
    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            new_cords = self.get_new_cords(pos)

            # Side to side and up to down
            if new_cords[0] == self.cords[0] or new_cords[1] == self.cords[1]:
                self.cords = new_cords

            # Top left to Bottom right
            if self.cords[0] - new_cords[0] == self.cords[1] - new_cords[1]:
                self.cords = new_cords

            # Top right to Bottom left
            if new_cords[0] - self.cords[0] == self.cords[1] - new_cords[1]:
                self.cords = new_cords

            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


class King(Piece):
    possible_moves = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
        (1, -1),
        (1, 1),
        (-1, -1),
        (-1, 1),
    ]

    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            new_cords = self.get_new_cords(pos)

            for move in self.possible_moves:
                if (new_cords[0] - move[0], new_cords[1] - move[1]) == self.cords:
                    self.cords = new_cords
                    break

            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


class Bishop(Piece):
    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            new_cords = self.get_new_cords(pos)

            # Top left to Bottom right
            if self.cords[0] - new_cords[0] == self.cords[1] - new_cords[1]:
                self.cords = new_cords

            # Top right to Bottom left
            if new_cords[0] - self.cords[0] == self.cords[1] - new_cords[1]:
                self.cords = new_cords

            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


class Knight(Piece):
    possible_moves = [
        (-2, -1),
        (-2, +1),
        (-1, -2),
        (-1, +2),
        (+1, -2),
        (+1, +2),
        (+2, -1),
        (+2, +1),
    ]

    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            new_cords = self.get_new_cords(pos)

            for move in self.possible_moves:
                if (new_cords[0] - move[0], new_cords[1] - move[1]) == self.cords:
                    self.cords = new_cords
                    break

            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


class Rook(Piece):
    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            new_cords = self.get_new_cords(pos)

            # Up down side to side
            if new_cords[0] == self.cords[0] or new_cords[1] == self.cords[1]:
                self.cords = new_cords

            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


class Pawn(Piece):
    def __init__(self, team, cords, pic, alive):
        super().__init__(team, cords, pic, alive)

    def move(self, pos):
        if self.released:
            # Calls the function from the base class
            new_cords = self.get_new_cords(pos)
            # Which team the Pawn is on
            if self.team == 0:
                # the Y cord changes by 1
                changed_cords = (new_cords[0], new_cords[1] + 1)
            else:
                changed_cords = (new_cords[0], new_cords[1] - 1)

            # Checks if changed cords are the same as self.cords, if they are the piece can move
            if changed_cords == self.cords:
                self.cords = new_cords

            # Updates the pieces pos
            self.rect.update((self.cords[0] * 100, self.cords[1] * 100), (100, 100))


# The main surface
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Constants
clock = pygame.time.Clock()
FPS = 60
list_rect = []

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
brown = (101, 67, 33)
light_brown = (190, 121, 49)

# All the pieces
pieces = [
    # White pieces
    Queen(0, (3, 7), 'WQ.png', True),
    King(0, (4, 7), 'WK.png', True),

    Bishop(0, (5, 7), 'WB.png', True),
    Bishop(0, (2, 7), 'WB.png', True),

    Knight(0, (6, 7), 'WKN.png', True),
    Knight(0, (1, 7), 'WKN.png', True),

    Rook(0, (7, 7), 'WR.png', True),
    Rook(0, (0, 7), 'WR.png', True),

    Pawn(0, (0, 6), 'WP.png', True),
    Pawn(0, (1, 6), 'WP.png', True),
    Pawn(0, (2, 6), 'WP.png', True),
    Pawn(0, (3, 6), 'WP.png', True),
    Pawn(0, (4, 6), 'WP.png', True),
    Pawn(0, (5, 6), 'WP.png', True),
    Pawn(0, (6, 6), 'WP.png', True),
    Pawn(0, (7, 6), 'WP.png', True),

    # Black pieces
    Queen(1, (3, 0), 'BQ.png', True),
    King(1, (4, 0), 'BK.png', True),

    Bishop(1, (5, 0), 'BB.png', True),
    Bishop(1, (2, 0), 'BB.png', True),

    Knight(1, (1, 0), 'BKN.png', True),
    Knight(1, (6, 0), 'BKN.png', True),

    Rook(1, (7, 0), 'BR.png', True),
    Rook(1, (0, 0), 'BR.png', True),

    Pawn(1, (1, 1), 'BP.png', True),
    Pawn(1, (2, 1), 'BP.png', True),
    Pawn(1, (3, 1), 'BP.png', True),
    Pawn(1, (4, 1), 'BP.png', True),
    Pawn(1, (5, 1), 'BP.png', True),
    Pawn(1, (6, 1), 'BP.png', True),
    Pawn(1, (7, 1), 'BP.png', True),
    Pawn(1, (0, 1), 'BP.png', True),
]


# Creates the boards rectangles cords
def set_up_board():
    global list_rect

    # Creates a list of cords for all 64 rectangles on the board
    list_rect_cords = []
    num1 = 0
    num2 = 0
    while num1 != 8:
        list_rect_cords.append((num1, num2))
        num2 += 1
        if num2 == 8:
            num2 = 0
            num1 += 1
            if num1 == 8:
                break

    # Creates a list of all rectangles on the board
    # This is using the list of cords
    for rect in list_rect_cords:
        temp_rect = pygame.Rect((rect[0] * 100, rect[1] * 100), (100, 100))
        list_rect.append(temp_rect)


# Draws everything
def draw(rectangles):
    # Fills the entire screen with brown
    WIN.fill(brown)

    # Checks if rect is a light brown rectangle
    for rect in rectangles:
        # If the cords together is even, its a white square
        if (rect[0]/100 + rect[1]/100) % 2 == 0:
            pygame.draw.rect(
                WIN,
                light_brown,
                rect,
            )

    # Draws the pieces
    for piece in pieces:
        piece.draw()


# A loop where i call the functions for all pieces (objects)
def pieces_loop():
    # Data of the mouse that is needed to move the pieces
    movement = pygame.mouse.get_rel()
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()

    # The loop
    for piece in pieces:
        piece.follow_cursor(pos, pressed, movement)
        piece.move(pos)


# Main loop
def main():
    set_up_board()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pieces_loop()

        draw(list_rect)
        pygame.display.update()


if __name__ == '__main__':
    main()
