import asyncio
import socket
import time_debug
from interface import MessageType

class PLC:
    line_values = None
    new_line_values_available = False
    received_byte_string = None
    send_command: MessageType = MessageType.REQUEST_SETTINGS

    def __init__(self, host, port, settings):
        self.host = host
        self.port = port
        self.socket = None
        self.settings = settings

    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            self.socket = (reader, writer)
            print("Connected")
            return True
        except Exception as e:
            print(f"An error occurred while connecting: {e}")
            return False

    async def send_receive(self):
        data = b'0'
        if not self.socket:
            connected = await self.connect()
            if not connected:
                return None


        reader, writer = self.socket
        if self.settings.plc_update_request_flag:
            self.send_command = MessageType.SETTINGS
            self.settings.plc_update_request_flag = False

        match self.send_command:
            case MessageType.IDLE:
                try:
                    await asyncio.wait_for(self._wait_for_values(), timeout=0.5)
                    self.new_line_values_available = False
                    if len(self.line_values) != 0:
                        data = bytes([self.float_to_byte(x) for x in self.line_values])
                        self.send_command = MessageType.LINE_VALUE
                    else:
                        pass
                except asyncio.TimeoutError:
                    pass
            case MessageType.REQUEST_SETTINGS:
                print("requesting settings from plc")
            case MessageType.SETTINGS:
                data = self.settings.get_settings(as_byte_stream=True)

        if self.send_command != MessageType.IDLE:
            data = bytes([self.send_command.value]) + data

        try:
            writer.write(data)
            await writer.drain()
            self.send_command = MessageType.IDLE

            self.received_byte_string = await reader.read(1024)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f'An error occured while beeing connected: {e}')
            self.socket = None
            return

        if len(self.received_byte_string) != 0:
            self.process_received_data()

    async def ready_for_new_frame(self):
        while self.new_line_values_available and self.socket:
            await asyncio.sleep(0)

    async def _wait_for_values(self):
        while not self.new_line_values_available:
            await asyncio.sleep(0)

    async def listen(self):
        while True:
            await self.send_receive()

    def send_line_values(self, line_values):
        self.line_values = line_values
        self.new_line_values_available = True

    def process_received_data(self):
        command = MessageType(list(self.received_byte_string)[0])
        match command:
            case MessageType.SETTINGS:
                print(f"received command {command}")
                self.settings.set_settings(self.received_byte_string[1:])
                self.request_settings = False
            case MessageType.ALIVE:
                pass


    @staticmethod
    def float_to_byte(f):
        if not 0 <= f <= 100:
            raise ValueError("Float must be between 0 and 100")
        return int(round(f))
