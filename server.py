from socket import *
import os

# SERVER_HOME_DIRECTORY = os.path.join(os.path.expanduser('~'), raw_input('Please enter your server home directory: '))

SERVER_HOME_DIRECTORY = os.path.join(os.path.expanduser('~'), os.path.join(os.getcwd(), 'files'))

server_s = socket(AF_INET, SOCK_STREAM)

server_s.bind(('0.0.0.0', 80))

server_s.listen(5)
print 'Listening to port 80...'
while True:
    (client_s, client_addr) = server_s.accept()
    print 'New connection was created'
    a = client_s.recv(1000).split(' ')
    if a[0] == 'GET':
        a[1] = a[1]
        file_path = SERVER_HOME_DIRECTORY + a[1]
        print 'GET REQUEST FOR {}'.format(file_path)
        is_file = os.path.isfile(SERVER_HOME_DIRECTORY + a[1])
        if is_file:
            print 'file was found {}'.format(file_path)
            file_obj = open(file_path, 'r')
            client_s.sendall('HTTP/1.0 200 Document Follows\n')
            client_s.sendall('Content-length: {}\n'.format(os.path.getsize(file_path)))
            client_s.sendall('\n')
            client_s.sendall(file_obj.read())
            client_s.close()
            file_obj.close()
        else:
            print 'file was not found {}'.format(file_path)
            client_s.sendall('HTTP/1.0 404 Not Found\n')
            client_s.sendall('\n')
            client_s.sendall('Sorry, but your file couldnt be found.')
            client_s.close()
    else:
        print 'not a get request {}'.format(a)
        client_s.close()

