import random
import copy
import pygame,sys 

import math
import time
import concurrent.futures
import os

from table import *
from bot import Bot
from config import *

class Game:
    def __init__(self, algo_0=None, algo_1=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.bots = [Bot(0, algo_0, self.screen, self.table), Bot(1, algo_1, self.screen, self.table)]
        self.move = None

    #  để cập nhật trạng thái trò chơi sau mỗi nước đi của người chơi.
    def update(self, move):
        self.table.play(move) #thực hiện nước đi move

    def run(self):
        turn = 0 if USER_GO_FIRST else 1
        # turn = 1 if USER_GO_FIRST else 0
        running = True

        # loop
        self.table.redraw()
        while not self.table.finished():
            # để lấy danh sách các sự kiện từ pygame.
            for event in pygame.event.get():
                # nếu sự kiện là đóng cửa sổ 
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit();sys.exit()#pygame.quit() để thoát khỏi pygame và sys.exit() để kết thúc chương trình. 				
                    
            time.sleep(1)
            
            move = self.bots[turn].execute(self.table.state, self.table.player_points)
            
            self.update(move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")

            #  Đảo giá trị của biến turn để chuyển lượt chơi cho người chơi tiếp theo.
            turn ^= 1 # như toán tử XOR đổi 2 giá trị 0 và 1
            self.table.redraw()
            
            # in ra bàn chơi ở terminal
            print(self.table)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()