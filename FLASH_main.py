import pygame as pg
import sys
import os
import FLASH_primarySettings as ps
import FLASH_characters
import FLASH_inanimates
import FLASH_rendering
import FLASH_menu

class MainLoop:
    def __init__(self):
        self.windowHandle = ps.window
        self.mapWidth = 16
        self.mapHeight = 42
        self.clock = pg.time.Clock()
        self.framerate = self.clock.tick(ps.frameLimit)
        self.imagesToLoad = {'wall':ps.wall, 'exit':ps.door, 'background':ps.background, 'far wall':ps.maxWallDistance, 'shadow monster': ps.shadowMonster, 'battery':ps.battery, 'hallucination':ps.hallucination, 'key':ps.key}
        self.UI = {'zero':ps.battery0, 'low':ps.batteryLow, 'med':ps.batteryMed, 'full':ps.batteryFull, 'key':ps.keyIcon}
        self.gameLoopFlag = True
        
    def startup(self, difficulty, screenIterator, mouseFlag):
        
        self.gameMap = FLASH_inanimates.GameMap(self.mapWidth,self.mapHeight, difficulty)
        print("=== MAP DEBUG INFO ===")
        self.gameMap.printMap()  
        print("======================")
        self.startX = self.mapWidth/2 if self.mapWidth%2 == 0 else self.mapWidth//2 + 1
        self.startY = 2
        self.escapeOpacity = 260
        self.camera = FLASH_rendering.Camera(ps.windowWidth, ps.windowHeight, ps.FOV, screenIterator, self.windowHandle)
        self.player = FLASH_characters.PlayerCharacter(self.camera, self.startX, self.startY, 0.0, 0.0, ps.movementControls, mouseFlag, ps.renderingDistance, ps.flashlightRenderingDistance)
        self.player.gameMap = self.gameMap
        self.player.imagesToLoad = self.imagesToLoad 
        self.player.game_start_time = pg.time.get_ticks()
        
        self.shadow = FLASH_characters.ShadowMonster('A', difficulty)
        self.timePaused = 0
        ps.background_music.play(loops=-1)
        ps.fog_level = 0
        ps.fog = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_Fog.png'))
        ps.fog.fill((255,255,255))
        ps.escape = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_Escape.png')).convert_alpha()
        self.UI = {
            'zero': ps.battery0, 
            'low': ps.batteryLow, 
            'med': ps.batteryMed, 
            'full': ps.batteryFull, 
            'key': ps.keyIcon,
            'flashlight_on': ps.flashlight_ui_on,
            'flashlight_off': ps.flashlight_ui_off
        }
        self.player.UI = self.UI 
        
        pg.display.set_caption('FLASH')
        pg.display.set_icon(ps.winIcon)
        pg.mouse.set_visible(False)
    
    def keypressChecks(self, event, menuTime):
        if event.type == pg.KEYDOWN:
            print(f"KEYDOWN: {event.key}")
            if event.key == pg.K_ESCAPE:
                paused = True
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                pg.mixer.music.pause()
                pg.mixer.pause()
                while paused:
                    self.timePaused = (pg.time.get_ticks()/1000)- self.shadow.moveOpportunity - menuTime
                    self.windowHandle.blit(ps.pause,((0,0),(ps.windowWidth,ps.windowHeight)))
                    pg.display.update()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                paused = False
                                pg.mixer.music.unpause()
                                pg.mixer.unpause()
                            elif event.key == pg.K_q:
                                self.gameLoopFlag = False
                                paused = False
                            elif event.key == pg.K_F4 and (pg.key.get_mods() & pg.KMOD_ALT):
                                pg.quit()
                                sys.exit()
                            elif event.key == pg.K_F11:
                                ps.toggle_fullscreen()
                                self.windowHandle = ps.window
                                self.camera.screenWidth = ps.windowWidth
                                self.camera.screenLength = ps.windowHeight
 
            elif event.key == pg.K_F11:
                ps.toggle_fullscreen()
                self.windowHandle = ps.window
                self.camera.screenWidth = ps.windowWidth
                self.camera.screenLength = ps.windowHeight
 
            if self.gameLoopFlag:
                if event.key == pg.K_r:
                    self.player.recharge_flashlight()
                elif event.key == pg.K_f:  # Обработка вспышки
                    # Воспроизводим звук вспышки
                    ps.flashlightSwitchSound.play()
                    # Создаем вспышку
                    self.player.flashlightFlash(self.shadow)
                # ВОТ ЭТО ВАЖНО - ДОБАВЛЯЕМ ВЫЗОВ ДВИЖЕНИЯ ДЛЯ КЛАВИШ WASD
                if event.key in self.player.movementControls:
                    self.player.physicalMovementCalculation(event.key, ps.step)
                
                ps.fog_level = self.player.hideSwitch(event.key, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                
                if not self.player.mouseFlag:
                    self.player.perspectiveMovementCalculation(event.key)
     
        if self.gameLoopFlag:
            if event.type == pg.KEYUP:
                # ВОТ ЭТО ТОЖЕ ВАЖНО - ОСТАНАВЛИВАЕМ ДВИЖЕНИЕ ПРИ ОТПУСКАНИИ КЛАВИШ
                if event.key in self.player.movementControls:
                    self.player.stopPhysicalMovement(event.key, ps.step)
                if not self.player.mouseFlag:
                    self.player.perspectiveStop(event.key)
        
    def mover(self):
        self.player.physicalMover(self.gameMap, ps.pickup, ps.keyPickup)
        self.player.perspectiveMover()
        charx = int(self.player.charX)
        chary = int(self.player.charY)
        if self.gameMap.mapArray[chary][charx] == 'B':
            self.player.extra_batteries += 1
            self.gameMap.mapArray[chary][charx] = '.'
            ps.pickup.play()

    def enemy(self, menuTime):
        self.shadow.update(self.player, self.gameMap, 1/60)
        self.gameMap.enemyAdded(self.shadow) 

    def drawFlashlightLevel(self, window):
        """Отрисовывает уровень заряда фонарика используя картинки из UI"""
        if self.player.flashlight_level == 3:
            battery_img = self.UI['full']
        elif self.player.flashlight_level == 2:
            battery_img = self.UI['med']
        elif self.player.flashlight_level == 1:
            battery_img = self.UI['low']
        else:  # 0
            battery_img = self.UI['zero']
    
        # Рисуем уровень заряда фонарика в левом верхнем углу
        window.blit(battery_img, (10, 10))

    def drawExtraBatteries(self, window):
        """Отрисовывает запасные батарейки в инвентаре"""
        font = pg.font.Font(None, 36)
    
        # Используем маленькую иконку батарейки для инвентаря
        battery_icon = pg.transform.scale(self.UI['zero'], (40, 20))  # Можно изменить размер по необходимости
    
        # Рисуем иконку и количество
        window.blit(battery_icon, (10, 70))
        text = font.render(f"×{self.player.extra_batteries}", True, (255, 255, 255))
        window.blit(text, (55, 65))
        
    def renderScreen(self):
        self.windowHandle = ps.window
        self.windowHandle.fill((0,0,0))
        self.camera.screenWidth = ps.windowWidth
        self.camera.screenLength = ps.windowHeight
        if not self.player.hiding:
            self.player.renderPlayerView(self.gameMap, '.', ['#','E'], self.imagesToLoad, self.shadow, ps.rayIncrementor)
            if self.shadow.fog == True:
                if ps.fog_level <= 150:
                    ps.fog_level += 1
            elif not self.shadow.fog:
                if ps.fog_level > 0:
                    ps.fog_level -= 1
            ps.fog.set_alpha(ps.fog_level)
            ps.window.blit(ps.fog, ps.fog_rect)
        
        if self.player.keyFlag:
            self.windowHandle.blit(self.UI['key'], (self.windowHandle.get_width() - self.UI['key'].get_width(), 0))
        
        # self.player.flashlight.batteries.drawBatteryLevel(self.windowHandle, self.UI)
        self.drawFlashlightLevel(self.windowHandle)  # Отрисовка уровня фонарика
        self.drawExtraBatteries(self.windowHandle)   # Отрисовка запасных батареек
        self.player.drawFlashlightUI(self.windowHandle)
        if self.escapeOpacity > 0:
            self.escapeOpacity -= 1
            self.windowHandle.blit(ps.escape, ((325, 250), (150, 100)))
        if self.escapeOpacity <= 255:
            ps.escape.fill((255, 255, 255, self.escapeOpacity), None, pg.BLEND_RGBA_MULT)

    #def drawFlashlightUI(self, window):
     #   """Отрисовывает фонарик в правом нижнем углу без зазоров"""
     #   if self.player.flashlight.onStatus:
     #       flashlight_img = self.UI['flashlight_on']
     #   else:
     #       flashlight_img = self.UI['flashlight_off']
    
        # Позиция в самом углу без зазоров
      #  pos_x = window.get_width() - flashlight_img.get_width()
     #   pos_y = window.get_height() - flashlight_img.get_height()

      #  window.blit(flashlight_img, (pos_x, pos_y))
    def gameLoop(self, difficulty, screenIterator, mouseFlag, menuTime):
        self.windowHandle = ps.window
        self.windowHandle.fill((0,0,0))
        pg.display.update()
        pg.time.delay(1000)
        self.startup(difficulty, screenIterator, mouseFlag)
        while self.gameLoopFlag:
            if self.player.is_flashing:
                self.player.flash_timer -= self.clock.get_time()
                if self.player.flash_timer <= 0:
                    self.player.is_flashing = False
                    # Возвращаем фонарик в исходное состояние после вспышки
                    self.player.flashlight.onStatus = False
                    
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.keypressChecks(event, menuTime)
            if self.gameLoopFlag:
                if self.player.mouseFlag:
                    self.player.perspectiveMovementCalculation(None)
                    if pg.mouse.get_focused():
                        pg.mouse.set_pos(self.player.initialPos)
                self.mover()
                self.renderScreen()
                self.enemy(menuTime)
                self.framerate = self.clock.tick(ps.frameLimit)
                pg.display.update()
            if self.player.winning == 0 and self.gameLoopFlag:
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                if self.player.hiding:
                    self.player.hideSwitch(pg.K_h, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                pg.mixer.fadeout(6000)
                pg.mixer.music.fadeout(6000)
                ps.background_music.fadeout(6000)
                self.renderScreen()
                pg.display.update()
                self.player.loss(self.clock, self.windowHandle, self.gameMap, '.', ['#','E'], self.imagesToLoad, self.UI, ps.cutscene, self.shadow, ps.gameOverScreen, ps.gameOverNoise, ps.jumpScareNoise, ps.shadowSwoosh, ps.rayIncrementor)
                self.gameLoopFlag = False
            elif self.player.winning == 1:
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                if self.player.hiding:
                    self.player.hideSwitch(pg.K_h, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                pg.mixer.fadeout(6000)
                pg.mixer.music.fadeout(6000)
                ps.background_music.fadeout(6000)
                self.renderScreen()
                pg.display.update()
                self.player.win(self.windowHandle, self.clock, self.gameMap, '.', ['#', 'E'], self.imagesToLoad, self.UI, self.shadow, ps.rayIncrementor, ps.difficulty, ps.win)
                self.gameLoopFlag = False

    def main(self):
        mainFlag = True
        gameFlag = False
        difficulty = 1
        graphic_Setting = 1
        controls = 0
        if sys.platform == 'darwin': 
            title = False
        else:
            title = True
        while mainFlag:
            if not gameFlag:
                settings = FLASH_menu.main_Menu(difficulty, graphic_Setting, controls, title)
                menuTime = settings[3]
                FLASH_menu.settings_Change(settings)
                gameFlag = True
                title = False
                difficulty = settings[0]
                graphic_Setting = settings[1]
                controls = settings[2]
            elif gameFlag:          
                self.gameLoop(ps.difficulty, ps.screenIterator, ps.mouseFlag, menuTime)
                ps.escape.fill((255, 255, 255, 255), None, pg.BLEND_RGBA_MULT)
                self.gameLoopFlag = True
                gameFlag = False

if __name__ == '__main__':
    game = MainLoop()
    game.main()
    pg.quit()