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

    def start(self, image):
        self.originalImage = image
        image = image[240:870, 450:1300]
        self.screenshot = image
        time.sleep(0.1)
        return message
