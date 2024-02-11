import os
from daphne.server import Server
from asgi import application  # Assurez-vous que le chemin vers votre ASGI application est correct

def start_application():
    print("Starting the application...")
    try:
        server = Server(application, host='0.0.0.0', port=8000)
        server.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start_application()


