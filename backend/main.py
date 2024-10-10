import asyncio
from plc import PLC
from frontend import Frontend
from interface import Settings
from imaging import Imaging
from constants import IP_PLC
import time_debug


settings = Settings()
plc = PLC(IP_PLC, 2100, settings)
frontend = Frontend(settings)
imaging = Imaging(settings, plc, frontend)


async def image_processing():
    print("started task image processing")
    while True:
        await asyncio.sleep(0)
        time_debug.commit_print()
        time_debug.print_time("starting image acquisition")
        imaging.run()
        time_debug.print_time("finished image acquisition")


async def plc_connection():
    print("started Task plc connection")

    tasks = [
        asyncio.create_task(plc.send_forever()),
        asyncio.create_task(plc.receive_forever())
    ]
    await asyncio.gather(*tasks)


async def main():
    tasks = [
        asyncio.create_task(image_processing()),
        asyncio.create_task(plc_connection())
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
