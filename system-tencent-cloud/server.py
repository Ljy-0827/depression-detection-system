import flask
import sys
from pathlib import Path
from flask_cors import CORS
import json
import zipfile
import os
from flask import send_from_directory
from flask import send_file
from flask import request

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    exec_dir = Path(sys.executable).parent.resolve()
else:
    exec_dir = Path(__file__).parent.resolve()

server = flask.Flask(__name__,
                     static_url_path='',
                     static_folder=str(exec_dir / 'web'),
                     template_folder=str(exec_dir / 'web'))

server.jinja_env.variable_start_string = '{['
server.jinja_env.variable_end_string = ']}'
CORS(server)

isComplete = [False, False, False, False, False]
score = 0
degree = ''

result_image_folder = './results/images'

cloud_video_directory = "./raw_data"

user_id = ""


# 初始化（在第一次请求前执行）
@server.before_first_request
def initialize():
    initial_data = {"files": []}
    # initial_result = {"result_status": False, "result_score": -1}
    initial_result = {"results": []}

    with open('./file_data/files_data.json', 'w') as file:
        json.dump(initial_data, file)

    with open('./result_data/result.json', 'w') as file:
        json.dump(initial_result, file)

    print("initialize")


@server.route('/')
def index():
    return flask.render_template('index.html')


# 上传用户ID
@server.route('/upload-id', methods=['POST'])
def upload_id():
    data = request.json
    user_id = data.get('user_id')

    id_file_path = "./file_data/id.json"
    id_data = {"user_id": user_id}

    with open(id_file_path, 'w') as id_file:
        json.dump(id_data, id_file, indent=2)

    result_file_path = "./result_data/result.json"

    with open(result_file_path, 'r') as result_file:
        result_data = json.load(result_file)

    new_result_entry = {"result_status": False, "result_score": -1, "id": user_id}
    result_data["results"].append(new_result_entry)

    with open(result_file_path, 'w') as result_file:
        json.dump(result_data, result_file, indent=2)

    return flask.jsonify({"message": "ID uploaded successfully"})


# 获取用户ID
@server.route('/get-id', methods=['GET'])
def get_id():
    id_file_path = "./file_data/id.json"

    try:
        with open(id_file_path, 'r') as id_file:
            id_data = json.load(id_file)
            user_id = id_data.get("user_id", None)

        if user_id is not None:
            return flask.jsonify({"user_id": user_id})
        else:
            return flask.jsonify({"message": "User ID not found"}), 404

    except FileNotFoundError:
        return flask.jsonify({"message": "ID file not found"}), 404
    except json.JSONDecodeError:
        return flask.jsonify({"message": "Error decoding JSON"}), 500


# 从云端下载视频到本地
@server.route('/download-cloud-video/<filename>', methods=['POST'])
def download_cloud_video(filename):
    json_data = request.json

    print(f"Received POST request for filename: {filename}")

    with open('./file_data/files_data.json', 'w') as file:
        json.dump(json_data, file)

    return flask.send_from_directory(cloud_video_directory, filename)


# 更新视频下载状态
@server.route('/update-download-status', methods=['POST'])
def update_download_status():
    try:
        json_data = request.get_json()

        file_data_path = './file_data/files_data.json'
        with open(file_data_path, 'w') as file:
            json.dump(json_data, file, indent=2)

        return flask.jsonify({'message': 'Download status updated successfully'}), 200
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500


# 获取云端视频文件信息
@server.route('/get-files-data', methods=['GET'])
def get_files_data():
    try:
        file_path = './file_data/files_data.json'
        return send_file(file_path, mimetype='application/json', as_attachment=True)
    except Exception as e:
        return f'Error sending files data: {e}', 500


# 获取云端结果文件信息
@server.route('/get-result-data', methods=['GET'])
def get_result_data():
    try:
        file_path = './result_data/result.json'
        return send_file(file_path, mimetype='application/json', as_attachment=True)
    except Exception as e:
        return f'Error sending files data: {e}', 500


# 上传量表作答结果
@server.route('/upload-questionnaire-answer', methods=['POST'])
def upload_questionnaire_answer():
    try:
        json_data = flask.request.get_json()
        with open('./raw_data/questionnaire/questionnaire_answer.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        return 'Questionnaire answer JSON data saved to raw_data_cache successfully', 200
    except Exception as e:
        return f'Error occurred while saving data: {e}', 500


# 上传视频
@server.route('/upload-video', methods=['POST'])
def upload_video():
    try:
        if 'video' not in flask.request.files:
            return 'No file part', 400

        video_file = flask.request.files['video']

        if video_file.filename == '':
            return 'No selected file', 400

        file_size = int(flask.request.form.get('fileSize'))
        user_id = flask.request.form.get('userId')

        file_data_path = './file_data/files_data.json'
        with open(file_data_path, 'r') as json_file:
            data = json.load(json_file)
            file_entry = {
                "fileName": video_file.filename,
                "isIntact": False,  # Initial value set to False
                "isLocal": False,
                "isDownloading": False,
                "id": user_id,
            }
            data["files"].append(file_entry)
            print(data)

        with open(file_data_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        save_path = './raw_data/' + video_file.filename
        print(video_file.filename)

        video_file.save(save_path)

        # 获取保存文件的大小
        saved_file_size = os.path.getsize(save_path)

        # 检查文件大小是否一致
        is_intact = saved_file_size == int(flask.request.form.get('fileSize'))

        # 更新files_data.json文件中的isIntact值
        with open(file_data_path, 'r') as json_file:
            data = json.load(json_file)
            for file_entry in data["files"]:
                if file_entry["fileName"] == video_file.filename:
                    file_entry["isIntact"] = is_intact

        with open(file_data_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        # 打印日志
        if is_intact:
            print('文件大小一致')
        else:
            print('文件大小不一致')

        return 'Video file saved to raw_data_cache successfully', 200

    except Exception as e:
        return f'Error occurred while saving data: {e}', 500


@server.route('/upload-result-status', methods=['POST'])
def upload_result_status():
    try:
        json_data = flask.request.get_json()
        with open('./result_data/result.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False)
        return 'JSON data saved successfully', 200
    except Exception as e:
        return f'Error occurred while saving data: {e}', 500


@server.route('/get-result-status', methods=['GET'])
def get_result_status():
    # 在这里添加获取 ./result_data/result.json 文件内容的逻辑
    result_file_path = './result_data/result.json'

    try:
        with open(result_file_path, 'r', encoding='utf-8') as result_file:
            result_data = json.load(result_file)
            return flask.jsonify(result_data)
    except FileNotFoundError:
        return flask.jsonify({'error': 'result.json not found'}), 404
    except Exception as e:
        return flask.jsonify({'error': f'Error occurred while reading result.json: {str(e)}'}), 500


@server.route('/trigger-initialize', methods=['POST'])
def trigger_initialize():
    initialize()
    return flask.jsonify({"message": "Initialization triggered successfully"})


@server.route('/calculate-result', methods=['GET'])
def calculate_result():
    try:
        score = 7
        return flask.jsonify(score)
    except Exception as e:
        return f'Error occurred while saving data: {e}', 500


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False, port=8080, ssl_context=('front_end_https.pem', 'front_end_https.key'))


@server.route('/', defaults={'path': ''})
@server.route('/<path:path>')
def catch_all(path):
    # 如果请求的路径以 /static/ 开头，那么将请求发送到静态文件目录
    if path.startswith('static/'):
        return send_from_directory(server.static_folder, path)
    # 否则，返回主页（index.html）
    return render_template('index.html')


if __name__ == '__main__':
    server.run(debug=True)