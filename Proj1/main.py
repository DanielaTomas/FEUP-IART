import pygame
from board import Board
from game_state import GameState
from queue import PriorityQueue
from menu import Menu
from macros import *
import time


def bfs(initial_state):
    queue = [initial_state]
    visited = set() # to not visit the same state twice

    while queue:
        print("queue size " + str(len(queue)))
        state = queue.pop(0)    # get the first state from the queue
        visited.add(state)  # add the state to the visited set
        if state.board.goal_state():
            return state.move_history

        for child in state.children():
            if child not in visited:
                #print(child.board)
                # add the child state to the queue
                queue.append(child)
            #else:
                #print("HELLO1")
    return None 


def a_star_search(initial_state):
    queue = PriorityQueue()
    queue.put(initial_state, 0)
    came_from = {}
    cost_so_far = {}
    cost_so_far[initial_state] = 0  # Set cost of initial state to zero

    while not queue.empty():
        print("queue size " + str(queue.qsize))
        state = queue.get()

        if state.board.goal_state():
            return state.move_history

        for neighbor in state.selected_piece.get_neighbors(state.board.board):
            new_cost = cost_so_far[state] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + GameState.manhattan_distance_heuristic(neighbor)
                queue.put(neighbor, priority)
                came_from[neighbor] = state

    return came_from, cost_so_far


def print_sequence(sequence):
    if sequence:
        print("Steps:", len(sequence))
        print()
        for state in sequence:
            print(state)
            print()
    else:
        print("No solution found")


def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', TILESIZE)
    pygame.display.set_caption('Cohesion')
    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
    menu = Menu(SCREEN_SIZE_LVL1)

    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return

            if menu.isOpen:
                selected_option = menu.handle_events(events)
                if selected_option == 0:
                    board = Board(LVL1_ROWS,LVL1_COLS)
                    print_sequence(a_star_search(GameState(board)))
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
                    selected_piece = None
                    drop_pos = None
                    count = 0
                    start_time = time.time()
                    menu.isOpen = False
                elif selected_option == 1:
                    board = Board(LVL2_ROWS,LVL2_COLS)
                    print_sequence(bfs(GameState(board)))
                    screen = pygame.display.set_mode((SCREEN_SIZE_LVL2[0], SCREEN_SIZE_LVL2[1]))
                    selected_piece = None
                    drop_pos = None
                    count = 0
                    start_time = time.time()
                    menu.isOpen = False     
                elif selected_option == 2:
                    return
                selected_option = None

            else:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if piece is not None:
                        selected_piece = piece, x, y

                if e.type == pygame.MOUSEBUTTONUP:
                    set = board.set_position(drop_pos, selected_piece)
                    if set:
                        count += 1
                    selected_piece = None
                    drop_pos = None

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        screen = pygame.display.set_mode((SCREEN_SIZE_LVL1[0], SCREEN_SIZE_LVL1[1]))
                        menu.selected_option = None
                        menu.isOpen = True

        screen.fill((0, 0, 0))
        if menu.isOpen:
            menu.draw(screen)
        elif board.goal_state():
            board.draw_Goal(screen,True)
        #elif (count > 5 or time.time()-start_time > 30): #TODO change this later for different levels
            #board.draw_Goal(screen,False)
        else:
            board.draw(screen, count, start_time)
            piece, x, y = board.get_square_under_mouse()
            board.draw_pieces(screen, font, selected_piece)
            board.draw_selector(screen, piece)
            drop_pos = board.draw_drag(screen, selected_piece, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()