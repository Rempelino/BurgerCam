import asyncio
import time_debug
from interface import MessageType
from time import sleep
import time


class PLC:
    line_values = None
    new_line_values_available = False
    received_byte_string = None
    send_command: MessageType = MessageType.SETTINGS_GET
    connection_process_active = False
    state_update_interval = 100
    current_interval = 50


    def __init__(self, host, port, settings):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.is_connected = False
        self.settings = settings

    async def connect(self):
        if self.is_connected:
            return
        if self.connection_process_active:
            while self.connection_process_active:
                await asyncio.sleep(1)
        while not self.is_connected:
            self.connection_process_active = True
            try:
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                self.connection_process_active = False
                self.is_connected = True
                self.settings.set_PLC_connection_state(True)
                print("Connected")
            except Exception as e:
                print(f"An error occurred while connecting: {e}")
                await asyncio.sleep(1)

    def disconnect(self):
        self.is_connected = False
        self.settings.set_PLC_connection_state(False)

    async def send_forever(self):
        while True:
            await self._send()

    async def receive_forever(self):
        while True:
            await self._receive()

    async def _send(self):
        await self._wait_for_data_to_send()
        await self.connect()
        data = b'0'
        match self.send_command:
            case MessageType.LINE_VALUE:
                self.new_line_values_available = False
                if len(self.line_values) != 0:
                    data = bytes([self.float_to_byte(x) for x in self.line_values])
                else:
                    pass
            case MessageType.SETTINGS_SET:
                self.settings.plc_settings_update_request_flag = False
                data = self.settings.get_settings(as_byte_stream=True)
            case MessageType.STATE_SET:
                self.settings.plc_state_update_request_flag = False
                data = self.settings.get_state(as_byte_stream=True)
                sleep(0.1) # to make sure protocols dont mix
                #print("sending state update")

        data = bytes([self.send_command.value]) + data

        try:
            #print(data)
            self.writer.write(data)
            await self.writer.drain()
            #sleep(1)
            self.send_command = MessageType.IDLE

            self.current_interval = self.current_interval + 1
            if self.current_interval > self.state_update_interval:
                self.current_interval = 0
                self.settings.plc_state_update_request_flag = True

        except Exception as e:
            print(f'Exception while sending: {e} -> closing connection to PLC')
            self.disconnect()
            return
        time_debug.print_time("done sending")

    def _data_to_send_available(self):
        if self.send_command == MessageType.IDLE:
            if self.new_line_values_available:
                self.send_command = MessageType.LINE_VALUE
            if self.settings.plc_settings_update_request_flag:
                self.send_command = MessageType.SETTINGS_SET
            if self.settings.plc_state_update_request_flag:
                self.send_command = MessageType.STATE_SET
            if self.settings.plc_settings_download_request_flag:
                self.send_command = MessageType.SETTINGS_GET
        return self.send_command != MessageType.IDLE

    async def _wait_for_data_to_send(self):
        while not self._data_to_send_available():
            await asyncio.sleep(0)

    async def _receive(self):
        await self.connect()
        try:
            self.received_byte_string = await self.reader.read(1024)
        except Exception as e:
            print(f'Exception while receiving: {e} -> closing connection to PLC')
            self.socket = None
            self.settings.set_PLC_connection_state(False)
            return

        if self.received_byte_string == b'':
            print("received empty message")
            self.disconnect()
            return

        print(f"received command {MessageType(list(self.received_byte_string)[0])}")
        if len(self.received_byte_string) != 0:
            command = MessageType(list(self.received_byte_string)[0])
            match command:
                case MessageType.SETTINGS_GET:
                    self.settings.set_settings(self.received_byte_string[1:])

    def send_line_values(self, line_values):
        self.line_values = line_values
        self.new_line_values_available = True

    @staticmethod
    def float_to_byte(f):
        if not 0 <= f <= 100:
            raise ValueError("Float must be between 0 and 100")
        return int(round(f))
