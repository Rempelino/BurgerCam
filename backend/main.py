import asyncio
from plc import PLC
from frontend import Frontend
from interface import Settings
from imaging import Imaging


settings = Settings()
plc = PLC('192.168.100.1', 2100, settings)
frontend = Frontend(settings)
imaging = Imaging(settings, plc, frontend)

async def image_processing():
    print("started task image processing")
    while True:
        await imaging.run()


async def plc_connection():
    print("started Task plc connection")
    while True:
        await plc.listen()

async def main():
    tasks = [
        asyncio.create_task(image_processing()),
        asyncio.create_task(plc_connection())
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
