from socket import socket
import threading
import re
import time


"""
    La classe ClientListener récupére le module threading
"""


class ClientListener(threading.Thread):

    """
        initialise le constructeur, en reprenant en parametre soi même, le server, le socket et l'adresse
        -permet de lier les send.message du client au server via cette classe ClientThread
        !!! threading.Thread est le reseau de communication pour le send.message du thread et rien d'autre
        défini le username : "No username"
    """

    def __init__(self, server, socket, address):
        super(ClientListener, self).__init__()
        self.server = server
        self.socket = socket
        self.address = address
        self.listening = True
        self.username = "No username"

    """
        la fonction run
        prend en parametre l'objet ClientListener 
        tant que la variable listening est à true
        récupére dans la data la donnée formalisé en donnée 1024 et encode utf8.
            -le try va autorise tous les données qui sont en 1024 et au format utf8 et le recuperer dans data
        en cas d'exception, gérer l'erreur
    """

    def run(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)
        print("Ending client thread for", self.address)

    """
        la fonction quit 
        prend en parametre l'objet ClientListener 
        permet de fermer la connexion entre client et le serveur
        affichera no_username has quit puisque cest le coté serveur qui sera éteint
    """

    def quit(self):
        self.listening = False
        self.socket.close()
        self.server.remove_socket(self.socket)
        self.server.echo("{0} has quit\n".format(self.username))

    """
        la fonction handle_msg
        prend en parametre l'objet ClientListener et la data récupéré de la classe client
        group de 1 permet de recuperer la 1ere variable, 
        (c'est une fonction regex qui peut etre utilise de plusieurs manieres pour recuperer un mot entier)
            - sinon ca quitte le jeu
    """

    def handle_msg(self, data):
        print(self.address, "sent :", data)
        username_result = re.search('^USERNAME (.*)$', data)
        if username_result:
            self.username = username_result.group(1)
            self.server.echo("{0} has joined.\n".format(self.username))
        elif data == "QUIT":
            self.quit()
        elif data == "":
            self.quit()
        else:
            self.server.echo(data)
