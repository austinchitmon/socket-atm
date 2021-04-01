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

# CONNECTION SETUP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def listen_for_server_response():
    data = s.recv(BUFFER_SIZE)
    return data.decode()

def handle_response(response):
    print(response)

def print_invalid_option_selection():
    print('ERROR: Please enter a number 1-4\n')

def validate_float_or_int(number):
    try:
        float(number)
        return True
    except ValueError:
        return validate_int(number)


def validate_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def option_selected_is_invalid(number):
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
    if validate_float_or_int(withdrawAmt):
        send_message(WITHDRAW_MSG + withdrawAmt)
        # wait for response from server
        responseMsg = listen_for_server_response()
        handle_response(responseMsg)
    else:
        print('Please enter a valid numerical amount to withdraw')

def deposit():
    send_message(DEPOSIT_MSG)


def view_balance():
    send_message(VIEW_MSG)

def close():
    print('Closing ATM...')
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
