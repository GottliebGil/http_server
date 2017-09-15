from socket import *
import os

SERVER_HOME_DIRECTORY = os.path.join(os.path.expanduser('~'), os.path.join(os.getcwd(), 'serve'))

ERRORS_HOME_DIRECTORY = os.path.join(os.path.expanduser('~'), os.path.join(os.getcwd(), 'errors'))

REQUEST_HANDLERS = {}

PORT = 8080


def create_header(err_code, content_length=0):
    """Returns header for a request"""
    if err_code == 200:
        data = 'HTTP/1.0 200 Document Follows\n'
        data += 'Content-length: {}\n'.format(content_length)
        data += '\n'
        return data
    if err_code == 404:
        data = 'HTTP/1.0 404 Not Found\n'
        data += '\n'
        return data


def request_handler(req_type):
    """Adds request-handling method to the array"""
    def add_to_registry(func):
        REQUEST_HANDLERS[req_type] = func
    return add_to_registry


@request_handler('GET')
def handle_get_request(req, client_s):
    """Handler for GET requests"""
    req[1] = req[1]
    file_path = SERVER_HOME_DIRECTORY + req[1]
    print 'File: {}'.format(file_path)
    is_file = os.path.isfile(SERVER_HOME_DIRECTORY + req[1])
    if is_file:
        print 'file was found'
        file_obj = open(file_path, 'r')
        client_s.sendall(create_header(200, os.path.getsize(file_path)))
        client_s.sendall(file_obj.read())
        file_obj.close()
    else:
        print 'file was not found'
        client_s.sendall(create_header(404))
        error_obj = open(os.path.join(ERRORS_HOME_DIRECTORY, '404.html'), 'r')
        client_s.sendall(error_obj.read())
    client_s.close()


def start_server():
    server_s = socket(AF_INET, SOCK_STREAM)

    server_s.bind(('0.0.0.0', PORT))

    server_s.listen(5)
    print 'Listening to port {}...'.format(PORT)
    while True:
        print '-------------'
        (client_s, client_addr) = server_s.accept()
        a = client_s.recv(1000).split(' ')
        if len(a) <= 2:
            print 'Bad request'
            client_s.close()
            continue
        if a[0] not in REQUEST_HANDLERS.keys():
            print 'Request couldn\'t be handled: {}'.format(a)
            client_s.close()
            continue
        print 'Handling a {} request'.format(a[0])
        REQUEST_HANDLERS[a[0]](a, client_s)


if __name__ == '__main__':
    start_server()