import os

import mouse
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import numpy as np
import win32con
import cv2


class PylaStart:

    def __init__(self, state):
        self.clickCount = 0
        self.pickChampionCommandTries = 0
        self.progressState = 'find'
        self.originalImage = None
        # self.progressState = 'findNewGame'
        self.playBtn = cv2.imread('images/playBtn.JPG')
        self.confirmBtn = cv2.imread('images/confirmBtn.JPG')
        self.findMatchBtn = cv2.imread('images/findMatch.JPG')
        self.acceptBtn = cv2.imread('images/acceptBtn.JPG')
        self.lockInBtn = cv2.imread('images/lockIn.JPG')
        self.shopImage = cv2.imread('images/shop.JPG')

        self.xBtn = cv2.imread('images/xBtn.JPG')
        self.okBtn = cv2.imread('images/okBtn.JPG')
        self.arrowBtn = cv2.imread('images/arrowBtn.JPG')
        self.continueBtn = cv2.imread('images/continueBtn.JPG')
        self.playAgainBtn = cv2.imread('images/playAgainBtn.JPG')
        self.bigOkBtn = cv2.imread('images/bigOkBtn.JPG')
        self.championOptions = {
            'sona': cv2.imread('images/sona.JPG'),
            'twitch': cv2.imread('images/twitch.JPG'),
            'cait': cv2.imread('images/cait.JPG'),
            'miss': cv2.imread('images/cait.JPG'),
            'garen': cv2.imread('images/Garen.JPG'),
            'tryndamere': cv2.imread('images/tryndamere.JPG'),
            'yi': cv2.imread('images/masterYi.JPG'),
        }
        self.pickChampionTries = 0
        self.tryToFindChampionMaxCycles = 6
        self.championIndex = 0
        self.screenshot = None
        self.tries = 0
        self.bonusX = 570
        self.bonusY = 310
        self.champBonus = 60    

        self.startGameOptions = {
            'start': lambda: self.__look_for_template(self.screenshot, self.playBtn, 'confirm'),
            'confirm': lambda: self.__look_for_template(self.screenshot, self.confirmBtn, 'find'),
            'find': lambda: self.__look_for_template(self.screenshot, self.findMatchBtn, 'accept',
                                                     onSuccess='Pressed find match',
                                                     onError='Trying to locate find match'),
            'accept': lambda: self.__look_for_template(self.screenshot, self.acceptBtn, 'pickChampion',
                                                       onSuccess='Accepted match.',
                                                       onError='Waiting to accept to show up', threshold=0.5,
                                                       bonusX=self.bonusX - 50, bonusY=self.bonusY - 20),
            'pickChampion': lambda: self.pickChampion('Picked champion', 'Looking for champions to pick..'),
            'lockIn': lambda: self.__look_for_template(self.screenshot, self.lockInBtn, 'detectGameStart',
                                                       onSuccess='Locked in champion',
                                                       onError='Trying to lock in...',
                                                       bonusX=self.bonusX,
                                                       bonusY=self.bonusY),
            'end': lambda: print('Game detected lets play!'),  # This message doesn't matter it won't be used anywhere

        }

    def findImageInClient(self, image, template, threshold=0.65):
        img_rgb = image
        w, h = template.shape[:-1]

        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            return pt[0], pt[1]
        return False, False

    def __look_for_template(self, image, template, progressState=None, threshold=0.7, onSuccess=None, onError=None,
                            static=False,
                            bonusX=None, bonusY=None, dontClick=False, clickAway=False):
        if bonusX:
            bonusX = bonusX
            bonusY = bonusY
        else:
            bonusX = self.bonusX
            bonusY = self.bonusY  # Default readjusting
        x, y = self.findImageInClient(image, template)
        if x:
            time.sleep(0.3)
            if static:
                if not dontClick:
                    self.click(x + bonusX, y + bonusY, l=True)
                    if clickAway:
                        time.sleep(0.1)
                        self.click(400, 350)
                        time.sleep(3)
                return True
            self.click(x + bonusX, y + bonusY, l=True)
            self.progressState = progressState
            return onSuccess
        return onError    

    def detectGameStart(self):
        resultBoolean = self.__look_for_template(self.screenshot, self.shopImage, 'end', static=True, dontClick=True)
        dodgedGame = self.__look_for_template(self.screenshot, self.acceptBtn, progressState='pickChampion',
                                              onSuccess=True, onError=False),

        if dodgedGame is True:
            print("SOMEONE DODGED")
            self.progressState = 'pickChampion'
            return 'Someone dodged! Accepting again!'
        elif resultBoolean:
            self.progressState = 'end'
            return 'Game started!'
        return 'Waiting for game to start' 

    def refreshNewGameCommands(self):
        self.commands = [
            lambda image: self.__look_for_template(self.originalImage[170:700, 350:1600], self.xBtn, threshold=0.6,
                                                   static=True,
                                                   bonusX=370, bonusY=204),
            lambda image: self.__look_for_template(image, self.arrowBtn, threshold=0.6, static=True,
                                                   bonusX=self.bonusX - 50, bonusY=self.bonusY - 50),

            lambda image: self.__look_for_template(image, self.okBtn, threshold=0.6, static=True,
                                                   bonusX=self.bonusX - 50, bonusY=self.bonusY - 50),

            lambda image: self.__look_for_template(image, self.continueBtn, threshold=0.45, static=True,
                                                   bonusX=self.bonusX - 50, bonusY=self.bonusY - 0, clickAway=True),

            lambda image: self.__look_for_template(image, self.playAgainBtn, progressState='find',
                                                   onSuccess=True, onError=False,
                                                   threshold=0.6, bonusX=self.bonusX - 50, bonusY=self.bonusY - 50)]

    def findNewGame(self):
        """
        1. check for X and for -> in circle
        2. (optional) check for daily play
        3. Look for continue button
        4. Look for play again
        5. Stop play and go to start
        image, template, progressState=None, threshold=0.7, onSuccess=None, onError=None,
                            static=False
        """
        image = self.originalImage[170:990, 350:1600]

        index = 0
        # Any of the images can occur at any time but ONCE! So we will continue to look for each one.
        # If playAgainBtn is found the code will start from the find function
        self.__look_for_template(image, self.bigOkBtn, threshold=0.6, static=True, bonusX=self.bonusX - 140,
                                 bonusY=self.bonusY - 78),
        for command in self.commands:
            if command(image):
                self.commands.pop(index)
                if self.progressState == 'find':
                    break
                time.sleep(5)
            index += 1
        if len(self.commands) <= 2:
            self.tries += 1
            if self.tries == 8:
                self.progressState = 'find'

    def pickChampion(self, onSuccess, onError):
        champions = list(self.championOptions.keys())
        championKey = champions[self.championIndex]
        champion = self.championOptions[championKey]

        self.startGameOptions['accept']()
        if self.pickChampionTries > self.tryToFindChampionMaxCycles:
            self.championIndex += 1
            if len(champions) == self.championIndex:
                self.championIndex = 0
            self.pickChampionTries = 0

        # If someone dodges the game we will have to look for accept again
        x, y = self.findImageInClient(self.screenshot, champion)
        if x:
            self.pickChampionTries = 0
            self.championIndex = 0
            self.click(x + self.bonusX - self.champBonus, y + self.bonusY, l=True)
            self.progressState = 'lockIn'
            return onSuccess
        self.pickChampionTries += 1
        return onError

    @staticmethod
    def click(x, y, l=False, r=False):
        win32api.SetCursorPos((x, y))

        if l:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        if r:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        time.sleep(0.1)

    def start(self, image):
        self.originalImage = image
        image = image[240:870, 450:1300]
        self.screenshot = image
        time.sleep(0.1)
        return message
