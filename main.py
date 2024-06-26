import pygame, sys
from button import Button
from game import Game 
import os
from config import *

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #Size của trò chơi
pygame.display.set_caption("Ô ĂN QUAN")
#-------------------Đường dẫn background-------------------#
BG = pygame.image.load(os.path.join(ASSETS, 'oanquangmainbg.png')) 
PLAYBG = pygame.image.load(os.path.join(ASSETS, 'bg23.png'))
OPTIONSBG = pygame.image.load(os.path.join(ASSETS, 'bg2s.png'))
#-------------------Đường dẫn FONT-------------------#
def get_font(size):
    return pygame.font.Font(os.path.join(ASSETS, 'font.otf'), size)
def get_subfont(size):
    return pygame.font.Font(os.path.join(ASSETS, 'subfont.otf'), size)
#---------------------Background music--------------------------------#
pygame.mixer.music.load(os.path.join(ASSETS,'choioanquan.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
#-------------------GIAO DIỆN TÙY CHỌN CHƠI-------------------#
def play():
    while True:
        SCREEN.blit(PLAYBG, (0, 0))

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_TEXT = get_font(45).render("LỰA CHỌN CHẾ ĐỘ CHƠI", True, "BROWN")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_AI = Button(image=None, pos=(950, 260),
                            text_input="CHƠI VỚI MÁY", font=get_subfont(70), base_color="BLACK", hovering_color=(186, 147, 109))
        PLAY_VS = Button(image=None, pos=(950, 380),
                            text_input="CHƠI ĐỐI KHÁNG", font=get_subfont(70), base_color="BLACK", hovering_color=(186, 147, 109))
        PLAY_BACK = Button(image=None, pos=(950, 500),
                            text_input="QUAY LẠI", font=get_subfont(70), base_color="BLACK", hovering_color=(186, 147, 109))

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_AI.changeColor(PLAY_MOUSE_POS)
        PLAY_AI.update(SCREEN)
        PLAY_VS.changeColor(PLAY_MOUSE_POS)
        PLAY_VS.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_AI.checkForInput(PLAY_MOUSE_POS):
                    game = Game(algo_0="human_player1", algo_1="minimax_alpha_beta")
                if PLAY_VS.checkForInput(PLAY_MOUSE_POS):
                    game = Game(algo_0="human_player1", algo_1="human_player2")
                game.run()

        pygame.display.update()

#-------------------GIAO DIỆN TÙY CHỌN-------------------#   
def options():
    while True:
        SCREEN.blit(OPTIONSBG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_VOLUME1 = Button(image=None, pos=(250, 120),
                            text_input="ÂM LƯỢNG MẶC ĐỊNH", font=get_subfont(60), base_color=(186, 147, 109), hovering_color="WHITE")
        OPTIONS_VOLUME2 = Button(image=None, pos=(250, 200),
                            text_input="ÂM LƯỢNG TỐI ĐA", font=get_subfont(60), base_color=(186, 147, 109), hovering_color="WHITE")
        OPTIONS_VOLUME0 = Button(image=None, pos=(250, 280),
                            text_input="TẮT ÂM THANH", font=get_subfont(60), base_color=(186, 147, 109), hovering_color="WHITE")
        OPTIONS_BACK = Button(image=None, pos=(250, 360),
                            text_input="QUAY LẠI", font=get_subfont(60), base_color=(186, 147, 109), hovering_color="WHITE")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_VOLUME1.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME1.update(SCREEN)
        OPTIONS_VOLUME2.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME2.update(SCREEN)
        OPTIONS_VOLUME0.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_VOLUME0.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_VOLUME0.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.music.set_volume(0)
                if OPTIONS_VOLUME1.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.music.set_volume(0.5)
                if OPTIONS_VOLUME2.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.music.set_volume(1)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

#-------------------GIAO DIỆN CHÍNH-------------------#   
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Ô ĂN QUAN", True, "#b68f40")
        MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(520, 448), 
                            text_input="CHƠI", font=get_subfont(60), base_color="Black", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(553, 538), 
                            text_input="TÙY CHỌN", font=get_subfont(50), base_color="Black", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(510, 632),
                             text_input="THOÁT", font=get_subfont(50), base_color="Black", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()