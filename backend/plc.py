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

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.settings.set_PLC_connection_state(True)
            print("Connected")
            return True
        except Exception as e:
            print(f"An error occurred while connecting: {e}")
            return False

    def send_receive(self):
        data = b'0'
        if not self.socket:
            connected = self.connect()
            if not connected:
                return None

        if self.settings.plc_update_request_flag:
            self.send_command = MessageType.SETTINGS
            self.settings.plc_update_request_flag = False

        match self.send_command:
            case MessageType.IDLE:
                if self.new_line_values_available:
                    self.new_line_values_available = False
                    if len(self.line_values) != 0:
                        data = bytes([self.float_to_byte(x) for x in self.line_values])
                        self.send_command = MessageType.LINE_VALUE
                    else:
                        pass
            case MessageType.REQUEST_SETTINGS:
                print("requesting settings from plc")
            case MessageType.SETTINGS:
                data = self.settings.get_settings(as_byte_stream=True)

        data = bytes([self.send_command.value]) + data

        try:
            self.socket.sendall(data)
            self.send_command = MessageType.IDLE
            self.received_byte_string = self.socket.recv(1024)
        except ConnectionResetError as e:
            print(f'ConnectionResetError: {e} -> closing connection to PLC')
            self.socket = None
            self.settings.set_PLC_connection_state(False)
            return
        except ConnectionAbortedError as e:
            print(f'ConnectionAbortedError: {e} -> closing connection to PLC')
            self.socket = None
            self.settings.set_PLC_connection_state(False)
            return
        except OSError as e:
            print(f'OSError: {e} -> Timeout - closing connection to PLC')
            self.socket = None
            self.settings.set_PLC_connection_state(False)
            return

        if len(self.received_byte_string) != 0:
            self.process_received_data()

    def listen(self):
        self.send_receive()

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
