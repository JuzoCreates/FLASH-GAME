import pygame as pg
import sys
import FLASH_primarySettings as ps
import os
class Option:
    mouseOver = False
    def __init__(self, img1, img2, position, dimensions, window):
        self.rect = pg.Rect(position[0], position[1], dimensions[0], dimensions[1])
        self.img1 = img1
        self.img2 = img2
        self.dimensions = dimensions
        self.position = position
        self.highlight()
        self.display(window)
    def highlight(self):
        if self.mouseOver == True:
            return(self.img2)
        else:
            return(self.img1)
    def display(self, window):
        img = pg.image.load(self.highlight())
        img = pg.transform.scale(img, self.dimensions)
        window.blit(img, self.position)
        pg.display.update()

def show_Background(background_Image, window):
    background_Image = pg.image.load(background_Image)
    background_Image = pg.transform.scale(background_Image, (ps.windowWidth, ps.windowHeight))
    window.blit(background_Image, (0,0))

def show_high_scores(window):
    """Показывает таблицу рекордов"""
    try:
        scores_file = '/home/Mr.Robot/FLASH-GAME/FLASH_Scores.txt'
        
        if os.path.exists(scores_file):
            with open(scores_file, 'r', encoding='utf-8') as f:
                scores = f.readlines()
        else:
            scores = ["Результатов пока нет!\n"]
            
        # Показать экран с результатами
        show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
        
        font = pg.font.Font(None, 36)
        title = font.render("ТАБЛИЦА РЕКОРДОВ", True, (255, 255, 255))
        window.blit(title, (window.get_width()//2 - title.get_width()//2, 50))
        
        y_pos = 120
        for i, score in enumerate(scores[-10:]):  # Показываем последние 10 результатов
            score_text = font.render(score.strip(), True, (255, 255, 255))
            window.blit(score_text, (50, y_pos))
            y_pos += 40
            
        back_button = Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", 
                           "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", 
                           (10, 10), (100, 50), window)
        
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    waiting = False
                if back_button.rect.collidepoint(pg.mouse.get_pos()):
                    back_button.mouseOver = True
                    back_button.display(window)
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        waiting = False
                else:
                    back_button.mouseOver = False
                    back_button.display(window)
                    
            pg.display.update()
            
    except Exception as e:
        print(f"Ошибка при загрузке результатов: {e}")

def show_Title(title_img, position, size, window):
    title = pg.image.load(title_img)
    title = pg.transform.scale(title, size)
    window.blit(title, position)

def open_Screen(window):
    logo = pg.image.load("FLASH_MenuAssets/FLASH_Logos/FLASH_Title.png")
    logo = pg.transform.scale(logo, (406, 201))
    window.blit(logo, ((ps.windowWidth-406)//2, (ps.windowHeight-201)//2))
    pg.display.update()
    pg.time.wait(2500)
    opacity = 0
    blackScreen = pg.Surface((ps.windowWidth, ps.windowHeight))
    while opacity <= 5:
        blackScreen.set_alpha(opacity)
        window.blit(blackScreen, (0,0))
        opacity += 0.01
        pg.display.update()
    
def main_Menu(difficulty, graphic_Setting, controls, title):
    pg.init()
    window = ps.window
    pg.mouse.set_visible(True)
    pg.display.set_caption('FLASH')
    
    menu = True
    game = True
    help = False
    help_HowToPlay = False
    help_Controls = False
    options = False
    graphics = False
    keybinds = False
    helpP2 = False
    credits = False

    programIcon = pg.image.load('FLASH_MenuAssets/FLASH_Icon.png')
    pg.display.set_icon(programIcon)
    
    while game:
        if title:
            open_Screen(window)
            title = False

        if menu:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
            show_Title("FLASH_MenuAssets/FLASH_Logos/FLASH_Logo.png", (275, 100), (255, 179), window)
            main_Menu_Options = [
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Start.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_StartHighlighted.png", (40, 300), (100, 50), window),
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Help.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_HelpHighlighted.png", (40, 400), (100, 50), window),
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Exit.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_ExitHighlighted.png", (40, 500), (100, 50), window),
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Options.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_OptionsHighlighted.png", (ps.windowWidth-55, ps.windowHeight-55), (50, 50), window),
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Credits.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_CreditsHighlighted.png", (10,10), (100, 50), window)
            ]
    
        while menu:
            menuTime = pg.time.get_ticks() / 1000
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    ps.toggle_fullscreen()
                    window = ps.window
                for option in main_Menu_Options:
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        option.highlight()
                        option.display(window)
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Start.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    return [difficulty, graphic_Setting, controls, menuTime]
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Help.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    menu = False
                                    show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
                                    help = True
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Exit.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    pg.quit()
                                    sys.exit()
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Options.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    menu = False
                                    graphics = True
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Credits.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    credits = True
                                    menu = False
                    else:
                        option.mouseOver = False
                    option.highlight()
                    option.display(window)
                pg.display.update()
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        pg.display.update()

        if help:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_HowToPlayScreen.png", window)
            helpOptions = [
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window),
                Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Next.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_NextHighlighted.png", (ps.windowWidth-110, 10), (100, 50), window)
            ]
        while help:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    ps.toggle_fullscreen()
                    window = ps.window
                for option in helpOptions:
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        option.highlight()
                        option.display(window)
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    help = False
                                    menu = True
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Next.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    helpP2 = True
                                    help = False
                    else:
                        option.mouseOver = False
                    option.highlight()
                    option.display(window)
                pg.display.update()

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        help = False
                        menu = True

            if helpP2:
                show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_HowToPlayControls.png", window)
                helpOptions = [
                    Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)
                ]
            while helpP2:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                        ps.toggle_fullscreen()
                        window = ps.window
                    for option in helpOptions:
                        if option.rect.collidepoint(pg.mouse.get_pos()):
                            option.mouseOver = True
                            option.highlight()
                            option.display(window)
                            if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                                if event.type == pg.MOUSEBUTTONDOWN:
                                    if event.button == 1:
                                        helpP2 = False
                                        menu = True
                        else:
                            option.mouseOver = False
                        option.highlight()
                        option.display(window)
                    pg.display.update()
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            helpP2 = False
                            help = True

        if graphics:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_SettingsMenu.png", window)
            graphicsBack = Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)
        while graphics:
            mouseButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_MouseHighlighted.png" if controls == 0 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Mouse.png"
            keyboardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_KeyboardHighlighted.png" if controls == 1 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Keyboard.png"
            lowButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_LowHighlighted.png" if graphic_Setting == 0 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Low.png"
            mediumButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_MediumHighlighted.png" if graphic_Setting == 1 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Medium.png"
            highButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_HighHighlighted.png" if graphic_Setting == 2 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_High.png"
            easyButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_EasyHighlighted.png" if difficulty == 0 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Easy.png"
            normalButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_NormalHighlighted.png" if difficulty == 1 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Normal.png"
            hardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_HardHighlighted.png" if difficulty == 2 else "FLASH_MenuAssets/FLASH_Buttons/FLASH_Hard.png"
            graphics_Menu_Options = [
                Option(mouseButton, mouseButton, (500, 100), (100, 50), window),
                Option(keyboardButton, keyboardButton, (625, 100), (100, 50), window),
                Option(lowButton, lowButton, (400, 200), (100, 50), window),
                Option(mediumButton, mediumButton, (525, 200), (100, 50), window),
                Option(highButton, highButton, (650, 200), (100, 50), window),
                Option(easyButton, easyButton, (400, 300), (100, 50), window),
                Option(normalButton, normalButton, (525, 300), (100, 50), window),
                Option(hardButton, hardButton, (650, 300), (100, 50), window),
            ]
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    ps.toggle_fullscreen()
                    window = ps.window
                if graphicsBack.rect.collidepoint(pg.mouse.get_pos()):
                    graphicsBack.mouseOver = True
                    graphicsBack.highlight()
                    graphicsBack.display(window)
                    if graphicsBack.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                graphics = False
                                menu = True
                else:
                    graphicsBack.mouseOver = False
                graphicsBack.highlight()
                graphicsBack.display(window)
                for option in graphics_Menu_Options:
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        option.highlight()
                        option.display(window)
                        if option.img1 == easyButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 0
                        if option.img1 == normalButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 1
                        if option.img1 == hardButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 2
                        if option.img1 == lowButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 0
                        if option.img1 == mediumButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 1
                        if option.img1 == highButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 2
                        if option.img1 == mouseButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    controls = 0
                        if option.img1 == keyboardButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    controls = 1
                    else:
                        option.mouseOver = False
                        option.highlight()
                        option.display(window)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        graphics = False
                        menu = True
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                pg.display.update()

        if credits:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_CreditsScreen.png", window)
            pg.display.update()
            backCredits = Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)
        while credits:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_F11:
                    ps.toggle_fullscreen()
                    window = ps.window
                if backCredits.rect.collidepoint(pg.mouse.get_pos()):
                    backCredits.mouseOver = True
                    backCredits.highlight()
                    backCredits.display(window)
                    if backCredits.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                credits = False
                                menu = True
                else:
                    backCredits.mouseOver = False
                backCredits.highlight()
                backCredits.display(window)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        credits = False
                        menu = True

    return [difficulty, graphic_Setting, controls, menuTime]

def settings_Change(settings):
    if settings[0] == 0:
        ps.difficulty = 'easy'
    elif settings[0] == 1:
        ps.difficulty = 'normal'
    elif settings[0] == 2:
        ps.difficulty = 'hard'
    
    if settings[1] == 0:
        ps.screenIterator = 8
        ps.rayIncrementor = 0.08
    elif settings[1] == 1:
        ps.screenIterator = 5
        ps.rayIncrementor = 0.05
    elif settings[1] == 2:
        ps.screenIterator = 2
        ps.rayIncrementor = 0.03
    
    if settings[2] == 0:
        ps.mouseFlag = True
    elif settings[2] == 1:
        ps.mouseFlag = False