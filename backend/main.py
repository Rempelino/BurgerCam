import asyncio
from plc import PLC
from frontend import Frontend
from interface import Settings
from imaging import Imaging
from constants import IP_PLC
import time_debug

def main():
    settings = Settings()
    plc = PLC(IP_PLC, 2100, settings)
    frontend = Frontend(settings)
    imaging = Imaging(settings, plc, frontend)
    while True:
        imaging.run()
        plc.listen()
        time_debug.print_time("-----DONE-----")
        time_debug.commit_print()

if __name__ == '__main__':
    main()
