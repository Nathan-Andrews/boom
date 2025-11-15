from flask import Flask, jsonify, render_template, send_from_directory, request

import os
import subprocess
import re

app = Flask(__name__)

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

ANSI_COLORS = {
    '49': 'table-row-odd',
    '100': 'table-row-even',
}

PASSWD="a27c37953ea57cf95ec55e628cf518b168e7b62bc50ff0a1c8b7ab39da0f93ad"
KEY="blahblah32348h2nfiwekhfgjng9qeqirubgkvq" #TODO: make this random and keep list of active
BOOMUSERDIR=<unset>
BOOMBOSS=<unset>
BOOMRCS=<unset>
BOOMINSTALL=<unset>
BOOMPORT=<unset>
BOOMCFGFILE=<unset>
CMDPREFIX=f"export BOOMSITERUNNER=runner; export BOOMCFGFILE=\"{BOOMCFGFILE}\"; export BOOMSOURCE=\"/{BOOMUSERDIR}/{BOOMBOSS}/{BOOMRCS}/.boomrc\"; bash -c \"source $BOOMSOURCE &>/dev/null; "

def ansi_to_html(text):
    def replace_ansi(match):
        code = match.group(0)
        if code == '\x1B[0m':
            return '</span>'
        elif code.startswith('\x1B['):
            class_code = code[2:-1]
            if class_code in ANSI_COLORS:
                return f'<span class="{ANSI_COLORS[class_code]}">'
        return ''

    text = ANSI_ESCAPE.sub(replace_ansi, text)
    return text.replace('\n', '<br>')

def validate_key(key):
    if key == KEY:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('.boom.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

@app.route('/run_command', methods=['POST'])
def run_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}boom latest && echo && boom favorite && echo && boom drought longest && echo && boom board && echo -n Patch && boom patchnotes current && echo && boom hall"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500

####
# Individual command routes
@app.route('/run_boom_latest_command', methods=['POST'])
def run_boom_latest_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}boom latest && echo"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/run_boom_favorite_command', methods=['POST'])
def run_boom_favorite_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}boom favorite && echo"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/run_boom_drought_longest_command', methods=['POST'])
def run_boom_drought_longest_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}boom drought longest && echo"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/run_boom_board_command', methods=['POST'])
def run_boom_board_command():
    try:
        api_key = request.get_json().get('key')
        boardarg = request.get_json().get('boardcmd') # One of avg/drought/freq/full/today/top/null
        if boardarg is None: boards = [""]
        elif ' ' in boardarg: boards = boardarg.split()
        else: boards = [boardarg]
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        # Empty boardarg == avg/freq/top/drought boards
        stdout = ""
        stderr = []
        for arg in boards:
            cmd = f'{CMDPREFIX}boom board {arg}"'
            result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            stdout += ansi_to_html(result.stdout)
            stderr += result.stderr.splitlines()

        return jsonify(output=stdout, error=stderr)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/run_boom_patchnotes_current_command', methods=['POST'])
def run_boom_patchnotes_current_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}echo -n Patch && boom patchnotes current && echo"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/run_boom_hall_command', methods=['POST'])
def run_boom_hall_command():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        cmd = f'{CMDPREFIX}boom hall && echo"'
        result = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return jsonify(output=ansi_to_html(result.stdout), error=result.stderr.splitlines())
    except Exception as e:
        return jsonify(error=str(e)), 500
####

@app.route('/read_log_file', methods=['POST'])
def read_log_file():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        logfile = f"/{BOOMUSERDIR}/{BOOMBOSS}/{BOOMINSTALL}/.boomlog"
        with open(logfile, 'r') as file:
            lines = file.readlines()
            display = reversed(lines[-54:]) if len(lines) > 54 else reversed(lines)
            return jsonify(lines=list(display))
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/read_boommeter_file', methods=['POST'])
def read_boommeter_file():
    try:
        api_key = request.get_json().get('key')
        if not validate_key(api_key): return jsonify(error="Invalid API Key"), 401

        logfile = f"/{BOOMUSERDIR}/{BOOMBOSS}/{BOOMINSTALL}/.boommeterlog"
        with open(logfile, 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if line.startswith('[CIPHER] '):
                    lines[idx] = line.lstrip('[CIPHER] ')
                elif line.startswith('[EDITED] '):
                    lines[idx] = f"*{line.lstrip('[EDITED] ')}"
                elif line.startswith('[ASCII] '):
                    lines[idx] = line.lstrip('[ASCII] ')
            display = reversed(lines[-53:]) if len(lines) > 53 else reversed(lines)
            return jsonify(lines=list(display))
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/boompass', methods=['POST'])
def boompass():
    passwd = request.get_json().get('password')

    if passwd == PASSWD:
        return jsonify(valid=True, key=KEY)
    else:
        return jsonify(valid=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=BOOMPORT, debug=True)
