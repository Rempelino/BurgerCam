from interface_definition import SettingsStructure
from save_settings import read_dataclass_from_file, write_dataclass_to_file
from interface import Interface
from datetime import datetime, timedelta
import os
import cv2
import shutil
from pathlib import Path


class Log:
    logging_active = False
    replay_active = False
    replay_path = None
    log_time = timedelta(seconds=60)
    time_stamp = None
    start_time = None
    video_writer = None

    def __init__(self, interface: Interface):
        self.interface = interface

    def update_frame(self, frame):
        if not self.logging_active:
            return

        elapsed_time = datetime.now() - self.start_time
        progress_percentage = (elapsed_time / self.log_time) * 100
        self.interface.set_log_state(logging_active=True, progress=progress_percentage)

        if self.video_writer is None:
            fps = 20
            output_path = f'Log/{self.time_stamp}/video.mp4'
            height, width = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


        if len(frame.shape) == 2:  # Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 3:  # Assuming it's already BGR
            pass
        elif frame.shape[2] == 4:  # RGBA
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        else:
            raise ValueError(f"Unsupported image shape: {frame.shape}")
        self.video_writer.write(frame)


        if datetime.now() - self.start_time > self.log_time:
            output_path = f'Log/{self.time_stamp}/video.mp4'
            self.video_writer.release()
            self.video_writer = None
            print(f"Video saved to {output_path}")
            self.interface.set_log_state(logging_active=False)
            self.logging_active = False

    def start_log(self):
        #create directory if it doesnt exist
        if "Log" not in os.listdir():
            os.mkdir("Log")

        # self.remove_old_logs()
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

