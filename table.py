from config import *
import os
from copy import deepcopy
import pygame
from tkinter import *
from tkinter import messagebox
from config import *
import time

background = pygame.image.load(os.path.join(ASSETS, 'bg_oanquan.png'))

# Properties definiton
O_DAN = (50, 50)
O_QUAN = (100, 100)  # ve hinh elipe, (x, y) nghia la truc ngan, truc dai
dan = pygame.image.load(os.path.join(ASSETS, 'dan.png'))
DAN = pygame.transform.scale2x(dan)
QUAN = pygame.image.load(os.path.join(ASSETS, 'quan.png'))
# QUANVALUE = 5
STATISTIC = [0, 0, 0]
TOTAL_SCORE_ = [0, 0] #điểm tổng của hai đối tượng 
HIGHEST_ = [0,0]#

clock = pygame.time.Clock()
dan = pygame.image.load(os.path.join(ASSETS, 'dan.png'))
DAN = pygame.transform.scale2x(dan)

fpsClock = pygame.time.Clock()
FPS = 120

hd_1 = pygame.image.load(os.path.join(ASSETS, 'c.png'))
hand_1 = pygame.transform.scale(hd_1, (70,70))

hd_2 = pygame.image.load(os.path.join(ASSETS, 'a.png'))
hand_2 = pygame.transform.scale(hd_2, (70,70))

hd_3 = pygame.image.load(os.path.join(ASSETS, 'b.png'))
hand_3 = pygame.transform.scale(hd_3, (70,70))

COLOR = Color()
#vẽ màn hình 
def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()#tạo font
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)#size
        textsurface = myfont.render(text, True, color)#màu
        screen.blit(textsurface, (x, y))#vẽ lên màn hình

    except Exception as e:#báo lỗi font
        print('Font Error')
        raise e
    
# Xác định vị trí tiếp theo dựa vào vị trí hiện tại và số sỏi tăng theo chỉ định
def ipos(pos, inc=1):# biết vị trí tiếp theo để rải sỏi
    return (pos + inc) % 12# pos là vị trí hiện tại số 1 inc = 1 bên phải 1 + 1 % 12 = 2 thì sang ô 2 

def fill_if_empty(_state, _player_points, player):
    #Tạo bản sao sâu (deep copy) của trạng thái và điểm của người chơi để không ảnh hưởng đến bản gốc.
    state, player_points = deepcopy(_state), deepcopy(_player_points)

    # Nếu 5 ô của mình kh còn sỏi thì sẽ lấy 5 sỏi mình ăn đc đặt vào 5 ô đó
    #kiểm tra trò chơi đã kết thúc chưa 
    if not finished(state):
        # Kiểm tra đang ở lượt người chơi 0, kiểm tra cột đầu tien user 0 có khác 0 không
        #từ ô 1-5 có sỏi không
        if player == 0 and not any([i[0] for i in state[1:6]]):  # USER_0's field is empty
        # có thì user 0 sẽ giảm 5 sỏi 
            player_points[0] -= 5
        # vòng for duyệt qua các hàng từ 1 - 5 và đặt một sỏi vào ô đầu tiên của user 0
            for i in range(1, 6):
                state[i][0] = 1
        #Tương tự user 0
        if player == 1 and not any([i[0] for i in state[7:12]]):  # USER_1's field is empty
            player_points[1] -= 5
            # từ ô 7 - 11 có sỏi không
            for i in range(7, 12):
                state[i][0] = 1
        
    return state, player_points

# Game kthuc khi 2 ô quan kh còn sỏi hay Quan
def finished(_state):
    return  _state[0] == [0, 2] and _state[6] == [0, 2]
#
def play_turn(self, _state, _player_points, _move, quanvalue=10):
    state, player_points = deepcopy(_state), deepcopy(_player_points)
    move = _move

    # từ ô 1 -> 5 thì xđ ngchoi là 0 và ngược lại
    player = 0 if 0 < move[0] < 6 else 1 # move[0] là ô sẽ đi 
    inc = 1 if move[1] == 'r' else -1#move [1] là hướng đi ô đó 

    cur_pos = move[0] # ô chọn đi mình chọn sẽ  
    next_pos = ipos(cur_pos, inc) # tìm vị trí ô kế tiếp mình chọn để đi
    
    self.state[cur_pos][0] = 0# chọn đi thì ô đó bằng 0 
    for _ in range(state[cur_pos][0]):  # duyệt qua số lượng sỏi có trong ô nguồn 
        self.state[next_pos][0] += 1 # ô tiếp theo sẽ tăng lên 1 
        self.redraw()#vẽ màn hình lại 

        state[next_pos][0] += 1 # một viên sỏi được di chuyển sang ô liền kề next_pos, và số lượng sỏi trong ô đó tăng lên 1. 
        
        if next_pos == 0:hand2x, hand2y = 185, 370
        elif next_pos == 6:hand2x, hand2y = 1055, 370
        elif next_pos in range(1, 6): hand2x, hand2y = 275 + 160 * (next_pos - 1), 410
        else: hand2x, hand2y = 275 + 160 * (11 - next_pos), 260
        #vẽ bàn tay theo tọa độ đã tính 
        self.screen.blit(hand_2, (hand2x, hand2y))
        #update bàn tay 
        pygame.display.update((hand2x, hand2y, hand_2.get_width(), hand_2.get_height()))
        #Xét thời gian bàn tay ngừng đi 
        pygame.time.wait(500)
        #ô kế ô kế 
        next_pos = ipos(next_pos, inc)
        #chỉnh FPS mượt hơn
        fpsClock.tick(FPS)

    # pygame.display.update()
    #Lấy phần nguyên trong ô hiện tại 
    state[cur_pos][0] //= 12  # Tính lại số sỏi còn trong ô đã chọn đi lúc nãy

    while True:

    # Xét TH mất lượt chơi
# Nếu vị trí kế tiếp là ô quan
# hoặc là 2 ô trống liên tiếp kh có sỏi và ô kế kế là ô quan phải thì sẽ mất lượt chơi
# ô quan không được đi tiếp [next_pos][1]
# 2) 2 ô liên tiếp thì mất lượt 
# ô kế tiếp trống và ô kế tiếp ko quan
        if state[next_pos][1] or (state[next_pos][0] == 0 and state[ipos(next_pos, inc)][0] == 0 and state[ipos(next_pos, inc)][1] != 1):
            # stop turn
        # đổi vị tí 0 thanh 1 
            player^=1
        # Hết sỏi thì fill 
            state, player_points = fill_if_empty(state, player_points, player)
            break

    # Xét TH đc ăn
# Nếu ô kế kh có sỏi và (ô kế kế có sỏi hoặc có quan hoặc có cả 2 nói chung ô kế có quân)
# ô trống và ô kế có sỏi hoặc ô kế đó có quan thì được ăn
        elif state[next_pos][0] == 0 and (state[ipos(next_pos, inc)][0] or state[ipos(next_pos, inc)][1] == 1):
            # eatable

            self.redraw()
            if next_pos in range(1, 6):
                x_space, y_space = 275 + 160*(next_pos-1), 415
            elif next_pos in range(7, 12):
                x_space, y_space = 275 + 160*(11-next_pos), 265
            
            self.screen.blit(hand_3, (x_space, y_space))
            # pygame.display.flip()
            pygame.display.update((x_space, y_space, hand_3.get_width(), hand_3.get_height()))

            pygame.time.wait(500)
            # ô ăn là ô quan thì cộng 10  
            # Nếu ô kế kế là có Quan thì sẽ đc ăn Quan
            if state[ipos(next_pos, inc)][1] == 1:
                # if isQuan: update Quan state
                player_points[player] += quanvalue # Cộng điểm khi ăn Quan
            # xong rồi thì 2 ( tức là ko có quan)
                state[ipos(next_pos, inc)][1] = 2
                            
            # cộng điểm khi ăn sỏi
            player_points[player] += state[ipos(next_pos, inc)][0] 
            state[ipos(next_pos, inc)][0] = 0 # ô sau khi bị ăn sẽ kh còn sỏi nào

            # ktra ô kế kế kế (tức là ô kế ô mình vừa mới ăn)
            # kh có sỏi và cũng kh có quan thì gán giá trị ô kế đó cho ô kế tiếp để chạy tiếp vòng lặp 
            

            #tìm vị trí kế ô mình vừa mới ăn có trong hay không nếu có thì 
            temp_pos = ipos(ipos(next_pos, inc), inc)
            # không sỏi không quan
            if state[temp_pos][0] == 0 and state[temp_pos][1] != 1: # empty and not quan
            # next_pos chạy lại vòng while nếu như quan 0 thì dừng, còn nếu như ô trống là ô thường thì chạy tiep các trường hợp
                next_pos = temp_pos
            else:
                player^=1
                state, player_points = fill_if_empty(state, player_points, player)
                break
    # Xét TH tiếp tục chơi tiếp
        else:
            # continue distribution
            cur_pos = next_pos
            next_pos = ipos(cur_pos, inc)

            if cur_pos in range(1, 6): cur_x, cur_y = 275 + 160 * (cur_pos - 1), 415
            elif cur_pos in range(7, 12): cur_x, cur_y = 275 + 160 * (11 - cur_pos), 265
            self.redraw()
            self.screen.blit(hand_1, (cur_x, cur_y))
            pygame.display.update((cur_x, cur_y, hand_1.get_width(), hand_1.get_height()))
            pygame.time.wait(500)

            self.state[cur_pos][0] = 0
            for _ in range(state[cur_pos][0]):  # duyệt qua số lượng sỏi trong ô nguồn
                self.state[next_pos][0] += 1
                self.redraw()
                
                state[next_pos][0] += 1 # một viên sỏi được di chuyển sang ô liền kề next_pos, và số lượng sỏi trong ô đó tăng lên 1. 
                
                if next_pos == 0:hand2x, hand2y = 185, 370
                elif next_pos == 6:hand2x, hand2y = 1055, 370
                elif next_pos in range(1, 6): hand2x, hand2y = 275 + 160 * (next_pos - 1), 410
                else: hand2x, hand2y = 275 + 160 * (11 - next_pos), 260

                # self.screen.blit(DAN, (x, y))
                self.screen.blit(hand_2, (hand2x, hand2y))
                pygame.display.update((hand2x, hand2y, hand_2.get_width(), hand_2.get_height()))
                pygame.time.wait(500)
                next_pos = ipos(next_pos, inc)
                fpsClock.tick(FPS)

            state[cur_pos][0] //= 12  # Tính lại số sỏi còn trong ô đã chọn đi lúc nãy
                
    return state, player_points

class Table:
    def __init__(self): # Khởi tạo trang thái ban đầu với lưới ô và điểm
        # Mỗi ptu của ds chứa 2 giá trị: [số viên sỏi, loại quan]
        # [
        #     [0, 1],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0],
        #     [0, 1],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0],
        #     [5, 0]
        # ]
        self.state = [[0, 1], [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], # của người chơi 1
                      [0, 1], [5, 0], [5, 0], [5, 0], [5, 0], [5, 0]]
        # self.state = [[0, 2], [0, 0], [0, 0], [2, 0], [0, 0], [0, 0], # của người chơi 1
        #               [4, 2], [0, 0], [0, 0], [1, 0], [1, 0], [0, 0]]
        # điểm 2 người chơi
        self.player_points = [0, 0]
        
        self.quanvalue = QUANVALUE # số điểm mà người chơi sẽ nhận được khi họ ăn một quân từ lưới ô của đối phương
        
    def __str__(self): # in bảng trò chơi ra cổng terminal (kh quan trọng hiểu càng tốt)
        return '''
            11 10  9  8  7  6 
        +--+--------------+--+
        |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--+--------------+--+
          0  1  2  3  4  5

        USER_0: {} USER_1: {}
        '''.format(
            # ktra ô đầu có sỏi chưa
                " *" if self.state[0][1] == 1 else " ",
                self.state[11][0] if self.state[11][0] else '',
                self.state[10][0] if self.state[10][0] else '',
                self.state[9][0] if self.state[9][0] else '',
                self.state[8][0] if self.state[8][0] else '',
                self.state[7][0] if self.state[7][0] else '',
                " *" if self.state[6][1] == 1 else " ",  
                self.state[0][0] if self.state[0][0] else '',
                self.state[6][0] if self.state[6][0] else '',
                self.state[1][0] if self.state[1][0] else '',
                self.state[2][0] if self.state[2][0] else '',
                self.state[3][0] if self.state[3][0] else '',
                self.state[4][0] if self.state[4][0] else '',
                self.state[5][0] if self.state[5][0] else '',
                self.player_points[0], self.player_points[1])

    def finished(self):
        if finished(self.state):
            if self.player_points[0] > self.player_points[1]:
                result = 'Người chiến thắng: player 0'
            elif self.player_points[0] < self.player_points[1]:
                result = 'Người chiến thắng: player 1'
            else: result = 'Trận đấu hòa!'
            result += '\nNgười chơi 0: ' + str(self.player_points[0]) + ' điểm'
            result += '\nNgười chơi 1: ' + str(self.player_points[1]) + ' điểm'
            print("END!!")
            
            response = messagebox.askquestion('game over', result + "\nBạn có muốn chơi lại không?", icon='info')
            if response == 'no':
                pygame.quit()

            return True
        else:
            return False

# Sau khi game đã kết thúc thì sẽ cộng số sỏi có trong 5 ô của mình
    def play(self, move):
        self.state, self.player_points = play_turn(self, self.state, self.player_points, move)
        if finished(self.state):
#cộng dồn sỏi còn trên bàn 
            self.player_points[0] += sum([self.state[i][0] for i in range(1, 6)])
            self.player_points[1] += sum([self.state[i][0] for i in range(7, 12)])
        self.redraw()

class TableGUI(Table):
    
    def __init__(self, screen=None):
        super().__init__()
        self.screen = screen
        
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(SCREEN_CAPTION)

    # vẽ các sỏi lên bàn cờ
    def __draw_table(self):
        # vẽ màu trắng đè lên toàn bộ màn hình, để chuẩn bị cho việc vẽ lại trạng thái mới.
        self.screen.fill((255, 255, 255))
        img_bg = pygame.transform.scale(background, (1280,720))
        
        self.screen.blit(img_bg, (0, 0))
        text_to_screen(self.screen, "Player 1", 330, 90, 40, COLOR.DARKRED)
        text_to_screen(self.screen, str(self.player_points[1]), 590, 70, 70, COLOR.DARKRED)
        text_to_screen(self.screen, "Player 0", 785, 580, 40, COLOR.PURPLE)
        text_to_screen(self.screen, str(self.player_points[0]), 590, 565, 70, COLOR.PURPLE)
        
        # So quan trong cac o
        # Viết số sỏi có trong từng ô dân
        text_to_screen(self.screen, str(self.state[11][0]), 270, 215, 30, COLOR.ORANGE) #No. 11
        text_to_screen(self.screen, str(self.state[10][0]), 430, 215, 30, COLOR.ORANGE) #No. 10
        text_to_screen(self.screen, str(self.state[9][0]), 590, 215, 30, COLOR.ORANGE) #No. 9
        text_to_screen(self.screen, str(self.state[8][0]), 750, 215, 30, COLOR.ORANGE) #No. 8
        text_to_screen(self.screen, str(self.state[7][0]), 910, 215, 30, COLOR.ORANGE) #No. 7
        text_to_screen(self.screen, str(self.state[1][0]), 270, 365, 30, COLOR.ORANGE) #No. 1
        text_to_screen(self.screen, str(self.state[2][0]), 430, 365, 30, COLOR.ORANGE) #No. 2
        text_to_screen(self.screen, str(self.state[3][0]), 590, 365, 30, COLOR.ORANGE) #No. 3
        text_to_screen(self.screen, str(self.state[4][0]), 750, 365, 30, COLOR.ORANGE) #No. 4
        text_to_screen(self.screen, str(self.state[5][0]), 910, 365, 30, COLOR.ORANGE) #No. 5

        # Viết số sỏi trong ô quan lần lượt số dân và quan có trong ô 
        text_to_screen(self.screen, str(abs(self.state[0][1] - 2)), 205, 230, 40, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.state[0][0]), 205, 300, 30, COLOR.ORANGE) # Ô quan bên trái

        text_to_screen(self.screen, str(abs(self.state[6][1] - 2)), 1070, 230, 40, COLOR.ORANGE)
        text_to_screen(self.screen, str(self.state[6][0]), 1070, 300, 30, COLOR.ORANGE) # Ô quan bên phải

        # Ve cac Quan
        if (self.state[0][1] == 1):
            self.screen.blit(QUAN, (150, 310))

        if (self.state[6][1] == 1):
            self.screen.blit(QUAN, (1110, 310))

        # Dat soi quan tren o ben trai (hiện tối đa là 8 sỏi trên mỗi ô tính cả ô quan và dân)
        # cách vẽ sỏi theo thứ tự trên dưới
        if (self.state[0][0] >= 1): self.screen.blit(DAN, (125, 370))
        if (self.state[0][0] >= 2): self.screen.blit(DAN, (125, 400))
        if (self.state[0][0] >= 3): self.screen.blit(DAN, (155, 370))
        if (self.state[0][0] >= 4): self.screen.blit(DAN, (155, 400))
        if (self.state[0][0] >= 5): self.screen.blit(DAN, (185, 370))
        if (self.state[0][0] >= 6): self.screen.blit(DAN, (185, 400))
        if (self.state[0][0] >= 7): self.screen.blit(DAN, (215, 370))
        if (self.state[0][0] >= 8): self.screen.blit(DAN, (215, 400))

        # Dat soi quan tren o ben phai
        if (self.state[6][0] >= 1): self.screen.blit(DAN, (1055, 370))
        if (self.state[6][0] >= 2): self.screen.blit(DAN, (1055, 400))
        if (self.state[6][0] >= 3): self.screen.blit(DAN, (1085, 370))
        if (self.state[6][0] >= 4): self.screen.blit(DAN, (1085, 400))
        if (self.state[6][0] >= 5): self.screen.blit(DAN, (1115, 370))
        if (self.state[6][0] >= 6): self.screen.blit(DAN, (1115, 400))
        if (self.state[6][0] >= 7): self.screen.blit(DAN, (1145, 370))
        if (self.state[6][0] >= 8): self.screen.blit(DAN, (1145, 400))

        # Dat soi cho USER_0
        for i in range(1, 6):
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (275 + 160 * (i - 1),415))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (275 + 160 * (i - 1),445))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (305 + 160 * (i - 1),415))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (305 + 160 * (i - 1),445))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (335 + 160 * (i - 1),415))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (335 + 160 * (i - 1),445))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (365 + 160 * (i - 1),415))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (365 + 160 * (i - 1),445))

        # Dat soi cho USER_1
        for i in range(7, 12):
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (275 + 160*(11-i), 265))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (275 + 160*(11-i), 295))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (305 + 160*(11-i), 265))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (305 + 160*(11-i), 295))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (335 + 160*(11-i), 265))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (335 + 160*(11-i), 295))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (365 + 160*(11-i), 265))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (365 + 160*(11-i), 295))

        pygame.display.update()
    
    def redraw(self):
        self.__draw_table()
