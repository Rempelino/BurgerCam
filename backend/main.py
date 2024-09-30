import asyncio
from plc import PLC
from frontend import Frontend
from interface import Settings
from imaging import Imaging
from constants import IP_PLC
import os
import sys
import subprocess
import shutil


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


def start_angular_frontend_windows():
    os.chdir('..')
    os.chdir("frontend")
    full_command = f'powershell.exe -Command ng serve'
    process = subprocess.Popen(full_command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               creationflags=subprocess.DETACHED_PROCESS)


def start_angular_frontend_linux():
    os.chdir('..')
    os.chdir("/home/henry/BurgerCam/frontend")
    command = 'ng serve'
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               preexec_fn=os.setsid)  # This creates a new session, detaching the process
    process.stdout.close()
    process.stderr.close()
    print(f"Angular frontend started with PID: {process.pid}")
    return process


async def main():
    tasks = [
        asyncio.create_task(image_processing()),
        asyncio.create_task(plc_connection())
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        start_angular_frontend_windows()
    else:
        start_angular_frontend_linux()
    asyncio.run(main())
