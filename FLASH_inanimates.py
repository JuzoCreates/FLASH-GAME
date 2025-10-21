import pygame as pg
import FLASH_primarySettings as ps
import random

class GameMap:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.mapArray = self.generateMap(difficulty)
        rowCounter = 0
        for row in self.mapArray:
            columnCounter = 0
            for column in row:
                if column == 'E':
                    self.exitCoord = (columnCounter, rowCounter)
                columnCounter += 1
            rowCounter += 1
        self.width = len(self.mapArray[0])
        self.height = len(self.mapArray)
    
    def randString(self):
        letters = '#.'
        newwall = ''
        for i in range(self.width):
            newwall += (random.choice(letters))
        return newwall

    def newWall(self):
        wallStart = '#'
        wallEnd = '#'
        wallMiddle = self.randString()
        finalWall = wallStart + wallMiddle + wallEnd
        return finalWall

    def generateMap(self, difficultySelect):
        if difficultySelect == 'easy':
            mapDivider = 6
        elif difficultySelect == 'normal':
            mapDivider = 4
        elif difficultySelect == 'hard':
            mapDivider = 2

        gamemap = []
        keyPlace = random.randint(0, self.width - 1)
        keyLine = '#'
        for generation in range(self.width):
            if generation == keyPlace:
                keyLine += 'K'
            else:
                keyLine += '.'
        keyLine += '#'
        for i in range(self.height):
            topWall = "#" + '#' *self.width + '#'
            emptyWalls = "#" + "." *self.width + '#'
            endWall = "#" + '#' *self.width + '#'
            exitSpot = random.randint(0,2)
            if exitSpot == 1:
                exitLine = "E" + "." * self.width + "#"
            else:
                exitLine = "#" + "." * self.width + "E"
            addedWall = self.newWall()
            if addedWall == ("#" + '#' *self.width + '#'):
                addedWall = emptyWalls
            gamemap.append(addedWall)
            gamemap.append(emptyWalls)
        gamemap.insert(0, topWall)
        gamemap.insert(1,emptyWalls)
        gamemap.insert(1,emptyWalls)
        gamemap.append(endWall)
        gamemap.append(endWall)
        exitSpot = random.randint(1,3)
        gamemap.insert(exitSpot, exitLine)
        gamemap.insert(0, topWall)
        gamemap.insert(-2, keyLine)
        rowIterator = 0
        for row in gamemap:
            gamemap[rowIterator] = list(row)
            rowIterator += 1

        section = (self.height * 2) / mapDivider
        nextSection = 1
        tempSection = section
        for batteryPlacement in range(1,mapDivider + 1):
            batteryPlace = random.randint(1, self.width - 2)
            lineChosen = random.randint(int(nextSection),int(tempSection))
            if gamemap[lineChosen][batteryPlace] == 'K':
                gamemap[lineChosen-1][batteryPlace] = 'B'
            else:
                gamemap[lineChosen][batteryPlace] = 'B'
            nextSection += section
            tempSection = section * (batteryPlacement + 1)
        monster_placed = False
        attempts = 0
        while not monster_placed and attempts < 100:
            monster_x = random.randint(1, self.width - 2)
            monster_y = random.randint(3, len(gamemap) - 3)
            if (gamemap[monster_y][monster_x] == '.' and 
                monster_y > 5):
                gamemap[monster_y][monster_x] = 'A'
                monster_placed = True
                print(f"Monster placed at: ({monster_x}, {monster_y})")
            attempts += 1
        if not monster_placed:
            print("Warning: Could not place monster on map!")
        return gamemap

    def printMap(self):
        for row in self.mapArray:
            print(row)
    def removeChar(self, coordinates):
        self.mapArray[coordinates[1]][coordinates[0]] = '.'
    
    def enemyAdded(self, shadow):
        # Сначала убираем старого монстра
        for y in range(self.height):
            for x in range(self.width):
                if self.mapArray[y][x] == 'A':
                    self.mapArray[y][x] = '.'
    
        # Добавляем нового монстра
        enemy_x = int(shadow.enemyX)
        enemy_y = int(shadow.enemyY)
    
        print(f"DEBUG: Monster trying to place at ({enemy_x}, {enemy_y})")
    
        if (0 <= enemy_x < self.width and 
            0 <= enemy_y < self.height):
            if self.mapArray[enemy_y][enemy_x] == '.':
                self.mapArray[enemy_y][enemy_x] = 'A'
                print(f"DEBUG: Monster successfully placed at ({enemy_x}, {enemy_y})")
            else:
                print(f"DEBUG: Cell occupied by '{self.mapArray[enemy_y][enemy_x]}', finding alternative...")
                # Если клетка занята, ищем соседнюю свободную
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in directions:
                   new_x = enemy_x + dx
                   new_y = enemy_y + dy
                   if (0 <= new_x < self.width and 0 <= new_y < self.height and
                       self.mapArray[new_y][new_x] == '.'):
                       self.mapArray[new_y][new_x] = 'A'
                       shadow.enemyX = new_x
                       shadow.enemyY = new_y
                       print(f"DEBUG: Monster moved to ({new_x}, {new_y})")
                       break

class MapElement:
    def __init__(self, mapChar):
        self.mapChar = mapChar

class Flashlight:
    def __init__(self, flashlightFlag, batteryMapChar):
        self.onStatus = flashlightFlag
        self.switching = [False, not flashlightFlag]
        if flashlightFlag:
            self.frame = 0
        else:
            self.frame = 12
        self.onImages = [ps.flashlightHalf, ps.flashlightOff, ps.flashlightOn]
        self.offImages = self.onImages[::-1]
        self.rect = self.onImages[0].get_rect()
        self.rect.x = ps.windowWidth - self.onImages[0].get_width()
        self.rect.y = ps.windowHeight - self.onImages[0].get_height()
        self.batteries = Battery(batteryMapChar)
        
    def drawChanges(self, window, switchSound):
        if self.switching[0] and self.switching[1] == True and self.frame < 12:
            window.blit(self.onImages[(self.frame//4)], self.rect)
            self.frame +=1
        elif self.switching[0] and self.switching[1] == False and self.frame < 12:
            if self.frame == 4:
                self.onStatus = False
                switchSound.play()
            window.blit(self.offImages[(self.frame//4)], self.rect)
            self.frame +=1
        if self.frame == 12:
            if self.switching[1]:
                self.onStatus = True
                switchSound.play()
            self.switching[0] = False
            self.switching[1] = not self.switching[1]
            
    def drawStableState(self, window):
        window.blit(self.onImages[2], self.rect)

class Battery(MapElement):
    def __init__(self, mapChar):
        MapElement.__init__(self, mapChar)
        self.power = 100
        self.drain = 1
        self.batRect = pg.Rect(10,10,100,50)
        self.offTime = None
        self.usage = None

    def deplete(self, flashLightStatus, shadow):
        # Убираем автоматический расход батареи - теперь только при вспышке
        if shadow.moveChoice == 'drain':
            self.power -= 10
            shadow.moveChoice = 'none'
            pg.mixer.music.load('FLASH_SoundEffects/FLASH_shock.wav')
            pg.mixer.music.play(0,0.0)
        
    def drawBatteryLevel(self, window, UIDict):
        if self.power <= 0:
            window.blit(UIDict['zero'], self.batRect)
        elif 1 <= self.power <= 30:
            window.blit(UIDict['low'], self.batRect)
        elif 31 <= self.power <= 60:
            window.blit(UIDict['med'], self.batRect)
        elif 61 <= self.power <= 100:
            window.blit(UIDict['full'], self.batRect) 