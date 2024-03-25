import socket

SERVER_HOST = ""
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print("Executing server")
print("Listening for connections at port %s" % SERVER_PORT)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    if request:
        print(request)

        request_line = request.split("\n")[0]
        request_method, path, http_version = request_line.split()

        if request_method == "GET":
            if path == "/":
                path = "/index.html"

            try:
                with open("htdocs" + path, "r") as file:
                    content = file.read()
                    response = f"HTTP/1.1 200 OK\n\n{content}"
            except FileNotFoundError:
                response = (
                    "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
                )

        elif request_method == "PUT":
            request_headers, request_body = request.split("\r\n\r\n", 1)
            file_path = "htdocs" + path
            with open(file_path, "w") as file:
                file.write(request_body)
                response = f"HTTP/1.1 201 Created\n\n<p>{path} Created.</p>"

        else:
            response = "HTTP/1.1 400 BAD REQUEST\n\n<h1>Bad Request</h1>"

        client_connection.sendall(response.encode())
        client_connection.close()

server_socket.close()
