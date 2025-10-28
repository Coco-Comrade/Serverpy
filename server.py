import socket
import logging
import random
from datetime import datetime
now = datetime.now()
SERVER_NAME = socket.gethostname()
QUEUE_LEN = 5
MAX_PACKET = 1024
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind(('0.0.0.0', 8820))
    server_socket.listen(QUEUE_LEN)
    logging.info('Listening on port 8820')
    while True:
        client_socket, client_address = server_socket.accept()
        logging.info('Accepted connection from {}'.format(client_address))

        try:
            while True:
                response = "Error unkown command given"
                request = client_socket.recv(MAX_PACKET).decode().strip()
                logging.info('Received {}'.format(request))
                if request == 'TIME':
                    response = datetime.now().strftime("%H:%M:%S")
                    logging.info('Sent local time')
                elif request == 'EXIT':
                    client_socket.close()
                    logging.info('Server exited')
                elif request == 'NAME':
                    response = ("Server name :"+SERVER_NAME)
                    logging.info('Sent server name')
                elif request == 'RAND':
                    response = f'Random number: {random.randint(1, 1000)}'
                    logging.info('Sent random number generator')
                elif request == "QUEUE":
                    response = "Queue :" + str(QUEUE_LEN)
                    logging.info('Sent queue length')
                client_socket.send(response.encode())
        except socket.error as err:
            logging.error('Socket error {}'.format(err))

except socket.error as err:
    logging.error('Socket error {}'.format(err))
finally:
    server_socket.close()
    logging.info('Closing server')
