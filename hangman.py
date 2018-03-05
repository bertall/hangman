import random
import os
import web3
from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
import time


gasLimit = 4000000

HANGMANPICS = [
'''
  +---+
  |   |
      |
      |
      |
      |
=========''', 
'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', 
'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', 
'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', 
'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', 
'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', 
'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

WordsDict = {
'Countries':[word.strip('\n') for word in open("countries.txt", 'r').readlines()], 
'Cities':[word.strip('\n') for word in open("cities.txt", 'r').readlines()], 
'Animals':[word.strip('\n') for word in open("animals.txt", 'r').readlines()]}

Categories = ['', 'Countries', 'Cities', 'Animals']

def encodeWords(category):
    category_int = []
    for word in category:
        category_int.append([ord(char) - 96 for char in word])
    return category_int

def Welcomenote():
    print('Выберите категорию')
    print(' 1: ' + Categories[1])
    print(' 2: ' + Categories[2])
    print(' 3: ' + Categories[3])
    print(' Another: Random word from the above 3 categories') 

    choose = input()
    if int(choose) > 3:
        return random.randint(1, 3)
    return int(choose)

def displayBoard(HANGMANPICS, missedLetters, category, blanks):
    print('Selected category: ' + category)
    
    print(HANGMANPICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    for letter in blanks:
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def checkCorrectAnswer(blanks):
    foundAllLetters = True
    for i in range(len(blanks)):
        if blanks[i] == '_':
            foundAllLetters = False
            break
    return foundAllLetters

def checkWrongAnswer(missedLetters):
    if len(missedLetters) == len(HANGMANPICS) - 1:
        return True
    return False
            
def main():
    print('Loading...')

    contract_source_code = open("hangmanContract.sol", 'r').read()

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:Hangman']
    http_provider = HTTPProvider('http://localhost:8545')
    w3 = Web3(http_provider)

    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': gasLimit})

    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']

    contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

    for i, categ in enumerate(WordsDict):
        catWords = encodeWords(WordsDict[categ])
        for word in catWords:
            contract_instance.addCategory(i+1, word, transact={'from': w3.eth.accounts[0]})

    os.system('clear')
    print('HANGMAN')
    choosenCategory = Welcomenote()
    missedLetters = ''
    correctLetters = ''
    gameSucceeded = False
    gameFailed = False
    secretWord = ''
    contract_instance.setWordLen(choosenCategory, transact={'from': w3.eth.accounts[0]})
    secretWordLen = contract_instance.getWordLen()
    blanks = ['_' for i in range(secretWordLen)]
    os.system('clear')
    while True:
        displayBoard(HANGMANPICS, missedLetters, Categories[choosenCategory], blanks)

        if gameSucceeded or gameFailed:
            secretWord = contract_instance.getWord()
            if gameSucceeded:
                print('Yes! The secret word is "' + ''.join(map(str, [chr(i+96) for i in secretWord])) + '"! You have won!')
            else:
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) +
                 ' missed guesses and ' + str(len(correctLetters)) +
                  ' correct guesses, the word was "' + ''.join(map(str, [chr(i+96) for i in secretWord])) + '"')

            if playAgain():
                os.system('clear')
                choosenCategory = Welcomenote()
                missedLetters = ''
                correctLetters = ''
                gameSucceeded = False
                gameFailed = False
                contract_instance.setWordLen(choosenCategory, transact={'from': w3.eth.accounts[0]})
                secretWordLen = contract_instance.getWordLen()
                blanks = ['_' for i in range(secretWordLen)]
                os.system('clear')
                continue 
            else: 
                break

        guess = getGuess(missedLetters + correctLetters)
        correct = contract_instance.check(ord(guess) - 96)
        if correct:
            correctLetters = correctLetters + guess
            for pos in correct:
                blanks[int(pos)] = guess
            gameSucceeded = checkCorrectAnswer(blanks)
        else:
            missedLetters = missedLetters + guess
            gameFailed = checkWrongAnswer(missedLetters)
        os.system('clear')

if __name__ == "__main__":
    main()
