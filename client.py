import socket

# CONSTANTS
running = True
OPTION_MESSAGE = "\nEnter the number of your desired ATM Operation:\n" \
                 "1.\tWithdraw from my bank account\n" \
                 "2.\tDeposit into my bank account\n" \
                 "3.\tView my balance\n" \
                 "4.\tClose ATM\n" \
                 "Input: "
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
WITHDRAW_MSG = 'withdraw_'
DEPOSIT_MSG = 'deposit_'
VIEW_MSG = 'view'
CLOSE_MSG = 'close'

# CONNECTION SETUP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


def listen_for_server_response():
    data = s.recv(BUFFER_SIZE)
    return data.decode()


def handle_response(response):
    print('\n%s' % response)


def print_invalid_option_selection():
    print('\nERROR: Please enter a number 1-4')


def print_invalid_monetary_amount():
    print('\nERROR: Please enter a positive whole dollar amount')


def validate_positive_float_or_int(number):
    try:
        # check if int
        if int(number):
            # means number entered is an int
            number = int(number)
            # check it is greater than 0
            if number > 0:
                return True
            else:
                # less than 0 int, throw error
                print_invalid_monetary_amount()
                return False
    except ValueError:
        print_invalid_monetary_amount()
        return False


def validate_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


def option_selected_is_invalid(number):
    # must be int inclusively between 1 and 4
    if validate_int(number) and 1 <= int(number) <= 4:
        return False
    else:
        print_invalid_option_selection()
        return True


def send_message(message):
    bytes = message.encode()
    s.send(bytes)


def withdraw():
    withdrawAmt = input('Enter an amount to withdraw: $')
    if validate_positive_float_or_int(withdrawAmt):
        send_message(WITHDRAW_MSG + withdrawAmt)
        # wait for response from server
        responseMsg = listen_for_server_response()
        handle_response(responseMsg)
    else:
        print('Please try again.')


def deposit():
    depositAmt = input('Enter an amount to deposit: $')
    if validate_positive_float_or_int(depositAmt):
        send_message(DEPOSIT_MSG + depositAmt)
        # wait for response from server
        responseMessage = listen_for_server_response()
        handle_response(responseMessage)
    else:
        print('Please try again.')


def view_balance():
    send_message(VIEW_MSG)
    # wait for response from server
    responseMsg = listen_for_server_response()
    handle_response(responseMsg)


def close():
    print('Closing ATM...')
    send_message(CLOSE_MSG)
    exit()


def option_selector(number):
    if number == 1:
        withdraw()
    elif number == 2:
        deposit()
    elif number == 3:
        view_balance()
    elif number == 4:
        close()


def main_loop():
    while running:
        inputNumber = input(OPTION_MESSAGE)
        if option_selected_is_invalid(inputNumber):
            continue
        else:
            inputNumber = int(inputNumber)
            # option_selector sends a message to the server to do the defined operation based on the number
            option_selector(inputNumber)


if __name__ == '__main__':
    main_loop()
