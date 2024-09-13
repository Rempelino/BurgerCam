import sys
import time

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from threading import Thread
import cv2
from frame import Frame
from urllib.parse import urlparse, parse_qs
from dacite import from_dict, Config, DaciteError
from settings import Settings, SettingsStructure

class Frontend:
    frame: Frame = None
    frame_has_changed = False
    streams = []
    enable_frame_update = True

    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.is_connected = False
        self.app = Flask(__name__)
        CORS(self.app)
        self.run_video = True
        self.define_routes()
        self.start_flask_thread()
        self.stream_to_stop = 0

    def update_frame(self, frame: Frame):
        self.frame = frame
        self.frame_has_changed = True

    def start_flask_thread(self):
        flask_thread = Thread(target=self.run_flask)
        flask_thread.daemon = True
        flask_thread.start()

    def run_flask(self):
        self.app.run(debug=False, threaded=True)

    def define_routes(self):

        @self.app.route('/api/settings')
        def get_settings():
            if request.method == 'OPTIONS':
                return '', 200
            return jsonify(self.settings.get_settings())

        @self.app.route('/api/set_settings', methods=['POST'])
        def set_settings():
            data = request.get_json()
            self.settings.set_settings(from_dict(data_class=SettingsStructure, data=data, config=Config(check_types=False)))
            return jsonify({'msg': 'got it'})

        @self.app.route('/enableFrameUpdate')
        def set_enable_frame_update():
            self.enable_frame_update = True
            return jsonify({'msg': 'got it'})

        @self.app.route('/disableFrameUpdate')
        def reset_enable_frame_update():
            self.enable_frame_update = False
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

        @self.app.route('/video_feed')
        def video_feed():
            ID = request.args.get("ID")
            print(ID)
            frame = self.generate_frames(ID)
            return Response(frame,
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/setting_change')
        def setting_change():
            url = request.url
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            params = {k: v[0] if v else None for k, v in params.items()}  # remove the lists that are present by default
            self.set_params(params)
            return jsonify({"msg": "updated settings"})

    def generate_frames(self, ID):
        ts = time.time()
        while True:
            #while time.time() - ts < 0.050:
            #    pass
            #ts = time.time()
            #while not self.frame_has_changed:
            #    pass
            self.frame_has_changed = True
            param = self.get_params(ID)
            frame = self.frame.get_frame(filter=param['filter'],
                                         with_rows=param['with_rows'] == 'true',
                                         with_level=param['with_level'] == 'true')
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


if __name__ == "__main__":
    myFrontend = Frontend()
