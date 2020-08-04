import pygame
import time

x_, y_ = None, None
turn = 1
win = False
tik_tak_toe = [[3 for i in range(3)] for j in range(3)]  # fill matrix with default garbage value 3


def victory_line(matching_type, pattern):  # type 1 -> row wise match | 2-> column wise match | 3 -> Diagonal match
    if matching_type == 1:  # pattern -> 0,1 or 2 => which row
        pygame.draw.line(canvas, (255, 0, 0), (10, pattern * 120 + 60), (340, pattern * 120 + 60), 3)
        pygame.display.flip()
        time.sleep(0.8)
    elif matching_type == 2:  # pattern -> 0,1 or 2 => which column
        pygame.draw.line(canvas, (255, 0, 0), (pattern * 120 + 60, 10), (pattern * 120 + 60, 340), 3)
        pygame.display.flip()
        time.sleep(0.8)
    else:  # pattern -> 1 or 2 => which Diagonal
        if pattern == 1:  # left to right
            pygame.draw.line(canvas, (255, 0, 0), (10, 10), (340, 340), 3)
            pygame.display.flip()
            time.sleep(0.8)
        else:  # right to left
            pygame.draw.line(canvas, (255, 0, 0), (340, 10), (10, 340), 3)
            pygame.display.flip()
            time.sleep(0.8)


def reset(arr):
    for i, e in enumerate(arr):
        if isinstance(e, list):
            reset(e)
        else:
            arr[i] = 3


def show_move(x, y):
    global turn
    if turn == 1:
        # draw cross
        tik_tak_toe[y // 120][x // 120] = 1  # set 3 -> 1 for cross
    else:
        # draw circle
        tik_tak_toe[y // 120][x // 120] = 2  # set 3 -> 2 for circle

    turn = (turn + 1) % 2


def is_win():
    for i in range(3):
        # row wise check
        if tik_tak_toe[i][0] != 3 and all(elem == tik_tak_toe[i][0] for elem in tik_tak_toe[i]):
            victory_line(1, i)
            return tik_tak_toe[i][0]
        # column wise check
        if tik_tak_toe[0][i] != 3:
            if all(tik_tak_toe[j][i] == tik_tak_toe[0][i] for j in range(3)):
                victory_line(2, i)
                return tik_tak_toe[0][i]
    # diagonal
    if tik_tak_toe[0][0] != 3 and all(
            tik_tak_toe[j][j] == tik_tak_toe[0][0] for j in range(3)):  # left to right diagonal
        time.sleep(0.3)
        victory_line(3, 1)
        return tik_tak_toe[0][0]
    if tik_tak_toe[0][2] != 3 and all(
            tik_tak_toe[2 - j][j] == tik_tak_toe[0][2] for j in range(3)):  # right to left diagonal
        victory_line(3, 2)
        return tik_tak_toe[0][2]
    for i in range(3):
        for j in range(3):
            if tik_tak_toe[i][j] == 3:
                return False  # no one wins till now as one or more is field empty
    return "Draw"  # string to signify draw state


def playGUI():
    global x_, y_, win
    while True:
        canvas.fill((49, 150, 100))
        event = pygame.event.wait()  # gets a single event from the event queue
        if event.type == pygame.QUIT:  # if the 'close' button of the window is pressed
            pygame.quit()
            exit()  # stop the execution

        # checker board making
        for i in range(3):
            pygame.draw.line(canvas, (0, 0, 0), (120 * i, 0), (120 * i, 360), 3)
            pygame.draw.line(canvas, (0, 0, 0), (0, 120 * i), (360, 120 * i), 3)

        # if any mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tik_tak_toe[event.pos[1] // 120][event.pos[0] // 120] == 3:
                x_, y_ = (event.pos[0] // 120 * 120), (
                        event.pos[1] // 120 * 120)  # capture the cell location (starting point by pixel)
                pygame.draw.rect(canvas, (255, 0, 0), (x_, y_, 120, 120))  # highlight the selected block
                pygame.draw.rect(canvas, (49, 150, 100), (x_ + 4, y_ + 4, 112, 112))
                show_move(x_, y_)  # Give the move
        elif event.type == pygame.MOUSEBUTTONUP:
            x_, y_ = None, None  # de-select
        for i in range(3):
            for j in range(3):
                if tik_tak_toe[i][j] == 1:
                    pygame.draw.line(canvas, (0, 0, 0), (j * 120 + 20, i * 120 + 20), (j * 120 + 100, i * 120 + 100), 3)
                    pygame.draw.line(canvas, (0, 0, 0), (j * 120 + 20, i * 120 + 100), (j * 120 + 100, i * 120 + 20), 3)
                elif tik_tak_toe[i][j] == 2:
                    pygame.draw.circle(canvas, (0, 0, 255), (j * 120 + 60, i * 120 + 60), 50, 1)
        win = is_win()  # return False if no one wins or player-no if he wins
        while win:
            canvas.fill((49, 150, 100))
            if win == "Draw":
                canvas.blit(font1.render("Players Draw", True, (255, 255, 255)), (25, 100))
            else:
                canvas.blit(font1.render("Player " + str(win) + " Wins", True, (255, 255, 255)), (25, 100))
            canvas.blit(font.render("Click to Exit ...", True, (255, 255, 255)), (130, 190))
            canvas.blit(font.render("PRESS SPACE TO PLAY AGAIN...", True, (255, 255, 255)), (80, 230))
            event = pygame.event.wait()
            if event.type == pygame.QUIT:  # Exit the window
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Exit the match
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset(tik_tak_toe)
                    canvas.fill((49, 150, 100))
                    break
            pygame.display.flip()
        pygame.display.flip()  # update the whole screen


if __name__ == "__main__":
    pygame.init()  # initialize
    font = pygame.font.SysFont('arial rounded mt bold', 20)
    font_ = pygame.font.SysFont('arial', 10)
    font1 = pygame.font.Font('game_over.ttf', 120)
    pygame.display.set_caption("TicTacToe")  # sets the window title
    canvas = pygame.display.set_mode((360, 360))  # sets the window size
    playGUI()
