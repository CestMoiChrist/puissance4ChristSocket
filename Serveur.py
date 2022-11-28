import socket
import signal  # identifie les signaux pour kill le programme
import sys  # utilisé pour sortir du programme
import time
# ClientThread permet de recuperer les send.message et sendall.message
from ClientThread import ClientListener


class Server():

    """
    le serveur n'a besoin que du param port pour se lancer
        entre dans la variable listener : socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        les parametres principaux du socket
        -bind : permet de le définir en tant que serveur
        -listen : écoute les connexions entrante
        -afficher le port utilisé avec print
        -clients_sockets : définit un tableau a vide

    """

    def __init__(self, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', port))
        self.listener.listen(1)
        print("Listening on port", port)
        self.clients_sockets = []
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    """
        la fonction signal_handler
        ce sot les librairies
        signal kill le programme
        frame ferme les tableaux je suppose
    """

    def signal_handler(self, signal, frame):
        self.listener.close()
        self.echo("QUIT")

    """  
        la fonction run
        prend en parametre l'objet Server
            -accept : en attente de connexion 
    """

    def run(self):
        while True:
            print("listening new customers")
            try:
                (client_socket, client_adress) = self.listener.accept()
            except socket.error:
                sys.exit("Cannot connect clients")
            self.clients_sockets.append(client_socket)
            print("Start the thread for client:", client_adress)
            client_thread = ClientListener(self, client_socket, client_adress)
            client_thread.start()
            time.sleep(0.1)

    def remove_socket(self, socket):
        self.client_sockets.remove(socket)

    def echo(self, data):
        print("echoing:", data)
        for sock in self.clients_sockets:
            try:
                sock.sendall(data.encode("UTF-8"))
            except socket.error:
                print("Cannot send the message")


if __name__ == "__main__":
    server = Server(59001)
    server.run()
