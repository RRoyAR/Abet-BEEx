from fastapi import WebSocket

from Backend.src.utils.singletone_meta import SingletonMeta


class SocketConnectionManager(metaclass=SingletonMeta):
    """
    Class allowing implementation of the Observer pattern.
    For any new socket, we'll append our listeners.
    When any event coming through we can broadcast it to all of our listeners (observers)
    """
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print("New websocket in")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print("websocket disconnected")
        self.active_connections.remove(websocket)

    async def broadcast(self, event: dict):
        """
        After an incoming event. broadcast it to any who listen,
        allowing the receiver to update accordingly
        :param event: Real-Time event that may change the available metrics or
        any other data the front-end might be based on
        :return: None
        """
        print("Broadcasting new event")
        for connection in self.active_connections:
            await connection.send_json(event)

