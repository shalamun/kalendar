import sys, os, datetime, calendar, sqlite3

def main(argv1=None):

    connection = sqlite3.connect('kalendar_database.db')
    cursor = connection.cursor()
    # creates the Notes table if it does not exist yet
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notes (
        start_date INTEGER,
        end_date INTEGER,
        content TEXT)
    ''')
    connection.commit()
    
    global current_date
    global current_date_format
    current_date = datetime.datetime.now()
    current_date_format = current_date.toordinal()

    def clear():
        # clears the terminal
        # should work for both win and linux
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_current_calendar():
        # prints out the calendar for the current month
        print(calendar.month(int(current_date.strftime('%Y')),int(current_date.strftime('%m'))))

    def menu():
        connection.commit() # saves all of the changes made
        clear()
        print('1: New note')
        print('2: Read notes')
        print('3: Sort and clean notes')
        print('4: Open data file')
        print('5: Exit')
        choice = str(input())
        if choice == '1':
            new_note()
        elif choice == '2':
            read_notes()
        elif choice == '3':
            clear()
            sort_notes()
            delete_old_notes()
        elif choice == '4':
            direct_open_file()
        elif choice == '5':
            sys.exit(0)
        else:
            print('Invalid menu selection.')
            input('Input anything to return to menu: ')
        menu()

    def new_note():
        clear()
        note = str(input('Input the text of a new note: '))
        clear()
        print_current_calendar()
        print(note)
        try:
                print('Start date:')
                date_year = (input('Input year (leave  blank for current year): '))
                if date_year == '':
                    date_year = int(current_date.strftime('%Y'))
                else:
                    date_year = int(date_year)
                date_month = (input('Input month (leave blank for current month): '))
                if date_month == '':
                    date_month = int(current_date.strftime('%m'))
                else:
                    date_month = int(date_month)
                date_day = int(input('Input day: '))
                start_date = datetime.date(date_year,date_month,date_day)
                start_date = int(start_date.toordinal())
        except ValueError: # returns to menu when the date input is invalid
            print('Invalid date input!')
            input('Input anything to return to menu: ')
            menu()
        # asks the user if end date is required as well
        if (input('Input end date as well? [y/N]')) in ('y', 'Y'):
            try:
                print('End date:')
                date_year = (input('Input year (leave  blank for current year): '))
                if date_year == '':
                    date_year = int(current_date.strftime('%Y'))
                else:
                    date_year = int(date_year)
                date_month = (input('Input month (leave blank for current month): '))
                if date_month == '':
                    date_month = int(current_date.strftime('%m'))
                else:
                    date_month = int(date_month)
                date_day = int(input('Input day: '))
                end_date = datetime.date(date_year,date_month,date_day)
                end_date = int(end_date.toordinal())
            except ValueError: # returns to menu when the date input is invalid
                print('Invalid date input!')
                input('Input anything to return to menu: ')
                menu()
        else: 
            end_date = 0    # sets the end date to 0 if none is given
        to_insert =  ''' 
        INSERT INTO Notes (start_date, end_date, content)
        VALUES (?, ?, ?);
        '''
        cursor.execute(to_insert, (start_date, end_date, note))
    
    menu()
    
if __name__ == '__main__':
    if len(sys.argv) != 1:
        if sys.argv[1] == ('-r' or '-R'):
            main(argv1='read_on_startup')
    else:
        main()
