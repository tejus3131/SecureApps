from flask import Flask, render_template, send_from_directory, jsonify
import json


class SecureAppsServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=self.index, methods=['GET'])
        self.app.add_url_rule('/', view_func=self.files, methods=['POST'])
        self.app.add_url_rule('/<filename>/<requested_item>', view_func=self.info, methods=['GET'])

        with open('static\info.json', 'r') as json_file:
            self.info = json.load(json_file)
        self.names = list(self.info.keys())

    def index(self):
        return render_template('index.html')
    
    def info(self, filename, requested_item):
        if requested_item == 'exe':
            filename = self.info[filename]['exe_name']
            return send_from_directory('static', filename, as_attachment=True)
        elif requested_item == 'ico':
            filename = self.info[filename]['icon_name']
            return send_from_directory('static', filename, as_attachment=True)
        elif requested_item == 'info':
            return jsonify(self.info[filename])
        else:
            return 'Invalid request'
        
    def files(self):
        return self.names
    
    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    app = SecureAppsServer()
    app.run()
