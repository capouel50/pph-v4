import os
from daphne.server import Server
from Hospi.asgi import application  # Assurez-vous que le chemin vers votre ASGI application est correct
import os

os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def start_application():
    print("Starting the application...")
    try:
        server = Server(application, host='0.0.0.0', port=8000)
        server.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    start_application()


