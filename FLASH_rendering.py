import pygame as pg
import math

class Camera:
    def __init__(self, screenWidth, screenLength, fov, screenIterator, pgScreenHandle):
        self.screenWidth = screenWidth
        self.screenLength = screenLength
        self.fov = fov
        self.screenIterator = screenIterator
        self.pgScreenHandle = pgScreenHandle

    def renderWalls(self, extendedRay, renderingDistance, horizontalScreenPixel, texturesToLoad, charY, flashlightFlag, flashlightRender):
        if extendedRay.distanceToObstruction <= renderingDistance:
            if extendedRay.obstructionChar == '#':
                texture = texturesToLoad['wall']
                ceiling = int(self.screenLength/2 - self.screenLength/extendedRay.distanceToObstruction)
            
                # Для вспышки используем меньшее затемнение
                if flashlightFlag:
                    percent = extendedRay.distanceToObstruction / renderingDistance * 0.3  # 30% затемнения для вспышки
                else:
                    percent = extendedRay.distanceToObstruction/ renderingDistance
                
                lineLength = self.screenLength - (ceiling*2)
                if(int(charY + (extendedRay.yRayUnitVector*(extendedRay.distanceToObstruction - extendedRay.rayIncrementor))) != int(extendedRay.yTestUnitVector)):
                    rayTest = extendedRay.xTestUnitVector % 1  
                else:
                    rayTest = extendedRay.yTestUnitVector % 1
            
                textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))           
                drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                drawnImage = texture.subsurface(drawnImageRect)
                scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                darkRectangle.fill((0,0,0,(255)*percent))
                self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
            elif extendedRay.obstructionChar == 'E':
                texture = texturesToLoad['exit']
                ceiling = int(self.screenLength/2 - self.screenLength/extendedRay.distanceToObstruction)
            
                # Для вспышки используем меньшее затемнение
                if flashlightFlag:
                    percent = extendedRay.distanceToObstruction / renderingDistance * 0.3  # 30% затемнения для вспышки
                else:
                    percent = extendedRay.distanceToObstruction/ renderingDistance
                
                lineLength = self.screenLength - (ceiling*2)
                if(int(charY + (extendedRay.yRayUnitVector*(extendedRay.distanceToObstruction - extendedRay.rayIncrementor))) != int(extendedRay.yTestUnitVector)):
                    rayTest = extendedRay.xTestUnitVector % 1  
                else:
                    rayTest = extendedRay.yTestUnitVector % 1
            
                textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))           
                drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                drawnImage = texture.subsurface(drawnImageRect)
                scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                darkRectangle.fill((0,0,0,(255)*percent))
                self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
            
        else:
            texture = texturesToLoad['far wall']
            if flashlightFlag:  # Во время вспышки показываем дальние стены
                ceiling = int(self.screenLength/2 - self.screenLength/flashlightRender)
            else:
                ceiling = int(self.screenLength/2 - self.screenLength/renderingDistance)
            lineLength = self.screenLength - (ceiling*2)
            drawnImageRect = pg.Rect(0, 0, self.screenIterator, lineLength)
            drawnImage = texture.subsurface(drawnImageRect)
            scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
            self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
   
    def renderMapElements(self, extendedRay, texturesToLoad, renderingDistance, flashlightRenderingDistance, horizontalScreenPixel, gameMap, shadow):
        if extendedRay.objectsHit != []:
            extendedRay.objectsHit.reverse()
            for pointData in extendedRay.objectsHit:
                # Для всех объектов во время вспышки используем уменьшенное затемнение
                if pointData[0] == 'A':  # Монстр
                    texture = texturesToLoad['shadow monster']
                    if texture:
                        distance = max(0.1, pointData[1])
                        wall_height = (self.screenLength / distance) * 2
                        ceiling = max(0, int((self.screenLength - wall_height) / 2))
                        lineLength = int(wall_height)
                    
                        # Для вспышки используем меньшее затемнение
                        percentVision = min(1.0, distance / renderingDistance * 0.3)  # 30% затемнения
                        rayTest = max(0.0, min(1.0, pointData[2]))
                    
                        textureXPos = int((texture.get_width() - self.screenIterator) * rayTest)
                        drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                        drawnImage = texture.subsurface(drawnImageRect)
                        scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                     
                        darkRectangle = pg.Surface((self.screenIterator, lineLength)).convert_alpha()
                        darkRectangle.fill((0, 0, 0, int(255 * percentVision)))
                    
                        self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                        self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                elif pointData[0] == 'B':
                    texture = texturesToLoad['battery']
                    ceiling = int(self.screenLength/2 - self.screenLength/(pointData[1]*1.25))
                    percentVision = pointData[1]/renderingDistance
                    lineLength = self.screenLength - (ceiling*2)
                    rayTest = pointData[2]
                    textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                    drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                    drawnImage = texture.subsurface(drawnImageRect)
                    scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                    darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                    darkRectangle.fill((0,0,0,(255)*percentVision))
                    self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                    self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                elif pointData[0] == 'K':
                    texture = texturesToLoad['key']
                    ceiling = int(self.screenLength/2 - self.screenLength/(pointData[1]*1.25))
                    percentVision = pointData[1]/renderingDistance
                    lineLength = self.screenLength - (ceiling*2)
                    rayTest = pointData[2]
                    textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                    drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                    drawnImage = texture.subsurface(drawnImageRect)
                    scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                    darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                    darkRectangle.fill((0,0,0,(255)*percentVision))
                    self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                    self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                     
                elif pointData[0] == 'H':
                    if renderingDistance != flashlightRenderingDistance:
                        texture = texturesToLoad['hallucination']
                        ceiling = int(self.screenLength/2 - self.screenLength/pointData[1])
                        percentVision = pointData[1]/renderingDistance
                        lineLength = self.screenLength - (ceiling*2)
                        rayTest = pointData[2]
                        textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                        drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                        drawnImage = texture.subsurface(drawnImageRect)
                        scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                        darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                        darkRectangle.fill((0,0,0,(255)*percentVision))
                        self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                        self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                    else:
                        gameMap.removeChar(pointData[3])
                        shadow.spook = False

class Ray:
    def __init__(self, originX, originY, rayA, rayIncrementor):
        self.originX = originX
        self.originY = originY
        self.rayA = rayA
        self.xRayUnitVector = math.sin(rayA)
        self.yRayUnitVector = math.cos(rayA)
        self.distanceToObstruction = 0.0
        self.rayIncrementor = rayIncrementor
        self.objectsHit = []
        self.obstructionHit = False

    def rayCast(self, gameMap, groundChar, wallChars, renderingDistance):
        self.distanceToObstruction = 0.000001
        while (not self.obstructionHit) and (self.distanceToObstruction < renderingDistance):
            self.distanceToObstruction += self.rayIncrementor 
            self.xTestUnitVector = self.originX + (self.xRayUnitVector * self.distanceToObstruction)
            self.yTestUnitVector = self.originY + (self.yRayUnitVector * self.distanceToObstruction)
            if 0 <= self.xTestUnitVector <= (gameMap.width) and 0 <= self.yTestUnitVector <= (gameMap.height):
                if gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] != groundChar:
                    if not gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] in wallChars:
                        objectHitAlready = False
                        for hitInstances in self.objectsHit:
                            if hitInstances[0] == gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)]:
                                objectHitAlready = True
                                break
                        if not objectHitAlready:
                            try:
                                centerPoint = (int(self.xTestUnitVector)+0.5,int(self.yTestUnitVector)+0.5)
                                playerXDiff = centerPoint[0] - self.originX
                                playerYDiff = centerPoint[1] - self.originY
                                playerPerspectiveSlope = playerYDiff/playerXDiff
                                objLineSlope = -1/playerPerspectiveSlope
                                if abs(objLineSlope) > 1000000000:
                                    playerPerspectiveSlope = 0
                                    raise ZeroDivisionError
                                yOffset = centerPoint[1]- (centerPoint[0]*objLineSlope)
                                a = 1 + (objLineSlope**2)
                                b = 2*(-centerPoint[0]) + 2*objLineSlope*(yOffset -centerPoint[1])
                                c = (centerPoint[0]**2) + ((yOffset-centerPoint[1])**2) -0.25
                                circleObjXIntersect1 = (-b + (((b**2) - (4*a*c))**0.5))/(2*a)
                                circleObjYIntersect1 = (circleObjXIntersect1*objLineSlope) + yOffset
                                circleObjXIntersect2 = (-b - (((b**2) - (4*a*c))**0.5))/(2*a)
                                circleObjYIntersect2 = (circleObjXIntersect2*objLineSlope) + yOffset
                                dVal = ((self.xTestUnitVector - circleObjXIntersect1)*(circleObjYIntersect2 - circleObjYIntersect1)) - ((self.yTestUnitVector - circleObjYIntersect1)*(circleObjXIntersect2 - circleObjXIntersect1))
                                if (dVal >= 0 and self.originY <= centerPoint[1]) or (dVal <= 0  and self.originY >= centerPoint[1]):
                                    circleCheck = ((self.xTestUnitVector - centerPoint[0])**2) + ((self.yTestUnitVector - centerPoint[1])**2)
                                    if circleCheck < 0.25:
                                        pointInFlag = True
                                    else:
                                        pointInFlag = False
                                else:
                                    pointInFlag = False
                            except ZeroDivisionError:
                                if (self.originX < centerPoint[0] < self.xTestUnitVector) or (self.xTestUnitVector < centerPoint[0] < self.originX):
                                    circleCheck = ((self.xTestUnitVector - centerPoint[0])**2) + ((self.yTestUnitVector - centerPoint[1])**2)
                                    if circleCheck < 0.25:
                                        pointInFlag = True
                                    else:
                                        pointInFlag = False
                                else:
                                    pointInFlag = True
                            
                        if not objectHitAlready and self.distanceToObstruction < renderingDistance and pointInFlag:
                            if playerPerspectiveSlope != 0:
                                try: 
                                    rayIntersectSlope = (self.yTestUnitVector - self.originY)/(self.xTestUnitVector - self.originX)
                                    yRayOffset = self.originY - (rayIntersectSlope*self.originX)
                                    intersectedX = (yOffset - yRayOffset)/(rayIntersectSlope - objLineSlope)
                                except ZeroDivisionError:
                                    intersectedX = self.originX
                                
                                if self.xTestUnitVector - self.originX != 0:
                                    intersectedY = (rayIntersectSlope*intersectedX) + yRayOffset
                                try:
                                    percentageOfLine =  (intersectedX - circleObjXIntersect1)/(circleObjXIntersect2 - circleObjXIntersect1)
                                except ZeroDivisionError:
                                    percentageOfLine = (intersectedY - circleObjYIntersect1)/(circleObjYIntersect2 - circleObjYIntersect1)
                            
                            elif playerPerspectiveSlope == 0:
                                rayIntersectSlope = (self.yTestUnitVector - self.originY)/(self.xTestUnitVector - self.originX)
                                yRayOffset = self.originY - (rayIntersectSlope*self.originX)
                                yIntersected = (rayIntersectSlope*centerPoint[0]) + yRayOffset
                                if int(centerPoint[1]) <= yIntersected <= (int(centerPoint[1])+1):
                                    percentageOfLine =  yIntersected % 1
                                else:
                                    percentageOfLine = 0
                            
                            pointData = [gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)], self.distanceToObstruction, percentageOfLine]
                            if gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] == 'H':
                                pointData.append((int(self.xTestUnitVector),int(self.yTestUnitVector)))
                            self.objectsHit.append(pointData)
                    else:
                        self.obstructionHit =  True
            else:
                self.obstructionHit = True
                self.distanceToObstruction = renderingDistance

        if self.distanceToObstruction >= renderingDistance:
            self.distanceToObstruction += 1
        else:
            self.obstructionChar = gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)]
