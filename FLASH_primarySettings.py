import os
import pygame as pg
import math

############# Settings #############
windowHeight = 600
windowWidth = 800
FOV = math.pi/4
screenIterator = 5
rayIncrementor = 0.05
movementControls = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
mouseFlag = False
renderingDistance = 5
flashlightRenderingDistance = 10
frameLimit = 30
fog_level = 0
fog_rect = pg.Rect(0,0,800,600)
difficulty = 'normal'
mouseSensitivity = 1.0

# Pygame window
pg.init()
window = pg.display.set_mode((windowWidth, windowHeight), pg.HWSURFACE|pg.DOUBLEBUF)
pg.mixer.init()

def toggle_fullscreen():
    global window, windowWidth, windowHeight, fog_rect
    info = pg.display.Info()
    # Если уже fullscreen, вернемся к окну 800x600
    if windowWidth != 800 or windowHeight != 600:
        # Возврат к оконному режиму
        windowWidth, windowHeight = 800, 600
        window = pg.display.set_mode((windowWidth, windowHeight), pg.HWSURFACE | pg.DOUBLEBUF)
    else:
        # Переход в полноэкранный режим (БЕЗ pg.FULLSCREEN)
        windowWidth, windowHeight = info.current_w, info.current_h
        window = pg.display.set_mode((windowWidth, windowHeight), pg.HWSURFACE | pg.DOUBLEBUF)
    fog_rect = pg.Rect(0, 0, windowWidth, windowHeight)

############# Menu Assets #############
pause = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_Pause.png')).convert_alpha()

############# General Assets #############
winIcon = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_Icon.png')).convert_alpha()

############# Game Assets #############
background_music = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_Background.ogg'))
background_music.set_volume(0.9)
win_music = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'Win.ogg'))
win_music.set_volume(0.0)
background = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_Background.png')).convert_alpha()
maxWallDistance = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_MaxWallDistance.jpg')).convert_alpha()
wall = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_Wall.png')).convert_alpha()
door = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_Door.png')).convert_alpha()
battery = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Pickups', 'FLASH_Battery.png')).convert_alpha()
shadowMonster = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Monster', 'FLASH_ShadowMonster.png')).convert_alpha()
hallucination = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Monster', 'FLASH_Hallucination.png')).convert_alpha()
fog = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_Fog.png'))
fog.fill((255,255,255))
gameOverScreen = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_Over.png')).convert_alpha()
key = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Pickups', 'FLASH_Key.png')).convert_alpha()
keyIcon = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_Key.png')).convert_alpha()
escape = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_Escape.png')).convert_alpha()
win = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_Win.png')).convert_alpha()
win = pg.transform.scale(win,(800,600))

step = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_steps.wav'))
step.set_volume(0.5)
monster_step = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_monsterSteps.ogg'))
monster_step.set_volume(0.3)
pickup = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_ding.wav'))
keyPickup = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_discovery.wav'))

cutscene = sorted(os.listdir('FLASH_JumpScare'))
jumpScareNoise = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_jumpscare.ogg'))
gameOverNoise = pg.mixer.Sound(os.path.join(os.path.dirname(__file__), 'FLASH_SoundEffects', 'gameOver.ogg'))
shadowSwoosh = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_swoosh.ogg'))

flashlightHalf = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_FlashlightHalfway.png')).convert_alpha()
flashlightOff = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_FlashlightOff.png')).convert_alpha()
flashlightOn = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_FlashlightOn.png')).convert_alpha()

flashlight_ui_on = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_FlashlightOn.png')).convert_alpha()
flashlight_ui_off = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_FlashlightOff.png')).convert_alpha()

flashlightSwitchSound = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_flashlightOn.wav'))
flashlightSwitchSound.set_volume(0.1)

battery0 =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_Battery0.png')).convert_alpha()
batteryLow =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_BatteryLow.png')).convert_alpha()
batteryMed =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_BatteryMed.png')).convert_alpha()
batteryFull =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_BatteryFull.png')).convert_alpha()

battery_icon_small = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Pickups', 'FLASH_Battery.png')).convert_alpha()
battery_icon_small = pg.transform.scale(battery_icon_small, (30, 15))