import threading
import socket
import time
import re


class Client():

    """ c'est l'objet, construit le client, recupere le nom, le server et le port
        -Connect Établit une connexion à un hôte distant.
        -Listening est une variable booleenne passé en dur en true.
        -Send envoie de manière synchrone des données à l’hôte distant spécifié dans 
        la Connect méthode ou Accept et retourne le nombre d’octets envoyés avec succès. 
    """

    def __init__(self, username, server, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.username = username
        self.send("USERNAME {0}".format(username))
        self.listening = True

    """
        fonction listener :
        prend en parametre l'objet client qui est entré en paramètre
        tant que le listener est actif (boolean listening = true)
        initialise une var data en chaine de string vide
        puis lance un essai :
            -le try va autorise tous les données qui sont en 1024 et au format utf8 et le recuperer dans data (de la classe ClientThread)
            -le except c'est le else, qui va te dire qu'il ne recoit pas de donnée
            -time sleep, permet de ralentir les temps d actualisation. ici cest a 0.1sec
    """

    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)

    """
        la fonction listen :
        prend en parametre l'objet client qui est entré en paramètre
        Le multithreading n’est pas une exécution strictement parallèle. Les threads peuvent être considérés 
        comme des entités distinctes du flux d’exécution de différentes parties de votre programme 
        s’exécutant indépendamment. Donc, essentiellement, les threads ne s’exécutent pas en parallèle, 
        mais Python passe d’un thread à un autre si rapidement qu’il semble qu’ils sont parallèles.
        Les threads communiquent entre eux plus facilement puisque c’est le même processus.
            -l'argument target, définit la cible sur laquelle elle charge, ici c'est la fonction listener.
            -daemon is a Garbage Collector which is going to execute in the background and destroy all 
            the useless objects
            -start démarre le thread
            la fonction listen permet de rendre l objet client en multithread et de lancer les vars

    """

    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    """
        la fonction send
        prend en parametre l'objet client et le message
            -re.search, c'est le regex, le try va tester s'il y aura une donnée dans username_result
            -s'il n'y a rien dans username_result, alors on injecte l'objet crée en nom et message
            -encode le normale, 
                -send() fonctionne en tcp
                -sendall() fonctionne envoi en format udp qui envoi tout le buffer
            -except gerer l'exception, l'erreur

    """

    def send(self, message):
        try:
            username_result = re.search('^USERNAME (.*)$', message)
            if not username_result:
                message = "{0}: {1}".format(self.username, message)
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            print("unable to send message")

    """
        la fonction tidy_up
        prend en parametre l'objet client qui est instancié (self)
        si la var listening est eteint, ce qui veut dire que le client n'ecoute plus, alors on ferme le socket.
            -definition de SOCKET = communication entre un client et un serveur
    """

    def tidy_up(self):
        self.listening = False
        self.socket.close()

    """
        la fonction handle_msg
        prend en parametre l'objet client qui est instancié (self) et les informations dans la data
            -si les données dans la data : est "QUIT" alors executer la fonction tidy_up qui ferme la connexion
            -pareil quand il n'y a rien dans la data "" <= vide
            -sinon afficher ce qui a été envoyé dans la data
    """

    def handle_msg(self, data):
        if data == "QUIT":
            self.tidy_up()
        elif data == "":
            self.tidy_up()
        else:
            print(data)

    """
        donc la condition pour que la classe Client fonctionne :
            -que le constructeur main soit définit dans l'objet
            -puis récupére les input =>
            input : la valeur que tu saisies dans la console recupérer en parametre par le constructeur client
            -listen lance le multi threading
            -initialise le message a "" vide, si le message est renvoye a vide
            -tant que le message n'est pas QUIT ou vide, et bien l'objet client sera toujours en écoute

    """


if __name__ == "__main__":
    username = input("username: ")
    server = input("server: ")
    port = int(input("port: "))
    client = Client(username, server, port)
    client.listen()
    message = ""
    while message != "QUIT":
        message = input()
        client.send(message)
