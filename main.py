from TypingSpeed import *
from DatabaseManagement import *
from Utils import *
from datetime import datetime


start_art = """
        ████████╗██╗   ██╗██████╗ ██╗███╗   ██╗ ██████╗     ███████╗██████╗ ███████╗███████╗██████╗ 
        ╚══██╔══╝╚██╗ ██╔╝██╔══██╗██║████╗  ██║██╔════╝     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗
           ██║    ╚████╔╝ ██████╔╝██║██╔██╗ ██║██║  ███╗    ███████╗██████╔╝█████╗  █████╗  ██║  ██║
           ██║     ╚██╔╝  ██╔═══╝ ██║██║╚██╗██║██║   ██║    ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║
           ██║      ██║   ██║     ██║██║ ╚████║╚██████╔╝    ███████║██║     ███████╗███████╗██████╔╝
           ╚═╝      ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝ 
                                                                                    """




def TypingSpeed(username, hard=False):
    """Main TypingSpeed function. includes all front-end logic"""

    string = get_words(hard=hard)
    _string = "\u200e ".join(string)  # get string to be displayed, added zero width char to prevent cheating

    print("Words:\n    " + _string)

    # timer(3)
    sleep(0.75)

    start_time = datetime.now()
    user_input = input(" —> ")
    end_time = datetime.now()
    timetaken = round((end_time - start_time).total_seconds(), 1)  # calc timetaken and round off

    if "\u200e " in user_input:  # anti-cheat
        print("Nice Try but you can't do that here")
        return

    netWPM = net_wpm(user_input, _string, timetaken)
    grossWPM = gross_wpm(user_input, timetaken)
    Accuracy, errors = accuracy(user_input, _string)

    # Print results

    results = f"""
    Net WPM: {netWPM}     Accuracy: {Accuracy}%    Gross WPM: {grossWPM}
    Time Taken: {timetaken}     Errors: {errors}
    """

    data = {'String': ' '.join(string), 'userInput': user_input, 'timeTaken': timetaken, 'netWPM': netWPM,
            'grossWPM': grossWPM, 'Accuracy': Accuracy, 'Error': errors}  # Data to be sent to update_user_data()

    data = (' '.join(string), user_input, timetaken, netWPM, grossWPM, Accuracy, errors)

    update_user_data(username, data)
    print(results + "\n")


def login():
    """Login function for accounts, cross checks data with user_details table"""
    while True:
        clear()
        print(start_art+'By: Joe', end='\n\n\n')
        username = input("Username: ").strip().lower()  # gets username and removes any extra spaces
        user = get_user_details(username)

        if not user:
            print('User Does Not Exist\n')
            ch = input('Register New User(y/n): ').lower()
            if ch == 'n':
                continue

            elif ch == 'y':

                print('\n\n---------------------------------------------------------------------------------------------\n')

                name = input('Enter Name: ')
                age = int(input('Enter Age: '))
                password = input('Enter Password: ')

                print('\n---------------------------------------------------------------------------------------------\n')

                data = (name, age, username, password)
                create_user(data)

                timer(2, True)
                continue
            else:
                continue

        while True:
            passwd = input("Password: ")

            if user[2] == hash(passwd):
                clear()
                print(start_art + f'username: {username}', end='\n\n\n')
                print(f"\nWelcome {user[3]} !")
                return user

            else:
                print('incorrect password\n')

                continue

        break


if __name__ == '__main__':

    while True:
        user = login()
        username = user[1]

        # Menu-driven program
        while True:
            choice = input("    1.Play    2.View My Stats    3.Leaderboard    4.logout    99.Exit\n\t")
            clear()
            if choice.lower().split()[0] in ["p", 'play', '1']:
                print(start_art+f'username: {username}', end='\n\n\n')
                try:
                    param = bool(choice.lower().split()[1])
                    TypingSpeed(username, hard=param)
                except IndexError:
                    TypingSpeed(username)

            elif choice.lower() in ["r", 'records', 'view records', '2']:
                print(start_art+f'username: {username}', end='\n\n\n')
                view_records(username)

            elif choice.lower().split()[0] in ["l", 'leaderboard', '3']:
                print(start_art+f'username: {username}', end='\n\n\n')
                try:
                    param = choice.lower().split()[1]
                    view_leaderboard(param)
                except IndexError:
                    view_leaderboard()

            elif choice.lower() in ['logout', 'bye', '4']:
                break

            elif choice.lower() in ["e", 'exit', '99']:
                exit()

            else:
                print("Enter Valid Choice")


