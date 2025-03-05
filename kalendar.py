import sys, os, datetime, calendar

def main(argv1=None):
    global file_location
    global current_date
    global current_date_format
    current_date = datetime.datetime.now()
    current_date_format = current_date.toordinal()
    file_location = "XXXXXXXXXXXXXXXXX"

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
        #should work for both win and linux

    def print_current_calendar():
        print(calendar.month(int(current_date.strftime('%Y')),int(current_date.strftime('%m'))))

    def menu():
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
        if  ('|' in note) == True:
            print('Invalid input. The character \"|\" is reserved for the program.')
            input('Input anything to return to menu: ')
            menu()
        clear()
        print_current_calendar()
        print(note)
        try:
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
            date = datetime.date(date_year,date_month,date_day)
            date = str(date.toordinal())
        except ValueError:
            print('Invalid date input!')
            input('Input anything to return to menu: ')
            menu()
        write_to_file = date + '|' + note + '\n'
        file = open(file_location,'a')
        file.write(write_to_file)
        file.close()
        print('Note created!')
        input('Input anything to return to menu: ')

    def read_notes():
        clear()
        file = open(file_location,'r')
        file_content, reminders = [], []
        for line in file:
            file_content.append(line.strip())
        try:
            while file_content[0] == '':
                del file_content[0]
        except IndexError:
            pass
        if len(file_content) == 0:
            print('No notes found.')
            input('Input anything to return to menu: ')
            menu()
        print_current_calendar()
        for i in file_content:
            current_line = i.split('|')
            date_difference = int(current_line[0]) - int(current_date_format)
            if date_difference < 0:
                reminders.append(f'{abs(date_difference)} days ago:\n{current_line[1]}')
            elif date_difference == 0:
                reminders.append(f'Today:\n{current_line[1]}')
            elif date_difference <= 14:
                reminders.append(f'In {date_difference} days:\n{current_line[1]}')
        file.close()
        for i in reminders:
            print(i + '\n')
        input('Input anything to return to menu: ')

    def delete_old_notes():
        file = open(file_location,'r')
        file_content, to_keep = [], []
        for line in file:
            file_content.append(line.strip())
        try:
            while file_content[0] == '':
                del file_content[0]
        except IndexError:
            pass
        if len(file_content) == 0:
            print('No notes found.')
            input('Input anything to return to menu: ')
            menu()
        for i in file_content:
            current_line = i.split('|')
            date_difference = int(current_line[0]) - int(current_date_format)
            if date_difference >= 0:
                to_keep.append(f'{current_line[0]}|{current_line[1]}\n')
        to_keep = ''.join(to_keep)
        file.close()
        file = open(file_location,'w')
        file.write(to_keep)
        print('Old notes deleted!')
        input('Input anything to return to menu: ')

    def sort_notes():
        file = open(file_location,'r')
        file_content, to_keep, date_list, content_list = [], [], [], []
        for line in file:
            file_content.append(line.strip())
        try:
            while file_content[0] == '':
                del file_content[0]
        except IndexError:
            pass
        if len(file_content) == 0:
            print('No notes found.')
            input('Input anything to return to menu: ')
            menu()
        for i in file_content:
            current_line = i.split('|')
            date_list.append(int(current_line[0]))
            content_list.append(str(current_line[1]))
        date_list, content_list = (list(i) for i in zip(*sorted(zip(date_list, content_list))))
        for i in range(len(date_list)):
            to_keep.append(f'{date_list[i]}|{content_list[i]}\n')
        file.close()
        to_keep = ''.join(to_keep)
        file = open(file_location,'w')
        file.write(to_keep)
        file.close()
        print(to_keep)
        print('Notes sorted!')
    
    def direct_open_file():
        os.startfile(file_location)

    if argv1 == 'read_on_startup':
        read_notes()

    menu()

if __name__ == '__main__':
    if len(sys.argv) != 1:
        if sys.argv[1] == ('-r' or '-R'):
            main(argv1='read_on_startup')
    else:
        main()