"""
Main Menu
"""
import os
from framework import Window, Text, Keys, Clock, Events
from inputManager import InputManager
import time
from mario import Mario
from donkeyKong import DonkeyKong

class MenuResult:
    def __init__(self):
        self.players = []
        self.UseAI = False
        self.Difficulty = 0

result = MenuResult()

window = Window(544, 600).setTitle('Donkey Kong').setIcon('assets/icon.png')


def AIDifficultySelect(onPlay, difficulty):
    def wrapper(window):
        result.useAI = True
        result.Difficulty = difficulty
        onPlay(window, result)
    return wrapper

def showOnePlayerOptions(onPlay):
    def wrapper(window):
        menu = MenuBuilder()
        menu.addOption("Easy", AIDifficultySelect(onPlay, 10))
        menu.addOption("Medium", AIDifficultySelect(onPlay, 100))
        menu.addOption("Hard", AIDifficultySelect(onPlay, 600))
        menu.addExitOption("Back")
        menu.show(window)
    return wrapper

def savePlayerSelection(onPlay, nextFunc, selected, done=False):
    def wrapper(window):
        if selected.__name__ != DonkeyKong.__name__:
            result.players.append(result)

        if not done:
            return nextFunc(onPlay)(window)
        else:
            return onPlay(window, result)
    return wrapper

def showPlayerSelect(onPlay, nextFunc):
    def wrapper(window):
        menu = MenuBuilder()
        menu.addOption("Mario", savePlayerSelection(onPlay, nextFunc, Mario))
        menu.show(window)
    return wrapper

def showSecondPlayerSelection(onPlay):
    def wrapper(window):
        menu = MenuBuilder()
        menu.addOption("Donkey Kong", savePlayerSelection(onPlay, None, DonkeyKong, True))
        menu.show(window)
    return wrapper


def showPlayOptions(onPlay):
    def wrapper(window):
        menu = MenuBuilder()
        menu.addOption("1 Player", showPlayerSelect(onPlay, showOnePlayerOptions))
        menu.addOption("2 Players", showPlayerSelect(onPlay, showSecondPlayerSelection))
        menu.show(window)
    return wrapper


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


def show(onPlay):
    """ Creates the main menu """
    Events.subscribe(Events.QUIT, exit)

    menu = MenuBuilder()
    menu.addOption("Play", showPlayOptions(onPlay))
    menu.addOption("Controls", controls)
    menu.addOption("Credits", credits)
    menu.addExitOption('Exit')

    menu.show(window)








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
        self._open = False
        self._debounce = 30

    def addOption(self, label, func):
        """ Adds an option to the menu """
        self.__options.append(MenuOption(label, func))
        return self

    def addLabel(self, label):
        """ Adds an option without a callback func """
        self.__options.append(MenuOption(label, None))
        return self

    def addExitOption(self, label):
        self.__options.append(MenuOption(label, self.__close()))
        return self

    def show(self, win):
        """ Shows the menu """
        self._open = True
        self.__window = win

        self.__options[self.__selectedIndex].onFocus()

        self.__subscribe()

        while self._open:
            #Clock.forceFPS(10)
            Events.handleEvents()
            InputManager.handleInput()
            self.__draw()

            if self._debounce > 0:
                self._debounce = self._debounce - 1

        #self.__unsubscribe()

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
        if not self._open:
            return

        if self._debounce > 0:
            return

        if key == Keys.UP:
            self._debounce = 50
            self.__findNextOptionWithCallback(-1)

        elif key == Keys.DOWN:
            self._debounce = 50
            self.__findNextOptionWithCallback(1)

        elif key == Keys.ENTER and self._open == True:
            option = self.__options[self.__selectedIndex]
            if option.Callback is not None:
                ##self.__unsubscribe()
                self._open = False
                option.Callback(self.__window)
                self._open = True
                #del self
                #self.__subscribe()

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

    def __close(self):
        def wrapper(self2):
            self._open = False
        return wrapper

    def __subscribe(self):
        InputManager.subscribe(
            [Keys.UP, Keys.DOWN, Keys.ENTER],
            self.__handleKeyPress
        )

    def __unsubscribe(self):
        try:
            InputManager.unsubscribe(
                [Keys.UP, Keys.DOWN, Keys.ENTER],
                self.__handleKeyPress
            )
        except:
            pass
