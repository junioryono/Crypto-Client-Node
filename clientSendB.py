from socket import *
import os

def menuText():
    print('\n1) Enter new transaction')
    print('2) Current balance of each account')
    print('3) Print the unconfirmed transactions')
    print('4) Print the last X number of confirmed transactions')
    print('5) Print the blockchain')
    print('6) Quit\n')

def main():
    serverName = 'localhost'
    serverPort = 15004
    socketUDP = socket(AF_INET, SOCK_DGRAM)
    socketUDP.connect((serverName, serverPort))

    balance1 = 1000
    balance2 = 1000
    transactionFee = 2

    outsideLoop = True
    while outsideLoop:
        menuText()
        outsideOption = input('Input choice (1 - 6): ')

        if (outsideOption == '1'):
            print('\nWhich account do you want to send money from?')
            print('1) B0000001')
            print('2) B0000002')

            myAccountInputLoop = True
            while myAccountInputLoop:
                myAccountInput = input('Choice: ')
                if (myAccountInput == '1'):
                    myAccount = 'B0000001'
                    balance = balance1
                    myAccountInputLoop = False
                elif (myAccountInput == '2'):
                    myAccount = 'B0000002'
                    balance = balance2
                    myAccountInputLoop = False
                else:
                    print('Not a valid input. Please enter an integer between 1-2.')

            print('\nWhich account do you want to send money to?')
            print('1) A0000001')
            print('2) A0000002')

            receivingAccountInputLoop = True
            while receivingAccountInputLoop:
                receivingAccountInput = input('Choice: ')
                if (receivingAccountInput == '1'):
                    receivingAccount = 'A0000001'
                    receivingAccountInputLoop = False
                elif (receivingAccountInput == '2'):
                    receivingAccount = 'A0000002'
                    receivingAccountInputLoop = False
                else:
                    print('Not a valid input. Please enter an integer between 1-2.')

            amountInput = input('\nHow much do you want to send to this account? ')
            transactionAmount = int(amountInput)

            totalTransactionAmount = transactionAmount + transactionFee
            if (totalTransactionAmount > balance):
                print('\nYour current balance is ' + str(balance) + ' BTC.')
                print('You are trying to send ' + str(transactionAmount) + ' BTC with a ' + str(transactionFee) + ' BTC transaction fee.')
                print('Due to the total transaction amount being more than your account balance, the transaction has been canceled.')
            elif (totalTransactionAmount <= balance):
                print('\n' + myAccount + ' pays ' + receivingAccount + ' the amount of ' + str(transactionAmount) + ' BTC with a transaction fee of ' + str(transactionFee) + ' BTC.')
                print('Transaction total amount is ' + str(totalTransactionAmount) + ' BTC.\n')
                print('Do you want to continue with the transaction?')

                insideLoop = True
                while (insideLoop):
                    print('1) Continue')
                    print('2) Cancel\n')
                    insideOption = input('Input choice (1 - 2): ')

                    if (insideOption == '1'):
                        balance = balance - totalTransactionAmount
                        transactionBlock = myAccount + receivingAccount + hex(transactionAmount)

                        try:
                            unconfirmedTransactions = open('unconfirmed_T.txt', 'r')
                        except IOError:
                            with open('unconfirmed_T.txt', 'a') as unconfirmedTransactions:
                                unconfirmedTransactions.write('\n' + str(transactionBlock))
                        else:
                            with open('unconfirmed_T.txt', 'a') as unconfirmedTransactions:
                                unconfirmedTransactions.write('\n' + str(transactionBlock))

                        unconfirmedTransactions.close()
                        message = str.encode(str('C' + transactionBlock), 'utf-8')
                        socketUDP.send(message)

                        with open('balanceB.txt', 'w') as fileBalance:
                            fileBalance.write('B0000001:' + str(hex(balance1)) + '\n' + 'B0000002:' + str(hex(balance2)))

                        print('\nTransaction complete. New balance: ' + str(balance) + ' BTC')
                        insideLoop = False
                    elif (insideOption == '2'):
                        print('\nTransaction canceled.')
                        insideLoop = False
                    else:
                        print('\nNot a valid input. Please enter an integer between 1 and 2.')

        elif (outsideOption == '2'):
            try:
                accountBalances = open('balanceB.txt', 'r')
            except IOError:
                print('\nB0000001 Balance: 1000 BTC')
                print('B0000002 Balance: 1000 BTC')
            else:
                print('')
                for line in accountBalances.readlines():
                    accountName = line[0:8]
                    accountBalance = str(int(line[11:14], 16))
                    print(accountName + ' Balance: ' + accountBalance + ' BTC')

            accountBalances.close()

        elif (outsideOption == '3'):
            try:
                unconfirmedTransactions = open('unconfirmed_T.txt', 'r')
            except IOError:
                print('\nNo transactions have been made yet.\n')
            else:
                printUnconfirmedTransactions = unconfirmedTransactions.read()
                print('\nUnconfirmed transactions:\n')
                print(printUnconfirmedTransactions)

            unconfirmedTransactions.close()

        elif (outsideOption == '4'):
            print('\nNo transactions have been confirmed yet.')

        elif (outsideOption == '5'):
            print('\nNo blocks in blockchain yet.')

        elif (outsideOption == '6'):
            print('Program has been quit.\n')
            outsideLoop = False

        else:
            print('Not a valid input. Please enter an integer between 1-6.')

    socketUDP.close()

main()