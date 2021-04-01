import socket

# CONSTANTS
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
WITHDRAW_MSG = 'withdraw_'
DEPOSIT_MSG = 'deposit_'
VIEW_MSG = 'view'
BALANCE = 1000


# CONNECTION SETUP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Listening for client...')
conn, addr = s.accept()



def send_response(responseMsg):
    conn.send(responseMsg.encode())

def handle_message(message):
    if message == WITHDRAW_MSG:
        send_response('withdrawing...')
    elif message == DEPOSIT_MSG:
        send_response('depositing...')
    elif message == VIEW_MSG:
        send_response('viewing...')

def on_connection_established():
    print('Connection established with ', addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print('received:', data.decode())
        handle_message(data.decode())




if __name__ == '__main__':
    on_connection_established()