import tkinter as tk
import random


class WordleGUI:
    def __init__(self):
        self.rootWin = tk.Tk()
        self.rootWin.title('Sqwordle')
        self.rootWin.config(bg='#121213')

        self.greenCol = '#538d4e'
        self.yellowCol = "#b59f3b"
        self.greyCol = '#3a3a3c'
        self.resetCol = '#818384'

        self.userGuess = ''
        self.guessNum = 0
        self.qwertyList = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        self.buttonList = []
        self.labelList = []
        self.wordleList = []
        self.wordList()
        self.wordleWord = self.wordList()[random.randint(0, 8257)]

        self.createButtons()
        self.createWidgets()

        self.rootWin.bind_all('<Escape>', self.quitEsc)
        self.rootWin.bind_all("<Return>", self.checkWordE)
        self.rootWin.bind_all("<Tab>", self.checkWordE)
        self.rootWin.bind_all("<BackSpace>", self.backspaceKey)  # make happen once

    def createLetters(self):
        """This makes the keyboard buttons in a list"""
        for row in range(len(self.qwertyList)):
            for column in range(len(self.qwertyList[row])):
                self.buttonList.append(tk.Button(self.rootWin,
                                                 text=self.qwertyList[row][column],
                                                 justify=tk.CENTER,
                                                 command=lambda t=(row, column): self.keyPress(t),
                                                 bg='#818384'))
                self.buttonList[-1].grid(row=row + 8, column=column)

    def createButtons(self):
        """the user interface keyboard buttons and quit/print/delete buttons"""
        self.createLetters()
        self.quitButton = tk.Button(self.rootWin,
                                    text='Quit',
                                    command=quit,
                                    bg='#818384')
        self.enterButton = tk.Button(self.rootWin,
                                     text='Enter',
                                     command=self.checkWord,
                                     bg='#818384')
        self.enterButton.grid(row=0, column=11)
        self.quitButton.grid(row=0, column=10)

    def createWidgets(self):
        """the 30 labels for the 6 guesses, created in a list and initialized to the grid"""
        for row in range(6):
            for column in range(5):
                self.labelList.append(tk.Button(self.rootWin,
                                                width=1,
                                                justify=tk.CENTER,
                                                bg='#818384'))
                self.labelList[-1].grid(row=row, column=column + 3)
        self.typeLabel = tk.Label(self.rootWin,
                                  justify=tk.CENTER,
                                  width=6,
                                  text='Type ^',
                                  bg=self.resetCol)
        # the entry panel for the guesses
        self.entry = tk.Entry(self.rootWin,
                              justify=tk.CENTER,
                              width=7,
                              bg=self.resetCol)
        # the initialization of all the labels
        self.entry.grid(row=7, column=10)
        self.typeLabel.grid(row=8, column=10)

    def keyPress(self, location):
        """This is triggered whenever a button from the onscreen keyboard is pressed, it prints the letter pressed
        and then adds the letter to the string of the user guess, clears the entry box, and puts the user guess
        string including the new letter inside of it """
        print(self.qwertyList[location[0]][location[1]])
        entry = self.entry.get()  # entry is temp variable w/ the contents of the entry
        entry += self.qwertyList[location[0]][location[1]]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, entry)

    def backspaceKey(self, event):
        """This is if the user is not clicked into the entry box they can still hit backspace to delete a letter"""
        # entry = self.entry.get()
        # entry = entry[0: -1]  # this is the user guess string minus the last letter
        # self.entry.delete(0, tk.END)
        # self.entry.insert(0, entry)

    def checkWordE(self, event):
        """This is an intermediary for if the user hits the enter button - because that generates an event the regular
        'checkWord' function cannot handle it, so we had to make this"""
        self.checkWord()

    def wordList(self):
        """ This takes the text file and makes it into a list of words with \n stripped"""
        wordleFile = open('wordlewords.txt', 'r')
        for line in wordleFile:
            line = line.strip()
            line = line.strip('\n')
            self.wordleList.append(line)
        return self.wordleList

    def keyColChange(self, ch, color):
        """Changes the color of the keyboard buttons to green/yellow/grey based on the user's guess"""
        buttonIndex = 0
        for row in self.qwertyList:
            for column in row:
                if column == ch:
                    # this if is to make sure that we are not turning an already green key to yellow or grey
                    if self.buttonList[buttonIndex]['bg'] == self.greenCol:
                        return  # this ends the function, so it cannot change the bg color
                    # this is to make sure we are not turning an already yellow key to grey, it checks to see that
                    # the color we want to make the yellow key is not green and if it isn't green then it does
                    # nothing (so we can only go up the color ladder
                    elif self.buttonList[buttonIndex]['bg'] == self.yellowCol:
                        if color != self.greenCol:
                            return
                    else:  # this is to make sure we can only turn blank buttons grey - not green/yellow ones
                        if color == self.greyCol:
                            if self.buttonList[buttonIndex]['bg'] == self.resetCol:
                                self.buttonList[buttonIndex]['bg'] = color
                    self.buttonList[buttonIndex]['bg'] = color
                else:
                    buttonIndex += 1

    def checkWord(self):
        """ Takes a random word and then takes user input and checks (first for validity of user guess) to see the
            similarities between the two words, and returns the user the information!"""
        winner = False

        entryGuess = self.entry.get()
        self.userGuess = entryGuess.lower()
        self.entry.delete(0, tk.END)

        if self.guessNum == 6:
            self.guessNum = 0
            self.wordleWord = self.wordList()[random.randint(0, 8257)]
            for i in range(len(self.buttonList)):  # this is to reset the colors of the onscreen keyboard
                self.buttonList[i]['bg'] = self.resetCol
            for i in range(30):  # this is to reset the labels of previous guesses
                self.labelList[i]['bg'] = self.resetCol
                self.labelList[i]['text'] = ' '
            return

        # print(self.wordleWord)   # incase need to bug check uncomment this to know the secret word

        if self.userGuess not in self.wordList():
            print('Be sure to use a valid word bestie')
        else:
            wordColorList = [self.greenCol, self.greenCol, self.greenCol, self.greenCol, self.greenCol]
            if self.userGuess == self.wordleWord:
                self.labelFill = self.userGuess
                for ch in self.userGuess:
                    self.keyColChange(ch, self.greenCol)  # here
                print('Congratulations! You are the big winner!')
                winner = True
            else:
                userGuessList = []
                for ch in self.userGuess:
                    userGuessList.append(ch)
                correctWordList = []
                for ch in self.wordleWord:
                    correctWordList.append(ch)
                for i in range(5):
                    userGuessList[i] = self.userGuess[i]
                    wordColorList[i] = self.greyCol
                    self.keyColChange(userGuessList[i], self.greyCol)
                    if userGuessList[i] == self.wordleWord[i]:
                        userGuessList[i] = self.userGuess[i]
                        wordColorList[i] = self.greenCol
                        self.keyColChange(userGuessList[i], self.greenCol)
                        correctWordList.remove(self.userGuess[i])
                for i in range(5):
                    if self.userGuess[i] != self.wordleWord[i] and self.userGuess[i] in correctWordList:
                        userGuessList[i] = self.userGuess[i]
                        wordColorList[i] = self.yellowCol
                        self.keyColChange(userGuessList[i], self.yellowCol)
                        correctWordList.remove(self.userGuess[i])
                self.labelFill = "".join(userGuessList)
            for i in range(5):
                self.labelList[i + (self.guessNum * 5)]['text'] = str(self.labelFill)[i].upper()
                self.labelList[i + (self.guessNum * 5)]['bg'] = wordColorList[i]

            self.guessNum += 1

            if winner:
                self.guessNum = 6
            if self.guessNum == 6:
                if not winner:
                    print('You lose, dumbass')
                    print('The correct word was:', self.wordleWord)
                print('Hit enter to play again?')

    def quitEsc(self, event):
        """This quits the program and is called when the escape key is hit"""
        self.rootWin.destroy()

    def run(self):
        """This is how we run the GUI"""
        self.rootWin.mainloop()

    def quit(self):
        """Quits the program, and is called when escape is hit"""
        self.rootWin.destroy()


if __name__ == '__main__':
    myGUI = WordleGUI()
    myGUI.run()
