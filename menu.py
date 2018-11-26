"""
Main Menu
"""
import os
from framework import Window, Text, Keys, Clock, Events
from inputManager import InputManager
import time

window = Window(544, 600).setTitle('Donkey Kong').setIcon('assets/icon.png')

class MenuOption:
    def __init__(self, text, func, fontSize=30):
        self.Label = text
        self.Callback = func
        self.__selected = False
        self.__fontSize = fontSize

    def onFocus(self):
        self.__selected = True

    def onBlur(self):
        self.__selected = False

    @property
    def isSelected(self):
        return self.__selected

    @property
    def image(self):
        text = Text(self.Label, fontSize=self.__fontSize)
        text.setBold()
        if self.isSelected and self.Callback is not None:
            text.setColor((255, 0, 0))

        return text.image


"""
The menu builder class is used for quickly rendering menus
"""
class MenuBuilder:
    def __init__(self):
        self.__options = []
        self.__selectedIndex = 0

    def addOption(self, label, func):
        """ Adds an option to the menu """
        self.__options.append(MenuOption(label, func))

        return self

    def addLabel(self, label):
        """ Adds an option without a callback func """
        self.__options.append(MenuOption(label, None))
        return self

    def show(self, win):
        """ Shows the menu """
        self._open = True
        self.__window = win

        self.__options[self.__selectedIndex].onFocus()

        self.__subscribe()

        while self._open:
            Clock.forceFPS(20)
            Events.handleEvents()
            InputManager.handleInput()
            self.__draw()

        self.__unsubscribe()

        return self

    def __draw(self):
        self.__window.fill((1, 1, 1)) # Background color
        i = 1
        width = self.__window.width

        for option in self.__options:
            x = (width - option.image.get_width())/2 # Puts label in the center
            self.__window.draw(option, x, 100 + 60*i)
            i = i + 1

        self.__window.flip()


    def __handleKeyPress(self, key):
        if key == Keys.UP:
            self.__findNextOptionWithCallback(-1)

        elif key == Keys.DOWN:
            self.__findNextOptionWithCallback(1)

        elif key == Keys.ENTER:
            option = self.__options[self.__selectedIndex]
            if option.Callback is not None:
                self.__unsubscribe()
                option.Callback(self.__window)
                self.__subscribe()
            #self._open = False

    def __findNextOptionWithCallback(self, increment):
        max = len(self.__options) - 1

        self.__options[self.__selectedIndex].onBlur()

        searching = True
        index = self.__selectedIndex
        while searching:
            index = index + increment
            if index > max:
                index = self.__selectedIndex
                searching = False

            if index < 0:
                index = self.__selectedIndex
                searching = False

            if self.__options[index].Callback is not None:
                searching = False

        self.__selectedIndex = index
        self.__options[self.__selectedIndex].onFocus()


    def __subscribe(self):
        InputManager.subscribe(
            [Keys.UP, Keys.DOWN, Keys.ENTER],
            self.__handleKeyPress
        )

    def __unsubscribe(self):
        InputManager.unsubscribe(
            [Keys.UP, Keys.DOWN, Keys.ENTER],
            self.__handleKeyPress
        )

def play(window):
    print("play")

def controls(window):
    print("controls")

def credits(window):
    menu = MenuBuilder()
    menu.addLabel("Michael Rouse")
    menu.show(window)
    print("credits")

def exit(data):
    window.close()
    os._exit(0)


def showMainMenu():
    """ Creates the main menu """
    Events.subscribe(Events.QUIT, exit)

    menu = MenuBuilder()
    menu.addOption("Play", play)
    menu.addOption("Controls", controls)
    menu.addOption("Credits", credits)
    menu.addOption("Exit", exit)

    menu.show(window)