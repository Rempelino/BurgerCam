import asyncio
from plc import PLC
from frontend import Frontend
from interface import Settings
from imaging import Imaging
from constants import IP_PLC


settings = Settings()
plc = PLC(IP_PLC, 2100, settings)
frontend = Frontend(settings)
imaging = Imaging(settings, plc, frontend)


async def image_processing():
    print("started task image processing")
    while True:
        await asyncio.sleep(0)
        await imaging.run()


async def plc_connection():
    print("started Task plc connection")
    while True:
        await asyncio.sleep(0)
        await plc.listen()


async def main():
    tasks = [
        asyncio.create_task(image_processing()),
        asyncio.create_task(plc_connection())
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
