import sqlite3
# Global variable for the db file name
jugglers = 'chainsaw_jugglers_db.sqlite'

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
    conn = sqlite3.connect(jugglers)
    c = conn.cursor()

    # Test if the jugglers table is already in the db (Found example on sqlite3 website)
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='jugglers' ''')

    # If the jugglers tale is in the db ignore the execute line. If it is not than create the table
    if c.fetchone()[0]==1: 
        pass
    else:
        # Create a table
        conn.execute('create table jugglers (Name text, Country text, NumberOfCatches integer)')

        # Add the base data
        conn.execute('insert into jugglers values ("Janne Mustonen", "Finland", 98)')
        conn.execute('insert into jugglers values ("Ian Stewart", "Canada", 94)')
        conn.execute('insert into jugglers values ("Aaron Gregg", "Canada", 88)')
        conn.execute('insert into jugglers values ("Chad Taylor", "USA", 78)')

    # Commit the data
    conn.commit()

    # Close the db connection
    conn.close()

# Menu method will print all the progam options
def menu():
    print('1. Show current chainsaw juggling record holders')
    print('2. Add a new record holder')
    print('3. Search for a record holder by name')
    print('4. Update the number of catches for a record holder')
    print('5. Delete a record holder by name')
    print('6. Exit program')

def showCurrentRecordHolders():
    # open db file
    conn = sqlite3.connect(jugglers)
    # Upgrade row factory to access column name
    conn.row_factory = sqlite3.Row
    # Display all current record holders
    print()
    for row in conn.execute('SELECT * FROM jugglers'):
        print(row['Name'] + '\t' + row['Country'] + '\t' + str(row['NumberOfCatches']))

    print()
    conn.close()

def addNewRecordHolder():
    # open db file
    conn = sqlite3.connect(jugglers)
    print()
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
    # Add the record
    conn.execute('INSERT into jugglers values (?, ?, ?)', (name, country, catches))
    # Save the db
    conn.commit()
    conn.close()
    print(name + ' has been added to the database.\n')

def searchForRecordHolderByName():
    print()
    # Get the name the user wants to search
    name = input('Enter the name of the juggler you want to locate: ')
    # SQL syntax
    search_for_record_sql = 'SELECT * FROM jugglers WHERE Name = ?'
    # connect to the db
    conn = sqlite3.connect(jugglers)
    # row factory for printing
    conn.row_factory = sqlite3.Row
    # execute search
    row = conn.execute(search_for_record_sql, (name, ))
    # Find the first row with that matching name
    row_data = row.fetchone()
    conn.close()

    if row_data == 0:
        print('No juggler was located by the name: ' + name)
        print()
    else:
        print(row_data['Name'] + '\t' + row_data['Country'] + '\t' + str(row_data['NumberOfCatches']))
        print()

def updateNumberOfCatchesForRecordHolder():
    print()
    # Get the name of the record holder the user wants to update
    name = input('Enter the name of the juggler you want to update: ')
    update_syntax = 'UPDATE jugglers SET NumberOfCatches = ? WHERE Name = ?'

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

    with sqlite3.connect(jugglers) as conn:
        updated = conn.execute(update_syntax, (catches, name))
        updated_count = updated.rowcount
    conn.close()
    # If no rows were updated than the record holder was not found
    if updated_count == 0:
        print('This juggler was not located in the database.')
        print()
    # Print the name of the deleted person as confirmation
    else:
        print(name + '\'s catch count was updated.')
        print()

def deleteRecordHolderByName():
    print()
    # Get the name of the record holder the user wants to delete
    name = input('Enter the name of the juggler you want to delete: ')
    # SQL synax for deleting by name
    delete_from_jugglers_table_sql = 'DELETE FROM jugglers WHERE Name = ?'
    # Context manager with block will roll back if there are errors as to not mess up the db
    # delete the record holder
    with sqlite3.connect(jugglers) as conn:
        deleted = conn.execute(delete_from_jugglers_table_sql, (name, ))
        deleted_count = deleted.rowcount
    conn.close()
    # If no rows were deleted than the record holder was not found
    if deleted_count == 0:
        print('This juggler was not located in the database.')
        print()
    # Print the name of the deleted person as confirmation
    else:
        print(name + ' was deleted')
        print()

main()