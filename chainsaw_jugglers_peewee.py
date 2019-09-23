import sqlite3
from peewee import *
import jugglers_class

# Assign database
db = SqliteDatabase('chainsaw_jugglers_peewee_db.sqlite')

# define the main method 
def main():
    createDataBase()
    print('This program manages a database of chainsaw juggling record holders')
    print('Enter the number of the option you want to choose.\n')
    # This loop will continue until the user enters 6 to exit the progam
    while True:
        # print user options
        menu()

        # The program will test that the user's input is one of the 6 options by comparing it to the list of choices  
        while True:
            try:
                choices = [1, 2, 3, 4, 5, 6]
                user_choice = int(input(': '))
                if user_choice in choices:
                    break
            except:
                pass
            print('A number 1-6 must be selected.')

        if user_choice == 1:
            showCurrentRecordHolders()

        if user_choice == 2:
            addNewRecordHolder()

        if user_choice == 3:
            searchForRecordHolderByName()

        if user_choice == 4:
            updateNumberOfCatchesForRecordHolder()

        if user_choice == 5:
            deleteRecordHolderByName()

        if user_choice == 6:
            break

def createDataBase():
    # Create the database connection to a db file
    db.connect()
    tables = db.get_tables()
    if len(tables) == 0:
        db.create_tables([jugglers_class.Juggler])

        # Add data to the db
        janne = jugglers_class.Juggler(name='Janne Mustonen', country='Finland', numberOfCatches=98)
        janne.save()
        ian = jugglers_class.Juggler(name='Ian Stewart', country='Canada', numberOfCatches=94)
        ian.save()
        aaron = jugglers_class.Juggler(name='Aaron Gregg', country='Canada', numberOfCatches=88)
        aaron.save()
        chad = jugglers_class.Juggler(name='Chad Taylor', country='USA', numberOfCatches=78)
        chad.save()

    db.close()

# Menu method will print all the progam options
def menu():
    print('1. Show current chainsaw juggling record holders')
    print('2. Add a new record holder')
    print('3. Search for a record holder by name')
    print('4. Update the number of catches for a record holder')
    print('5. Delete a record holder by name')
    print('6. Exit program')

def showCurrentRecordHolders():
    db.connect()
    jugglers = jugglers_class.Juggler.select()
    for juggler in jugglers:
        print(juggler)
    print()
    db.close()

def addNewRecordHolder():
    print()
    db.connect()
    # Get the name, country, and number of catches in order to add a new record
    name = input('Enter the new record holder\'s name: ')
    country = input('Enter the new record holder\'s country: ')
    # loop to make sure the number of catches is a positive integer number
    while True:
        try:
            catches = int(input('Enter the new record holder\'s number of catches: '))
            if catches > 0:
                break
            else:
                print('Number of catches must be a positive integer.')
        except:
            pass
        print('Number of catches must be an integer')

    new_juggler = jugglers_class.Juggler(name=name, country=country, numberOfCatches=catches)
    new_juggler.save()
    db.close()
    print()

def searchForRecordHolderByName():
    print()
    db.connect()
    # Get the name the user wants to search
    name = input('Enter the name of the juggler you want to locate: ')
    jugglers = jugglers_class.Juggler.select().where(jugglers_class.Juggler.name == name)
    for juggler in jugglers:
        print(juggler)
    print()
    db.close()

def updateNumberOfCatchesForRecordHolder():
    print()
    db.connect()
    # Get the name of the record holder the user wants to update
    name = input('Enter the name of the juggler you want to update: ')

    while True:
        try:
            catches = int(input('Enter the updated number of catches: '))
            if catches > 0:
                break
            else:
                print('Number of catches must be a positive integer.')
        except:
            pass
        print('Number of catches must be an integer')

    rows_changed = jugglers_class.Juggler.update(numberOfCatches=catches).where(jugglers_class.Juggler.name == name).execute()
    print(rows_changed)
    print()
    db.close()

def deleteRecordHolderByName():
    print()
    db.connect()
    # Get the name of the record holder the user wants to delete
    name = input('Enter the name of the juggler you want to delete: ')

    rows_deleted = jugglers_class.Juggler.delete().where(jugglers_class.Juggler.name == name).execute()
    print(rows_deleted)
    db.close()

main()