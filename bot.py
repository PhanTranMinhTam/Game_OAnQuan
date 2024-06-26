import pygame
import os

from game import *
from config import *
from copy import deepcopy
from random import shuffle, choice, randint
from table import fill_if_empty, finished, play_turn

import time
import sys
Lbutton = pygame.image.load(os.path.join(ASSETS, 'left.png'))
Rbutton = pygame.image.load(os.path.join(ASSETS, 'right.png'))
hd_1 = pygame.image.load(os.path.join(ASSETS, 'c.png'))
hand_1 = pygame.transform.scale(hd_1, (70,70))

background_color = (198, 186, 156)

class Bot:
    def __init__(self, player_id, algo=None, screen=None, table=None):
        self.INF = 300
        self.quanvalue = QUANVALUE
        self.player_id = player_id # người chơi thứ 0 hay 1
        self.algo = algo # thuật toán cho người chơi player_id có thể là người chơi bth nếu giá trị là none
        self.screen = screen
        self.table = table

    # Ktra khi game đã kthuc thì số sỏi bên ô phía người nào thì đc cộng dồn vào
    def checking_ending(self, state_, cur_point_):  # (bool_continue?, draw_win_lose)
        state, player_points = deepcopy(state_), deepcopy(cur_point_)

        if finished(state):
            player_points[0] += sum([i[0] for i in state[1:6]])
            player_points[1] += sum([i[0] for i in state[7:12]])

            if player_points[0] > player_points[1]:
                # print("USER_0 win !\n")
                return (True, -100 if self.player_id else 100)
            elif player_points[0] < player_points[1]:
                # print("USER_1 (máy) win !\n")
                return (True, 100 if self.player_id else -100)
            else:
                return (True, 0)

        return (False, player_points[1] if self.player_id else player_points[0])

    def get_available_move(self, state, player_id):
        list_of_action = [] # Ds để lưu trữ các hđông có sẵn

        # inc sẽ xác định phạm vi của các ô
        inc = 6 if player_id else 0 # nếu người chơi 1 thì sẽ xét từ ô 7 -> 12 (5 ô)
        for i in range(1+inc, 6+inc):
            if state[i][0]: # Ktra ô i có sỏi không
                list_of_action.extend([(i, 'l'), (i, 'r')]) # thêm 2 bước di chuyển l và r vào ds list

        return list_of_action

    # Tính giá trị node lá
    def evaluationFunction(self, state, cur_point, is_ending):
        # Nếu game kthuc thì lấy điểm sau khi kết thúc (-INF hoặc INF theo hàm checking_ending)
        # cộng điểm htai của player1(máy) - điểm htai của player2(người)
        # Nếu chưa kthuc thì kh có điểm sau khi kthuc
        player1_score = cur_point[1]
        player0_score = cur_point[0]

        if is_ending[0]:
            return is_ending[1] + (player1_score - player0_score) if self.player_id else is_ending[1] + (player0_score - player1_score)
        return (player1_score - player0_score) if self.player_id else (player0_score - player1_score)

    # cách di chuyển (tương tự hàm play_turn) dành cho máy
    def generate_next_move(self, state_, move, cur_point_, id):  # return next_state,next_point
        state, cur_point = deepcopy(state_), deepcopy(cur_point_)
        inc = 1 if move[1] == 'r' else -1
        cur_pos = move[0]
        next_pos = (cur_pos + inc) % 12

        for _ in range(state[cur_pos][0]):
            state[next_pos][0] += 1
            next_pos = (next_pos + inc) % 12
        state[cur_pos][0] //= 12

        while True:
            # TH dừng
            if state[next_pos][1] or (state[next_pos][0] == 0 and state[(next_pos + inc) % 12][0] == 0 and
                                      state[(next_pos + inc) % 12][1] != 1):
                return state, cur_point
            # TH đc ăn
            elif state[next_pos][0] == 0 and (
                    state[(next_pos + inc) % 12][0] or state[(next_pos + inc) % 12][1] == 1):
                cur_point[id], state[(next_pos + inc) % 12][0] = cur_point[id] + state[(next_pos + inc) % 12][0], 0
                if state[(next_pos + inc) % 12][1] == 1:
                    cur_point[id] += self.quanvalue
                    state[(next_pos + inc) % 12][1] = 2

                if state[(next_pos + inc * 2) % 12][0] == 0 and state[(next_pos + inc * 2) % 12][1] != 1:
                    next_pos = (next_pos + inc * 2) % 12
            # TH đi tiếp
            else:
                cur_pos = next_pos
                next_pos = (cur_pos + inc) % 12
                for _ in range(state[cur_pos][0]):
                    state[next_pos][0] += 1
                    next_pos = (next_pos + inc) % 12
                state[cur_pos][0] //= 12

    def random_algo(self, state_game):
        pos = 0
        if self.player_id:
            while True:
                pos = randint(7, 11) # random ô 7 đến 11
                if state_game[pos][0] != 0: # ktra ô đó có sỏi không
                    break
        else:
            while True:
                pos = randint(1, 5)
                if state_game[pos][0] != 0:
                    break
        # trả về ô đã chọn random và sẽ chọn ngẫu nhiên giữa l và r
        return pos, choice(['l', 'r'])

    def human_player1(self, state_game, cur_point):
        # tạo ds move có move[0] là hộp cần di chuyển, move[1] là hướng đi
        move = [None, None]
        old_box = 0 # theo dõi hộp đã chọn trước đó.
        self.table.redraw()
        x, y = 0, 0 #để lưu trữ tọa độ của chuột trên màn hình.
        isClicked = False  # kiểm tra xem người chơi đã nhấp chuột hay chưa.

        available_boxes = [] # lưu trữ hộp mà người chơi có thể di chuyển đc
        # duyệt và ktra các hộp nào có sỏi thì sẽ đc di chuyển và ngược lại
        for i in range(1,6): # duyệt từ hộp 1 đến 5
            if state_game[i][0] > 0: # ktra hộp i có hạt hay không
                available_boxes.append(i) # Thêm i vào ds lưu trữ hộp mà có thể di chuyển đc

        while True:
            isClicked = False
            # time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        # MOUSEMOTION: cung cấp thông tin về tọa độ của con trỏ chuột sau mỗi lần di chuyển.
        # MOUSEBUTTONDOWN:  cung cấp thông tin về loại nút chuột được nhấp
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # lấy tọa độ của trỏ chuột
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClicked = True
                        # print ("x, y", x, y)

            if 365 < y < 510: # Ktra chuột đang nhập trong phạm vi theo trục y (tức là từ đường kẻ vạch giữa bảng xuống hết bảng)
                if 255 < x < 415: # Ktra chuôt đang click ở ô thứ 1
                    move[0] = 1 # hộp 1 là hộp cần di chuyển
                    if move[0] not in available_boxes: # hộp 1 không có sỏi nào 
                        continue # tiếp tục vòng lặp để chọn lai hộp

            # kiểm tra xem hộp mà người chơi đang chọn (move[0]) có khác với hộp trước đó mà người chơi đã chọn 
            # Nếu khác thì sẽ vẽ lại giao diện, vẽ các nút vào vị trí theo tọa độ và trong phạm vi của ô 1
                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (265, 480))
                        self.screen.blit(Rbutton, (385, 480))
                        self.screen.blit(hand_1, (300, 410))
                        old_box = move[0] # lưu hộp đã chọn lại

                # Nếu được click vào thì chọn hướng đi l và r
                # chọn bằng cách chia ô thành 2 left và right,
                # left đc chọn khi nhập vào tọa độ trc nửa ô và right ngược lại
                    if isClicked:
                        move[1] = 'l' if x < 335 else 'r'

                elif 415 < x < 575: # ô 2
                    move[0] = 2
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (430, 480))
                        self.screen.blit(Rbutton, (540, 480))
                        self.screen.blit(hand_1, (460, 410))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 495 else 'r'
                        # self.screen.blit(layer_bg, (435, 410))
                        # pygame.draw.rect(self.screen, background_color, (435, 410, 120, 65))

                elif 575 < x < 735:  # ô 3
                    move[0] = 3
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (580, 480))
                        self.screen.blit(Rbutton, (695, 480))
                        self.screen.blit(hand_1, (620, 410))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 655 else 'r'
                        # self.screen.blit(layer_bg, (595, 410))
                        # pygame.draw.rect(self.screen, background_color, (595, 410, 120, 65))

                elif 735 < x < 895: # ô 4
                    move[0] = 4
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (740, 480))
                        self.screen.blit(Rbutton, (855, 480))
                        self.screen.blit(hand_1, (780, 410))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 815 else 'r'
                        # self.screen.blit(layer_bg, (755, 410))
                        # pygame.draw.rect(self.screen, background_color, (755, 410, 120, 65))

                elif 895 < x < 1055:  # ô 5
                    move[0] = 5
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (900, 480))
                        self.screen.blit(Rbutton, (1010, 480))
                        self.screen.blit(hand_1, (940, 410))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'l' if x < 975 else 'r'
                        # self.screen.blit(layer_bg, (915, 410))
                        # pygame.draw.rect(self.screen, background_color, (915, 410, 120, 65))
                else:
                    self.table.redraw()
                    old_box = 0

            else:
                self.table.redraw()
                old_box = 0

            pygame.display.update() # cập nhật toàn bộ màn hình giúp trỏ chuột vào sẽ hiển thị các nút
            # pygame.display.update()
            # khi đã xác định đc ô cần di chuyển và hướng đi thì dừng lặp và return
            if move[0] is not None and move[1] is not None:
                break
        return move[0], move[1]
    def human_player2(self, state_game, cur_point):
        # tạo ds move có move[0] là hộp cần di chuyển, move[1] là hướng đi
        move = [None, None]
        old_box = 0 # theo dõi hộp đã chọn trước đó.
        self.table.redraw()
        x, y = 0, 0 #để lưu trữ tọa độ của chuột trên màn hình.
        isClicked = False  # kiểm tra xem người chơi đã nhấp chuột hay chưa.
        available_boxes = [] # lưu trữ hộp mà người chơi có thể di chuyển đc
        # duyệt và ktra các hộp nào có sỏi thì sẽ đc di chuyển và ngược lại
        for i in range(7,12): # duyệt từ hộp 7 đến 11
            if state_game[i][0] > 0: # ktra hộp i có hạt hay không
                available_boxes.append(i) # Thêm i vào ds lưu trữ hộp mà có thể di chuyển đc

        while True:
            isClicked = False
            # time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        # MOUSEMOTION: cung cấp thông tin về tọa độ của con trỏ chuột sau mỗi lần di chuyển.
        # MOUSEBUTTONDOWN:  cung cấp thông tin về loại nút chuột được nhấp
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # lấy tọa độ của trỏ chuột
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0] 
                    y = mouse[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClicked = True


            if 215 < y < 360: # Ktra chuột đang nhập trong phạm vi theo trục y (tức là từ đường kẻ vạch giữa bảng xuống hết bảng)
                if 255 < x < 415: # Ktra chuôt đang click ở ô thứ 11
                    move[0] = 11 # hộp 11 là hộp cần di chuyển
                    if move[0] not in available_boxes: # hộp 11 không có sỏi nào 
                        continue # tiếp tục vòng lặp để chọn lai hộp

            # kiểm tra xem hộp mà người chơi đang chọn (move[0]) có khác với hộp trước đó mà người chơi đã chọn 
            # Nếu khác thì sẽ vẽ lại giao diện, vẽ các nút vào vị trí theo tọa độ và trong phạm vi của ô 1
                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (265, 330))
                        self.screen.blit(Rbutton, (385, 330))
                        self.screen.blit(hand_1, (300, 260))
                        old_box = move[0] # lưu hộp đã chọn lại

                # Nếu được click vào thì chọn hướng đi l và r
                # chọn bằng cách chia ô thành 2 left và right,
                # left đc chọn khi nhập vào tọa độ trc nửa ô và right ngược lại
                    if isClicked:
                        move[1] = 'r' if x < 335 else 'l'
                        # self.screen.blit(layer_bg, (275, 260))
                        # pygame.draw.rect(self.screen, background_color, (275, 260, 120, 65))


                elif 415 < x < 575: # ô 10
                    move[0] = 10
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (430, 330))
                        self.screen.blit(Rbutton, (540, 330))
                        self.screen.blit(hand_1, (460, 260))
                        old_box = move[0]
                    if isClicked:
                        move[1] = 'r' if x < 495 else 'l'
                        # self.screen.blit(layer_bg, (435, 260))
                        # pygame.draw.rect(self.screen, background_color, (275, 260, 120, 65))

                elif 575 < x < 735:  # ô 9
                    move[0] = 9
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (580, 330))
                        self.screen.blit(Rbutton, (695, 330))
                        self.screen.blit(hand_1, (620, 260))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'r' if x < 655 else 'l'
                        # self.screen.blit(layer_bg, (605, 260))
                        # pygame.draw.rect(self.screen, background_color, (275, 260, 120, 65))

                elif 735 < x < 895: # ô 8
                    move[0] = 8
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (740, 330))
                        self.screen.blit(Rbutton, (855, 330))
                        self.screen.blit(hand_1, (780, 260))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'r' if x < 815 else 'l'
                        # self.screen.blit(layer_bg, (755, 260))
                        # pygame.draw.rect(self.screen, background_color, (275, 260, 120, 65))

                elif 895 < x < 1055:  # ô 7
                    move[0] = 7
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw()
                        self.screen.blit(Lbutton, (900, 330))
                        self.screen.blit(Rbutton, (1010, 330))
                        self.screen.blit(hand_1, (940, 260))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'r' if x < 975 else 'l'
                        # self.screen.blit(layer_bg, (915, 260))
                        # pygame.draw.rect(self.screen, background_color, (275, 260, 120, 65))
                else:
                    self.table.redraw()
                    old_box = 0

            else:
                self.table.redraw()
                old_box = 0

            pygame.display.update()
            # khi đã xác định đc ô cần di chuyển và hướng đi thì dừng lặp và return
            if move[0] is not None and move[1] is not None:
                break
        return move[0], move[1]
    
    def alpha_beta_pruning_search(self, state_game, cur_point, depth=3):
        alpha, beta = -self.INF, self.INF

        def minimax_alpha_beta(curState, cur_point, curDepth, maximizingPlayer, alpha, beta):
            is_ending = self.checking_ending(curState, cur_point)  # (bool_continue?, draw_win_lose)
            if is_ending[0] or curDepth == 0:
                return self.evaluationFunction(curState, cur_point, is_ending)

            if maximizingPlayer:
                max_eval = -self.INF
                curState, cur_point = fill_if_empty(curState, cur_point, self.player_id)
                for move in self.get_available_move(curState, self.player_id):
                    next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id)
                    cur_eval = minimax_alpha_beta(next_state, next_point, curDepth - 1, False, alpha, beta)
                    max_eval = max(max_eval, cur_eval)
                    alpha = max(alpha, cur_eval)
                    if alpha >= beta:
                        break
                return max_eval
            else:
                min_eval = self.INF
                curState, cur_point = fill_if_empty(curState, cur_point, self.player_id ^ 1)
                for move in self.get_available_move(curState, self.player_id ^ 1):
                    next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id ^ 1)
                    cur_eval = minimax_alpha_beta(next_state, next_point, curDepth - 1, True, alpha, beta)
                    min_eval = min(min_eval, cur_eval)
                    beta = min(beta, cur_eval)
                    if alpha >= beta:
                        break
                return min_eval

        best_move, score = None, -self.INF
        curState, cur_point = fill_if_empty(state_game, cur_point, self.player_id)
        for move in self.get_available_move(state_game, self.player_id):
            next_state, next_point = self.generate_next_move(curState, move, cur_point, self.player_id)
            cur_score = minimax_alpha_beta(next_state, next_point, depth-1, False, alpha, beta)
            if cur_score > score:
                score = cur_score
                best_move = move
            alpha = max(alpha, score)

        return self.get_available_move(state_game, self.player_id)[0] if best_move is None else best_move

    def execute(self, state_game_, cur_point_, depth=2):
            # copy lại nhằm để tránh ảnh hưởng đến trạng thái ban đầu của biến gốc
        state_game, cur_point = deepcopy(state_game_), deepcopy(cur_point_)

        if self.algo == "human_player1":  ## human play
            return self.human_player1(state_game, cur_point)
        elif self.algo == "human_player2" :
            return self.human_player2(state_game, cur_point)
        elif self.algo == "random":
            return self.random_algo(state_game)
        elif self.algo == "minimax_alpha_beta":
            return self.alpha_beta_pruning_search(state_game, cur_point, depth)
