import time
from threading import Thread
from typing import Union
from urllib.parse import urlparse, parse_qs
import os
import cv2
from dacite import from_dict, Config
from flask import Flask, jsonify, request, Response,send_from_directory
from flask_cors import CORS

from frame import Frame
from interface import Interface, SettingsStructure
from log import Log
import logging
from datetime import datetime

class Frontend:
    frame: Frame = None
    frame_has_changed = False
    streams = []

    def __init__(self, settings: Interface, log: Log):
        logger = logging.getLogger('werkzeug')
        logger.setLevel(logging.WARNING)
        self.settings: Interface = settings
        self.is_connected = False
        self.app = Flask(__name__, static_folder='../Production/frontend/browser')
        CORS(self.app)
        self.run_video = True
        self.define_routes()
        self.start_flask_thread()
        self.stream_to_stop = 0
        self.log = log



    def update_frame(self, frame: Frame):
        self.frame = frame
        self.frame_has_changed = True

    def start_flask_thread(self):
        flask_thread = Thread(target=self.run_flask)
        flask_thread.daemon = True
        flask_thread.start()

    def run_flask(self):
        self.app.run(debug=False, threaded=True, port=8080, host='0.0.0.0')

    def define_routes(self):
        # Serve Angular app
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def serve(path):
            if path != "" and os.path.exists(self.app.static_folder + '/' + path):
                return send_from_directory(self.app.static_folder, path)
            else:
                return send_from_directory(self.app.static_folder, 'index.html')

        @self.app.route('/api/get_settings')
        def get_settings():
            if request.method == 'OPTIONS':
                return '', 200
            self.settings.state.frontend_update_required = False
            return jsonify(self.settings.get_settings())

        @self.app.route('/api/get_state')
        def get_state():
            if request.method == 'OPTIONS':
                return '', 200
            return jsonify(self.settings.get_state())

        @self.app.route('/api/start_log')
        def start_log():
            if request.method == 'OPTIONS':
                return '', 200
            self.log.start_log()
            return jsonify("command", "received")

        @self.app.route('/api/start_replay', methods=['POST'])
        def start_replay():
            data = request.get_json()
            self.log.start_replay(self.convert_datetime_format(data['replay'], to_file_format=True))
            return jsonify({'msg': 'got it'})

        @self.app.route('/api/stop_replay')
        def stop_replay():
            self.log.stop_replay()
            return jsonify({'msg': 'got it'})

        @self.app.route('/api/get_available_logs')
        def get_available_logs():
            if request.method == 'OPTIONS':
                return '', 200
            if "Log" not in os.listdir():
                os.mkdir("Log")
            data = os.listdir('Log')
            data_formatted = [self.convert_datetime_format(x) for x in data]

            return jsonify(data_formatted)

        @self.app.route('/api/set_settings', methods=['POST'])
        def set_settings():
            def float_hook(value: Union[int, float]) -> float:
                return float(value)
            data = request.get_json()
            self.settings.set_settings(
                from_dict(data_class=SettingsStructure, data=data, config=Config(type_hooks={float: float_hook})))
            return jsonify({'msg': 'got it'})

        @self.app.route('/api/action', methods=['POST', 'OPTIONS'])
        def perform_action():
            if request.method == 'OPTIONS':
                return '', 200
            data = request.json
            is_checked = data.get('isChecked', False)
            self.run_video = is_checked
            if is_checked:
                print("running video")
            else:
                print("stopping video")
            return jsonify({"result": is_checked})

        @self.app.route('/api/video_feed')
        def video_feed():
            ID = request.args.get("ID")
            frame = self.generate_frames(ID)
            return Response(frame,
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/api/setting_change')
        def setting_change():
            url = request.url
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            params = {k: v[0] if v else None for k, v in params.items()}  # remove the lists that are present by default
            self.set_params(params)
            return jsonify({"msg": "updated interface"})

    def generate_frames(self, ID):
        ts = time.time()
        while True:
            self.frame_has_changed = True
            param = self.get_params(ID)
            if self.frame:
                frame = self.frame.get_frame(filter=param['filter'],
                                             with_rows=param['with_rows'] == 'true',
                                             with_level=param['with_level'] == 'true')
            else:
                frame = cv2.imread('../Media/noPicAvailable.jpg')
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
            except cv2.error:
                frame = cv2.imread('../Media/noPicAvailable.jpg')
                ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def get_params(self, ID):
        for par in self.streams:
            if par['ID'] == ID:
                return par
        par = {'filter': None,
               'with_rows': 'false',
               'with_level': 'false'}
        return par

    def set_params(self, param):
        existing_param = next((p for p in self.streams if p.get('ID') == param.get('ID')), None)
        if existing_param:
            existing_param.update(param)
        else:
            self.streams.append(param)
    @staticmethod
    def convert_datetime_format(input_datetime, to_file_format=False):
        if to_file_format:
            dt = datetime.strptime(input_datetime, "%Y.%m.%d %H:%M:%S")
            return dt.strftime("%Y_%m_%d_%H_%M_%S")
        dt = datetime.strptime(input_datetime, "%Y_%m_%d_%H_%M_%S")
        return dt.strftime("%Y.%m.%d %H:%M:%S")

if __name__ == "__main__":
    myFrontend = Frontend()
