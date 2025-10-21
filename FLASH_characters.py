import pygame as pg
import os
import sys
from datetime import date
import random
import math
import FLASH_inanimates
import FLASH_rendering
import FLASH_primarySettings as ps

class Character:
    '''
    Describes a basic character in the game.
    ===============Attributes===============
    charX (int): x-coordinate position of the character
    charY (int): y-coordinate position of the character
    charDelX (float): value for change in x position, essentially x-speed
    charDelY (float): value for change in y position, essentially y-speed
    '''
    def __init__(self, charX, charY, charDelX, charDelY):
        self.charX = charX
        self.charY = charY
        self.charDelX = charDelX
        self.charDelY = charDelY
        
class PlayerCharacter(Character):
    '''
    Describes a playable character in the game, inherits from character.
    ===============Attributes===============
    playerCam (Camera): the player's camera that renders their POV
    charAngle (float): angle of the player relative to the position it was in from initialization
    charDelAngle (float): value for change in angle
    movementControls (List[pygame.key]): list of keys for physical movement, follows the pattern [fwd, bwd, left,right]
    mouseFlag (bool): Determines if the mouse should be used for moving player perspective (if false, use arrow keys instead)
    renderingDistance (int): the max range of the player's unaided eye
    flashlightRenderingDistance (int): the max range of the player's vision with the help of a flashlight
    flashlight (Flashlight): the flashlight object the player holds
    flashlightScreenDivision (int): the number of pixels wide the screen is segmented into
    moving (bool): flag for whether the player is moving or not so the step sound clip is not interrupted by itself
    keyFlag (bool): flag for whether the player has picked up the key
    hiding (bool): flag for whether the player is hiding from the monster
    drain (int): Used to drain battery power every second while flashlight is active.
    offTime (int): Tracks time flashlight is off so battery power cannot drain during that time.
    usage (int): Tracks time flashlight is on so battery power can drain during that time.
    bLid / tLid (pygame.Rect): Sets position of rectangles which are used to obstruct player view when hiding.
    winning (int): integer displaying if the player has won or lost (0 = going to lose, 1 = going to win, 2 = playing)
    initialPos (Tuple[int]): the coordinates of the mouse when the game begins (sometimes not used if the player uses arrow keys)
    '''
    def __init__(self, camera, charX, charY, charAngle, charDelAngle, movementControls, mouseFlag, renderingDistance, flashlightRenderingDistance):
        super().__init__(charX, charY, 0.0, 0.0)
        self.game_start_time = None
        self.playerCam = camera
        self.charAngle = charAngle
        self.charDelAngle = charDelAngle
        self.movementControls = movementControls
        self.mouseFlag = mouseFlag
        self.renderingDistance = renderingDistance
        self.flashlightRenderingDistance = flashlightRenderingDistance
        self.flashlight = FLASH_inanimates.Flashlight(False, 'B')
        self.flashlightScreenDivision = camera.screenWidth // 16
        self.is_flashing = False
        self.flash_timer = 0 
        self.extra_batteries = 2  
        self.max_extra_batteries = 5
        self.flashlight_level = 3  # Уровень заряда фонарика: 3=полный, 2=две полосы, 1=одна полоса, 0=половинчатая(пусто)
        self.moving = False
        self.hiding = False
        self.keyFlag = False
        self.bLid = pg.Rect(0, 600, 800, 300)
        self.tLid = pg.Rect(0, -300, 800, 300)
        self.winning = 2
        if self.mouseFlag:
            self.initialPos = pg.mouse.get_pos()

    def physicalMovementCalculation(self, enteredKey, stepSound):
        if enteredKey in self.movementControls and not self.hiding:
            if enteredKey == self.movementControls[0]:
                self.charDelX = (math.sin(self.charAngle)) * 0.08
                self.charDelY = (math.cos(self.charAngle)) * 0.08
            if enteredKey == self.movementControls[1]:
                self.charDelX = - (math.sin(self.charAngle)) * 0.08
                self.charDelY = - (math.cos(self.charAngle)) * 0.08
            if enteredKey == self.movementControls[2]:
                leftAngle = self.charAngle + (math.pi/2)
                self.charDelX = (-math.sin(leftAngle)) * 0.08
                self.charDelY = (-math.cos(leftAngle)) * 0.08
            if enteredKey == self.movementControls[3]:
                leftAngle = self.charAngle + (math.pi/2)
                self.charDelX = (math.sin(leftAngle)) * 0.08
                self.charDelY = (math.cos(leftAngle)) * 0.08
            if self.moving == False:
                stepSound.play(loops=-1)
                self.moving = True

    def physicalMover(self, gameMap, pickupSound, discoverySound):
        target_x = self.charX + self.charDelX
        target_y = self.charY + self.charDelY
        if (0 <= target_x < gameMap.width and 
            0 <= target_y < gameMap.height and
            not self.hiding):
            target_cell = gameMap.mapArray[int(target_y)][int(target_x)]
            if target_cell in ['.', 'B', 'K', 'E']:
                if target_cell == 'B':
                    gameMap.mapArray[int(target_y)][int(target_x)] = '.'
                    if self.extra_batteries < self.max_extra_batteries:
                        self.extra_batteries += 1
                        pickupSound.play()
                        print(f"Batteries collected: {self.extra_batteries}/{self.max_extra_batteries}")
                    else:
                        print("Inventory full! Cannot collect more batteries.")
                        pickupSound.play()
                elif target_cell == 'K':
                    self.keyFlag = True
                    gameMap.mapArray[int(target_y)][int(target_x)] = '.'
                    discoverySound.play()
                    print("You found a key! The door is unlocked!")
                elif target_cell == 'E':
                    if self.keyFlag: 
                        self.winning = 1
                        print("Exit found! You win!")
                        return
                    else:
                        print("A key is needed to open the door!")
                        return
                if target_cell != 'E' or not self.keyFlag:
                    self.charX = target_x
                    self.charY = target_y

    def stopPhysicalMovement(self, enteredKey, stepSound):
        if enteredKey in self.movementControls:
            self.charDelX = 0.0
            self.charDelY = 0.0
            self.moving = False
            stepSound.stop()

    def perspectiveMovementCalculation(self, enteredKey):
        if not self.mouseFlag:
            if enteredKey == pg.K_LEFT:
                self.charDelAngle = -0.07
            elif enteredKey == pg.K_RIGHT:
                self.charDelAngle = 0.07
        else:
            if pg.mouse.get_focused():
                if pg.mouse.get_pos()[0] < self.initialPos[0]:
                    self.charDelAngle = -0.07
                elif pg.mouse.get_pos()[0] > self.initialPos[0]:
                    self.charDelAngle = 0.07
                elif self.charDelAngle != 0:
                    self.charDelAngle = 0

    def perspectiveMover(self):
        if not self.hiding:
            self.charAngle += self.charDelAngle

    def perspectiveStop(self, enteredKey):
        if (self.charDelAngle < 0 and enteredKey == pg.K_LEFT) or (self.charDelAngle > 0 and enteredKey == pg.K_RIGHT):
            self.charDelAngle = 0

    def flashlightFlash(self, shadow):
        """Создает реальную вспышку, которая мгновенно освещает карту"""
        if self.flashlight_level > 0 and not self.hiding and not self.is_flashing:
            # Устанавливаем состояние вспышки
            self.is_flashing = True
            self.flash_timer = 500  # 500 мс = 0.5 секунды длительность вспышки
       
            # Уменьшаем уровень заряда фонарика
            self.flashlight_level -= 1
            print(f"Flashlight flashed! Battery level: {self.flashlight_level}")
    
            # Временно включаем фонарик для визуального эффекта
            self.flashlight.onStatus = True
    
            # Проверяем, монстр ли в зоне вспышки
            if shadow.get_distance_to_player(self) < 6:
                shadow.state = "scared"
                shadow.scared_timer = 5.0
                shadow.is_flashed = True
                print("Monster is flashed and scared for 5 seconds!")
            else:
                print("No monster in flash range.")
        else:
            if self.flashlight_level <= 0:
                print("Flashlight battery is empty! Recharge first.")
            elif self.hiding:
                print("Cannot flash while hiding!")
            elif self.is_flashing:
                print("Flashlight is already flashing!")

    
    def drawFlashlightUI(self, window):
        """Отрисовывает фонарик в правом нижнем углу без зазоров"""

        # Убедитесь, что у PlayerCharacter есть доступ к UI изображениям
        if not hasattr(self, 'UI') or self.UI is None:
            print("ERROR: PlayerCharacter has no UI reference!")
            return

        if self.is_flashing:
            # Используем текстуру включенного фонарика для вспышки
            flashlight_img = self.UI['flashlight_on']
        elif self.flashlight.onStatus:
            flashlight_img = self.UI['flashlight_on']
        else:
            flashlight_img = self.UI['flashlight_off']
    
        # Позиция в самом углу без зазоров
        pos_x = window.get_width() - flashlight_img.get_width()
        pos_y = window.get_height() - flashlight_img.get_height()
    
        window.blit(flashlight_img, (pos_x, pos_y))
 
    def recharge_flashlight(self):
        """Перезаряжает фонарик одной батарейкой из запаса"""
        if self.extra_batteries > 0 and self.flashlight_level < 3:
            self.extra_batteries -= 1
            self.flashlight_level += 1
            print(f"Flashlight recharged! Battery level: {self.flashlight_level}, Spare batteries: {self.extra_batteries}")
            return True
        else:
            if self.extra_batteries <= 0:
                print("No spare batteries left!")
            elif self.flashlight_level >= 3:
                print("Flashlight is already full!")
            return False

    def renderPlayerView(self, gameMap, groundChar, wallChars, texturesToLoad, shadow, rayIncrementor):
        # Если идет вспышка, используем увеличенную дистанцию рендеринга
        if self.is_flashing:
            current_rendering_distance = self.flashlightRenderingDistance * 0.5
        else:
            current_rendering_distance = self.renderingDistance
    
        for horizontalScreenPixel in range(0, self.playerCam.screenWidth + 1, self.playerCam.screenIterator):
            currentRayAngle = (self.charAngle - (self.playerCam.fov/2)) + ((horizontalScreenPixel/self.playerCam.screenWidth) * self.playerCam.fov)
            extendedRay = FLASH_rendering.Ray(self.charX, self.charY, currentRayAngle, rayIncrementor)
            extendedRay.rayCast(gameMap, groundChar, wallChars, current_rendering_distance)
        
            # Для вспышки используем уменьшенное затемнение
            if self.is_flashing:
                self.playerCam.renderWalls(extendedRay, current_rendering_distance, horizontalScreenPixel, texturesToLoad, self.charY, True, self.flashlightRenderingDistance)
                self.playerCam.renderMapElements(extendedRay, texturesToLoad, current_rendering_distance, self.flashlightRenderingDistance, horizontalScreenPixel, gameMap, shadow)
            else:
                self.playerCam.renderWalls(extendedRay, current_rendering_distance, horizontalScreenPixel, texturesToLoad, self.charY, False, self.flashlightRenderingDistance)
                self.playerCam.renderMapElements(extendedRay, texturesToLoad, current_rendering_distance, self.flashlightRenderingDistance, horizontalScreenPixel, gameMap, shadow)

    def hideSwitch(self, enteredKey, window, clock, texturesToLoad, gameMap, shadow, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect):
        if enteredKey == pg.K_h:
            fog_level = self.hide(window, clock, texturesToLoad, gameMap, shadow, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect)
        return fog_level

    def hide(self, window, clock, texturesToLoad, gameMap, shadow, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect):
        if not self.hiding:
            if shadow.spook == True:
                shadow.spook = False
            self.moving = False
            self.stopPhysicalMovement(pg.K_w, stepSound)
            while self.bLid.top > 300:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                clock.tick(90)
                pg.draw.rect(window, (0, 0, 0), self.bLid)
                pg.draw.rect(window, (0, 0, 0), self.tLid)
                # self.flashlight.batteries.drawBatteryLevel(window, UIDict)
                if self.keyFlag:
                    window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
                self.bLid.top -= 4
                self.tLid.top += 4
                pg.display.update()
            self.hiding = True
        elif self.hiding == True:
            self.hiding = False
            while self.bLid.top < 600:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                clock.tick(90)
                window.fill((0, 0, 0))
                self.renderPlayerView(gameMap, '.', ['#','E'], texturesToLoad, shadow, rayIncrementor)
                if shadow.fog == True:
                    if fog_level <= 150:
                        fog_level += 1
                elif not shadow.fog:
                    if fog_level > 0:
                        fog_level -= 1
                fog.set_alpha(fog_level)
                window.blit(fog, fog_rect)
                pg.draw.rect(window, (0, 0, 0), self.bLid)
                pg.draw.rect(window, (0, 0, 0), self.tLid)
                # self.flashlight.batteries.drawBatteryLevel(window, UIDict)
                if self.keyFlag:
                    window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
                self.bLid.top += 4
                self.tLid.top -= 4
                pg.display.update()
        return fog_level

    def loss(self, clock, window, gameMap, groundChar, wallChars, texturesToLoad, UIDict, cutscene, shadow, overScreen, overSound, jumpscareSound, swoosh, rayIncrementor):
        '''
        Enhanced loss sequence with smoother transitions and better timing
        '''
        startTime = pg.time.get_ticks()
        screenFill = False
        rect = pg.Surface((window.get_width(), window.get_height()))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)

        # Fade to black while still showing the game view
        while not screenFill:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Allow skipping with Enter
                        screenFill = True
                        break
    
            clock.tick(60)
            lossTime = pg.time.get_ticks()
            timeDiff = lossTime - startTime
            if timeDiff > 4000:  # Reduced from 6000 for better pacing
                timeDiff = 4000
            percent = timeDiff / 4000
    
            # Render the final game view
            window.fill((0, 0, 0))
            self.renderPlayerView(gameMap, groundChar, wallChars, texturesToLoad, shadow, rayIncrementor)
    
            # Apply fading black overlay
            rect.set_alpha(255 * percent)
            window.blit(rect, (0,0))
    
            # Draw UI elements
            if self.keyFlag:
                window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
            # self.flashlight.batteries.drawBatteryLevel(window, UIDict)  # Commented out as per your original
    
            pg.display.update()
    
            if timeDiff == 4000:
                screenFill = True

        # Start the jump scare cutscene
        window.fill((0,0,0))
        swoosh.set_volume(0.8)
        scareDelay = random.randint(2000, 3500)  # Reduced delay for better pacing

        # Load all cutscene images first for smoother playback
        cutscene_images = []
        for image_name in cutscene:
            img_path = os.path.join(os.path.dirname('__file__'), 'FLASH_JumpScare', image_name)
            imToLoad = pg.image.load(img_path).convert_alpha()
            # Scale image to window size if needed
            if imToLoad.get_size() != (window.get_width(), window.get_height()):
                imToLoad = pg.transform.scale(imToLoad, (window.get_width(), window.get_height()))
            cutscene_images.append(imToLoad)

        # Play cutscene with improved timing - увеличены задержки для более долгого скримера
        for i, image in enumerate(cutscene_images):
            # Check for quit events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Skip cutscene with Enter
                        break
     
            window.fill((0,0,0))
            original_image_name = cutscene[i]
     
            # Special handling for specific frames - увеличены задержки
            if original_image_name != 'FLASH_21.png' and original_image_name != 'FLASH_02.png':
                if original_image_name == 'FLASH_05.png' or original_image_name == 'FLASH_10.png':
                    swoosh.play()
                elif original_image_name == 'FLASH_22.png':
                    jumpscareSound.play()
                    pg.mixer.fadeout(1500)  # Увеличен fadeout
         
                window.blit(image, (0,0))
                pg.display.update()
                clock.tick(8)  # Немного замедлен кадр для более долгого показа
         
            elif original_image_name == 'FLASH_02.png':
                window.blit(image, (0,0))
                pg.display.update()
                pg.time.delay(500)  # Увеличенная задержка
                swoosh.play()
         
            else:  # FLASH_21.png - the big scare
                window.blit(image, (0,0))
                pg.display.update()
                # Увеличенная задержка для главного скримера
                main_scare_delay = random.randint(2500, 4000)  # Увеличен диапазон
                pg.time.delay(main_scare_delay)
 
        # Transition to game over screen
        pg.time.delay(1500)  # Увеличенная задержка после скримера
        window.fill((0,0,0))
        pg.display.update()
        pg.time.delay(1000)   # Увеличенная задержка
 
        # Scale game over screen to window size
        overScreen_scaled = pg.transform.scale(overScreen, (window.get_width(), window.get_height()))
 
        # Fade in game over screen
        secondStartTime = pg.time.get_ticks()
        secondScreenFill = False
        overSound.play()
 
        fade_surface = pg.Surface((window.get_width(), window.get_height()))
        fade_surface.fill((0, 0, 0))
 
        while not secondScreenFill:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Skip with Enter
                        secondScreenFill = True
                        break
     
            clock.tick(60)
            overTime = pg.time.get_ticks()
            timeDiff = overTime - secondStartTime
            if timeDiff > 2000:  # Ускоренный fade-in (2 секунды)
                timeDiff = 2000
 
            percent = timeDiff / 2000
            fade_surface.set_alpha(255 * (1 - percent))  # Fading out the black overlay
     
            window.blit(overScreen_scaled, (0,0))
            window.blit(fade_surface, (0,0))
            pg.display.update()
     
            if timeDiff == 2000:
                secondScreenFill = True

        # Показываем Game Over экран ровно 1.5 секунды
        pg.time.delay(1500)

        # Затем быстро исчезаем (примерно 1.5 секунды)
        startTime = pg.time.get_ticks()
        screenFill = False
 
        while not screenFill:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  # Skip with Enter
                        screenFill = True
                        break
     
            clock.tick(60)
            fadeOutTime = pg.time.get_ticks()
            timeDiff = fadeOutTime - startTime
            if timeDiff > 1500:  # Fade-out за 1.5 секунды
                timeDiff = 1500

            percent = timeDiff / 1500
            fade_surface.set_alpha(255 * percent)
        
            window.blit(overScreen_scaled, (0,0))
            window.blit(fade_surface, (0,0))
            pg.display.update()

            if timeDiff == 1500:
                screenFill = True
 
        window.fill((0,0,0))
        pg.display.update()

    def win(self, window, clock, gameMap, groundChar, wallChars, texturesToLoad, UIDict, shadow, rayIncrementor, difficulty, win_screen):
        """Display win screen when player escapes"""
        # Stop any movement
        self.charDelX = 0.0
        self.charDelY = 0.0

        # Calculate play time
        if self.game_start_time:
            play_time_seconds = (pg.time.get_ticks() - self.game_start_time) / 1000
        else:
            play_time_seconds = 0

        # Format time as minutes:seconds
        minutes = int(play_time_seconds // 60)
        seconds = int(play_time_seconds % 60)
        time_string = f"{minutes:02d}:{seconds:02d}"

        self.save_score(difficulty, time_string)

        # Scale win screen to window size
        win_screen_scaled = pg.transform.scale(win_screen, (window.get_width(), window.get_height()))

        # Create surfaces for rendering
        fade_surface = pg.Surface((window.get_width(), window.get_height()))
        fade_surface.fill((0, 0, 0))

        # Create a surface for the time text
        font = pg.font.Font(None, 48)
        time_text = font.render(time_string, True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(window.get_width() // 2, 280)) 

        # Start the victory sequence
        ps.win_music.set_volume(0.0)
        ps.win_music.play(loops=-1)

        # 5-second fade in (уменьшено с 12 секунд для лучшего UX)
        fade_in_duration = 5000
        start_time = pg.time.get_ticks()

        while True:
            current_time = pg.time.get_ticks()
            elapsed = current_time - start_time
            progress = min(1.0, elapsed / fade_in_duration)
    
            if progress >= 1.0:
                break
        
            # Smoothly increase music volume and screen opacity
            music_volume = progress
            ps.win_music.set_volume(music_volume)
    
            screen_alpha = int(255 * progress)
            fade_alpha = 255 - screen_alpha
    
            # Render the win screen with current alpha
            window.fill((0, 0, 0))
            win_screen_scaled.set_alpha(screen_alpha)
            window.blit(win_screen_scaled, (0, 0))
    
            # Render time text with the same alpha
            time_text.set_alpha(screen_alpha)
            window.blit(time_text, time_rect)
    
            # Apply fading black overlay
            fade_surface.set_alpha(fade_alpha)
            window.blit(fade_surface, (0, 0))
    
            pg.display.update()
            clock.tick(60)

        # Show the final screen
        window.blit(win_screen_scaled, (0, 0))
        window.blit(time_text, time_rect)
        pg.display.update()

        # Wait for Enter or Escape key
        waiting = True
        print("Press ENTER or ESC to continue...")

        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_ESCAPE:
                        waiting = False
            clock.tick(60)

        # Fade out music and screen (3 секунды)
        fade_out_duration = 3000
        start_time = pg.time.get_ticks()

        while True:
            current_time = pg.time.get_ticks()
            elapsed = current_time - start_time
            progress = min(1.0, elapsed / fade_out_duration)
    
            if progress >= 1.0:
                break
        
            # Smoothly decrease music volume and screen opacity
            music_volume = 1.0 - progress
            ps.win_music.set_volume(music_volume)
    
            fade_alpha = int(255 * progress)
    
            # Render the final screen
            window.blit(win_screen_scaled, (0, 0))
            window.blit(time_text, time_rect)
    
            # Apply fading black overlay
            fade_surface.set_alpha(fade_alpha)
            window.blit(fade_surface, (0, 0))
    
            pg.display.update()
            clock.tick(60)

        # Плавно останавливаем музыку с fadeout
        ps.win_music.fadeout(1000)
        pg.time.delay(1000)  # Даем время для завершения fadeout

        # Final cleanup
        window.fill((0, 0, 0))
        pg.display.update()

    def save_score(self, difficulty, time_string):
        """Сохраняет результат игры в файл"""
        try:
            scores_file = '/home/Mr.Robot/FLASH-GAME/FLASH_Scores.txt'
        
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(scores_file), exist_ok=True)
        
            # Получаем текущую дату
            current_date = date.today().strftime("%Y-%m-%d")
        
            # Форматируем запись
            score_entry = f"Дата: {current_date} | Сложность: {difficulty} | Время: {time_string}\n"
        
            # Записываем в файл (добавляем в конец)
            with open(scores_file, 'a', encoding='utf-8') as f:
                f.write(score_entry)

            print(f"Score saved successfully: {score_entry.strip()}")

        except Exception as e:
            print(f"There was an error saving the score: {e}")

class ShadowMonster(FLASH_inanimates.MapElement):
    def __init__(self, mapChar, difficulty):
        FLASH_inanimates.MapElement.__init__(self, mapChar)
        self.enemyX = 8
        self.enemyY = 35
        self.state = "patrol"
        self.visible = True
        self.chase_timer = 0
        self.fog = False 
        self.moveChoice = None
        self.moveOpportunity = 0
        self.chase = False
        self.spook = False
        self.scared_timer = 0
        self.is_flashed = False
        self.step_sound_timer = 0
        self.step_sound_playing = False
        self.last_step_time = 0
        
        # Используем предзагруженный звук из primarySettings
        self.step_sound = ps.monster_step
        
        if difficulty == 'easy':
            self.speed = 0.015
            self.detection_range = 5
            self.attack_range = 1.5
            self.step_sound_interval = 2000  # Интервал между шагами
            self.patrol_step_chance = 0.3  # 30% chance в патруле
        elif difficulty == 'normal':
            self.speed = 0.02
            self.detection_range = 7
            self.attack_range = 1.3
            self.step_sound_interval = 1500
            self.patrol_step_chance = 0.5  # 50% chance в патруле
        elif difficulty == 'hard':
            self.speed = 0.025
            self.detection_range = 10
            self.attack_range = 1.2
            self.step_sound_interval = 1000
            self.patrol_step_chance = 0.7  # 70% chance в патруле

    def update(self, player, gameMap, delta_time):
        old_x = int(self.enemyX)
        old_y = int(self.enemyY)
        if (0 <= old_x < gameMap.width and 0 <= old_y < gameMap.height and
            gameMap.mapArray[old_y][old_x] == 'A'):
            gameMap.mapArray[old_y][old_x] = '.'
        self.moveOpportunity += delta_time
        self.step_sound_timer += delta_time * 1000
        current_time = pg.time.get_ticks()
        
        if self.state != "scared" and self.is_flashed:
            self.is_flashed = False
            print("Monster can be flashed again!")
            
        distance = self.get_distance_to_player(player)
        
        # ПРОВЕРКА ЛИНИИ ВИДИМОСТИ ДЛЯ ПРЕСЛЕДОВАНИЯ
        can_see_player = self.has_line_of_sight(player, gameMap)
        
        if self.state == "patrol":
            # Начинаем погоню только если видим игрока и нет стены между ними
            if distance < self.detection_range and can_see_player:
                self.state = "chase"
                self.chase = True
                print("Monster started chasing!")
                # При начале погони сразу включаем звук шагов
                self.play_step_sound(player)
            
            self.patrol_behavior(gameMap)
            
            # В режиме патруля воспроизводим звук только иногда
            if (self.step_sound_timer >= self.step_sound_interval and 
                random.random() < self.patrol_step_chance and
                not self.step_sound_playing):
                self.play_step_sound(player)
                self.step_sound_timer = 0
                
        elif self.state == "chase":
            # Проверяем ослепление фонариком
            if (player.flashlight.onStatus and 
                distance < 8 and 
                self.is_monster_in_flashlight_cone(player) and
                not self.is_flashed):
                self.state = "scared"
                self.chase = False
                self.scared_timer = 5.0
                self.is_flashed = True
                # РЕЗКО ОСТАНАВЛИВАЕМ ЗВУК ПРИ ОСЛЕПЛЕНИИ
                self.stop_step_sound()
                print("Monster is scared by the flashlight!")
            elif distance < self.attack_range and can_see_player:
                player.winning = 0
                self.stop_step_sound()  # Останавливаем звук при атаке
                print("Monster caught the player!")
            else:
                # Продолжаем преследование только если видим игрока
                if can_see_player:
                    self.chase_behavior(player, gameMap)
                    # В режиме преследования постоянно воспроизводим звук
                    if not self.step_sound_playing:
                        self.play_step_sound(player)
                else:
                    # Если потеряли видимость, возвращаемся к патрулированию
                    self.state = "patrol"
                    self.chase = False
                    self.stop_step_sound()
                    print("Monster lost sight of player, returning to patrol")
                    
        elif self.state == "scared":
            # В режиме испуга НЕ двигаемся
            self.scared_behavior(player, gameMap)
            self.scared_timer -= delta_time
            # Гарантируем, что звук выключен в режиме испуга
            self.stop_step_sound()
            
            if self.scared_timer <= 0:
                self.state = "patrol"
                self.is_flashed = False
                print("Monster is no longer scared.")

    def play_step_sound(self, player):
        """Воспроизводит звук шагов монстра с правильным объемом"""
        if self.step_sound is None:
            return
            
        distance = self.get_distance_to_player(player)
        max_distance = 20
        volume = max(0, 1.0 - (distance / max_distance))
        volume = min(1.0, max(0.1, volume))
        
        try:
            # Устанавливаем громкость
            self.step_sound.set_volume(volume * 0.3)
            
            # Если звук не воспроизводится, запускаем его с зацикливанием
            if not self.step_sound_playing:
                # Воспроизводим с зацикливанием (loops=-1)
                self.step_sound.play(loops=-1)
                self.step_sound_playing = True
                # print(f"Monster step sound started (looped), volume: {volume * 0.3:.2f}")
            
        except Exception as e:
            print(f"Error playing monster step sound: {e}")
            # Fallback на обычный звук шагов
            if not self.step_sound_playing:
                ps.step.set_volume(volume * 0.5)
                ps.step.play(loops=-1)
                self.step_sound_playing = True

    def stop_step_sound(self):
        """Останавливает звук шагов монстра"""
        if self.step_sound_playing:
            try:
                if self.step_sound:
                    self.step_sound.stop()
                # Также останавливаем fallback звук на всякий случай
                ps.step.stop()
                self.step_sound_playing = False
                # print("Monster step sound stopped")
            except Exception as e:
                print(f"Error stopping monster step sound: {e}")
                self.step_sound_playing = False

    def patrol_behavior(self, gameMap):
        """Поведение при патрулировании - двигается случайно"""
        if self.state == "scared":
            return  # Не двигаемся в режиме испуга
            
        if random.random() < 0.05:
            self.move_randomly(gameMap)

    def chase_behavior(self, player, gameMap):
        """Поведение при преследовании - движется к игроку"""
        self.move_towards_player(player, gameMap)

    def scared_behavior(self, player, gameMap):
        """Поведение при испуге - убегает от игрока"""
        # В режиме испуга монстр не двигается - он замирает на месте
        pass

    def has_line_of_sight(self, player, gameMap):
        """Проверяет, есть ли прямая видимость между монстром и игроком без стен"""
        start_x, start_y = self.enemyX, self.enemyY
        end_x, end_y = player.charX, player.charY
        
        # Используем упрощенный алгоритм проверки линии видимости
        steps = 20  # Количество точек для проверки
        for i in range(steps + 1):
            t = i / steps
            check_x = start_x + (end_x - start_x) * t
            check_y = start_y + (end_y - start_y) * t
            
            # Проверяем, не является ли текущая клетка стеной
            map_x = int(check_x)
            map_y = int(check_y)
            
            if (0 <= map_x < gameMap.width and 0 <= map_y < gameMap.height):
                if gameMap.mapArray[map_y][map_x] == '#':
                    return False  # Стена на пути - нет видимости
                    
        return True  # Достигли игрока без столкновения со стенами

    def is_monster_visible_to_player(self, player, gameMap):
        player_angle = player.charAngle
        monster_angle = math.atan2(self.enemyY - player.charY, self.enemyX - player.charX)
        angle_diff = abs((monster_angle - player_angle + math.pi) % (2 * math.pi) - math.pi)
        return angle_diff < (math.pi/4)
    
    def is_monster_in_flashlight_cone(self, player):
        dx = self.enemyX - player.charX
        dy = self.enemyY - player.charY
        angle_to_monster = math.atan2(dx, dy)
        angle_diff = (angle_to_monster - player.charAngle + math.pi) % (2 * math.pi) - math.pi
        return abs(angle_diff) < (math.pi / 3)

    def move_towards_player(self, player, gameMap):
        dx = player.charX - self.enemyX
        dy = player.charY - self.enemyY
        distance = max(0.1, math.sqrt(dx*dx + dy*dy))
        dx /= distance
        dy /= distance
        new_x = self.enemyX + dx * self.speed
        new_y = self.enemyY + dy * self.speed
        if self.can_move_to(new_x, new_y, gameMap):
            self.enemyX = new_x
            self.enemyY = new_y

    def move_away_from_player(self, player, gameMap):
        dx = player.charX - self.enemyX
        dy = player.charY - self.enemyY
        distance = max(0.1, math.sqrt(dx*dx + dy*dy))
        dx /= distance
        dy /= distance
        new_x = self.enemyX - dx * self.speed
        new_y = self.enemyY - dy * self.speed
        if self.can_move_to(new_x, new_y, gameMap):
            self.enemyX = new_x
            self.enemyY = new_y

    def move_randomly(self, gameMap):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.enemyX + dx * self.speed * 2
            new_y = self.enemyY + dy * self.speed * 2
            if self.can_move_to(new_x, new_y, gameMap):
                self.enemyX = new_x
                self.enemyY = new_y
                break

    def can_move_to(self, x, y, gameMap):
        map_x = int(x)
        map_y = int(y)
        if not (0 <= map_x < gameMap.width and 0 <= map_y < gameMap.height):
            return False
        return gameMap.mapArray[map_y][map_x] == '.'

    def get_distance_to_player(self, player):
        return math.sqrt(
            (player.charX - self.enemyX)**2 + 
            (player.charY - self.enemyY)**2
        )