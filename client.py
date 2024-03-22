import socket


class Client:
    def __init__(self):
        self.host = "68.7.149.165"
        self.port = 8067
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        try:
            self.socket.send(data.encode("utf-8"))
            return True
        except:
            print("Error sending data")
            return False

    def receive(self):
        try:
            data = self.socket.recv(1024)
            return data.decode("utf-8")
        except:
            print("Error receiving data")
            return None

    def close(self):
        self.socket.close()
        print("Connection closed")
