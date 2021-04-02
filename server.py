#   Student:    Austin Chitmon
#   ID:         010754712


import socket

# CONSTANTS
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
WITHDRAW_MSG = 'withdraw'
DEPOSIT_MSG = 'deposit'
VIEW_MSG = 'view'
CLOSE_MSG = 'close'
KILL_MSG = 'kill'
BALANCE = 100.00
s = None
conn = None
addr = None

def first_time_setup():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))

def listen_for_client():
    global s
    global conn
    global addr
    s.listen(1)
    print('Listening for client...')
    conn, addr = s.accept()



def send_response(responseMsg):
    conn.send(responseMsg.encode())


def parse_message(message):
    return message.split('_')


def able_to_withdraw(amount):
    global BALANCE
    print('LOG: Doing withdraw check with $%.2f - $%.2f' % (BALANCE, amount))
    val = BALANCE >= amount
    print('LOG: Able to withdraw?: %r' % val)
    return val


def do_withdraw(amount):
    global BALANCE
    BALANCE = BALANCE - amount


def withdraw_container(amount):
    global BALANCE
    amount = float(amount)
    if able_to_withdraw(amount):
        do_withdraw(amount)
        print('LOG: New balance: $%.2f' % BALANCE)
        send_response('Successfully withdrew $%.2f' % amount)
    else:
        print('LOG: Invalid balance to withdraw')
        send_response('ERROR: Not enough balance to withdraw.')


def do_deposit(amount):
    global BALANCE
    print('LOG: Doing deposit: $%.2f + $%.2f' % (BALANCE, amount))
    BALANCE = BALANCE + amount
    print('LOG: New balance after deposit: $%.2f' % BALANCE)


def deposit_container(amount):
    global BALANCE
    amount = float(amount)
    do_deposit(amount)
    send_response('Successfully deposited $%.2f' % amount)


def view_balance_container():
    global BALANCE
    print('LOG: Current Balance: $%.2f' % BALANCE)
    send_response('Current Balance: $%.2f' % BALANCE)


def handle_message(message):
    messageList = parse_message(message)
    if messageList[0] == WITHDRAW_MSG:
        withdraw_container(messageList[1])
    elif messageList[0] == DEPOSIT_MSG:
        deposit_container(messageList[1])
    elif messageList[0] == VIEW_MSG:
        view_balance_container()
    elif messageList[0] == CLOSE_MSG:
        print('LOG: Current connection closed by client.')
    elif messageList[0] == KILL_MSG:
        print('TERMINATE: Server terminated by client.')
        exit()


def on_connection_established():
    print('Connection established with ', addr)
    # while connection open, listen for data
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print('--RECEIVED:', data.decode())
        handle_message(data.decode())
        print('--OPERATION COMPLETE')


if __name__ == '__main__':
    first_time_setup()
    while True:
        listen_for_client()
        on_connection_established()
