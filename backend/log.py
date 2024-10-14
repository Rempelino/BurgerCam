from interface_definition import SettingsStructure
from save_settings import read_dataclass_from_file, write_dataclass_to_file
from interface import Interface
from datetime import datetime, timedelta
import os
import cv2
import shutil
from pathlib import Path
import asyncio


class Log:
    logging_active = False
    replay_active = False
    replay_path = None
    frames = None
    log_time = timedelta(seconds=60)
    time_stamp = None
    start_time = None

    def __init__(self, interface: Interface):
        self.interface = interface

    def update_frame(self, frame):
        if not self.logging_active:
            return
        self.frames.append(frame)

        elapsed_time = datetime.now() - self.start_time
        progress_percentage = (elapsed_time / self.log_time) * 100
        self.interface.set_log_state(logging_active=True, progress=progress_percentage)


        if datetime.now() - self.start_time > self.log_time:
            self.logging_active = False
            tasks = [
                asyncio.create_task(self.save_video())
            ]
            asyncio.gather(*tasks)

    def start_log(self):
        #create directory if it doesnt exist
        if "Log" not in os.listdir():
            os.mkdir("Log")

        self.remove_old_logs()
        self.interface.set_log_state(True, False, 0.0)
        self.frames = []
        self.logging_active = True
        self.start_time = datetime.now()
        self.time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        # Create the directory
        try:
            os.mkdir(f'Log/{self.time_stamp}')
        except FileExistsError:
            print(f"Directory '{self.time_stamp}' already exists.")
        except PermissionError:
            print("Permission denied: Unable to create directory.")
        except Exception as e:
            print(f"An error occurred: {e}")
        write_dataclass_to_file(self.interface.get_settings(), f'Log/{self.time_stamp}/settings.pkl')

    async def save_video(self):
        self.interface.set_log_state(saving_active=True)
        fps = len(self.frames) / self.log_time.seconds
        images = self.frames
        output_path = f'Log/{self.time_stamp}/video.mp4'

        if not images:
            raise ValueError("The list of images is empty")

        height, width = images[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for index, image in enumerate(images):
            await asyncio.sleep(0)
            self.interface.set_log_state(saving_active=True, progress=(index/len(images)*100))
            # print(f'saving {(index/len(images)*100):.1f}%')
            # Ensure the image is in BGR color space (OpenCV default)
            if len(image.shape) == 2:  # Grayscale
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif image.shape[2] == 3:  # Assuming it's already BGR
                pass
            elif image.shape[2] == 4:  # RGBA
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            else:
                raise ValueError(f"Unsupported image shape: {image.shape}")
            video_writer.write(image)

        video_writer.release()
        print(f"Video saved to {output_path}")
        self.interface.set_log_state(saving_active=False)

    def start_replay(self, replay):
        self.interface.set_log_state(replay_active=True)
        self.replay_active = True
        self.replay_path = 'log/' + replay + '/video.mp4'
        self.interface.set_settings(read_dataclass_from_file(SettingsStructure, f'Log/{replay}/settings.pkl'))
        print(self.replay_path)

    def stop_replay(self):
        self.interface.set_log_state(replay_active=False)
        self.replay_active = False
        self.replay_path = None

    @staticmethod
    def remove_old_logs():
        log_dir = Path('Log')
        if not log_dir.exists() or not log_dir.is_dir():
            print("Log directory does not exist.")
            return

        # Get all subdirectories in the Log directory
        log_folders = [f for f in log_dir.iterdir() if f.is_dir()]

        # Sort the folders by modification time (newest first)
        log_folders.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Keep the most recent logs, remove the rest
        for folder in log_folders[5:]:
            try:
                shutil.rmtree(folder)
                print(f"Removed old log: {folder}")
            except Exception as e:
                print(f"Error removing {folder}: {e}")

