import wakatime
import traceback
import sublime
import sublime_plugin
import platform
import traceback
import time
from . import commands
from .lib import fusion360utils as futil
import subprocess
import zipfile
import sys
from io import BytesIO
import json
import os 
import requests
import configparser
import shutil
try:
    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import Error as ConfigParserError
except ImportError:
    from configparser import ConfigParser, Error as ConfigParserError
try: 
    import adsk.core
    import adsk.fusion
    import adsk.cam
except ImportError:
    adsk = None

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)
is_win = platform.system() == 'Windows'

def parseConfigFile(configFile):
    kwargs = {} if is_py2 else {"strict": False}
    configs = configParser(**kwargs)
    try:
        with open(configFile, "r", encoding="utf-8") as f:
            try:
                if is_py2:
                    configs.readfp(f)
                else:
                    configs.read_file(f)
                return configs
            except ConfigParserError:
                log(ERROR, traceback.format_exc())
                return None
    except IOError:
        log(DEBUG, "Error: Could not read from config file {0}\n".format(configFile))
        return configs

class api_key(object):
    _key = None
    def read_wakatime_key(self):
        if self._key:
            return self._key
        key =  SETTINGS.get("api_key")
        if key:
            self._key = key
            return self._key

        configs = None
        try:
            configs = parseConfigFile(CONFIG_FILE)
            if configs:
                if configs.has_option("settings", "api_key"):
                    key = configs.get("setting", "api_key")
                    if key:
                        self._key = key
                        return self._key
        except:
            pass
        key = self.apiKeyFromVault(configs):
        vault = SETTINGS.get("api_key_vault_cmd")
        if not vault_cmd and configs:
            try: 
                if configs.has_option('settings', 'api_key_vault_cmd'):
                    vault_cmd = configs.get('setting', 'api_key_vault_cmd')
            except:
                pass
        if not vault_cmd or not vault_cmd.strip():
            return None
         try:
            process = Popen(vault_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            retcode = process.poll()
            if retcode:
                log(ERROR, 'Vault command error ({retcode}): {stderr}'.format(retcode=retcode, stderr=u(stderr)))
                return None
            return stdout.strip() or None
        except:
            log(ERROR, traceback.format_exc())

        return None
        def write(self):
            global SETTINGS
            self._key = key
            SETTINGS.set('api_key', str(key))
            sublime.save_settings(SETTINGS_FILE )
APIKEY = api_key()
def 
def get_wakatime_path():
    wakatime_dir = os.path.join(os.path.expanduser("~"), ".wakatime")
    if not os.path.exists(wakatime_dir):
        os.makedir(wakatime_dir)
    return os.path.join(wakatime_dir, "wakatime-cli")

def get_arch():
    arch = os.uname().machine
    if arch == "x86_64":
        return "AMD64"
    elif arch in ("aarch64", "arm64"):
        return "ARM64"
    else:
            return "unknow architecture"
def get_wakatime_cli():
    arch = get_arch()
    arch = arch.lower()
    system = platform.system()
    url = ""
    if system == "Windows":
        url = f"https://github.com/wakatime/wakatime-cli/releases/download/v1.106.1/wakatime-cli-windows-{arch}.zip"
    elif system == "Darwin":
        url = "https://github.com/wakatime/wakatime-cli/releases/download/v1.106.1/wakatime-cli-darwin-{arch}.zip"
    elif system =="linux":
        url = "https://github.com/wakatime/wakatime-cli/releases/download/v1.106.1/wakatime-cli-linux-{arch}.zip"
    else:
        ui.messageBox("Failed to download The Wakatime CLI")
        raise OSError("Unsupported platform")
    try:
        response = requests.get(url)
        response.raise_for_status()

        with zipfile.Zipfile(bytesIO(response.content)) as zip_file:
            zip_file.extractall(os.path.dirname(get_wakatime_path()))
    except Exception as e:
        print(f"Failed to download WakaTime CLI: {e}")
    

    if platform.system() != "Windows":
    wakatime_cli_path = get_wakatime_path()
    os.chmod(wakatime_cli_path, 0o755)  # Set executable permissions
def  get_active_file_path():
    try:
        app = adsk.core.Application.get()
        if not app:
            raise Exception("No active file found")
        file = app.activeDocument
        if not file:
            raise Exception("No active file found")
            return file.dataFile.path
    except Exception as e:
        print(f"Error retrieving the file path: {e}")
        return None
def get_project_folder():
    file_path = get_active_file_path
    if file_path: 
        
        folder_path = os.path.dirname(file_path)
        project_name= os.path.basename(folder_path)
        return project_name
    else:
        print("No active file or file not saved locally.")
        return None
def send_data_to_wakatime():
    project_name = get_project_folder
    if not project_name:
        print("Failed to find project folder name")

# globals
ST_VERSION = int(sublime.version())
HOME_FOLDER = os.path.realpath(os.environ.get('WAKATIME_HOME') or os.path.expanduser('~'))
RESOURCES_FOLDER = os.path.join(HOME_FOLDER, '.wakatime')
CONFIG_FILE = os.path.join(HOME_FOLDER, '.wakatime.cfg')
INTERNAL_CONFIG_FILE = os.path.join(HOME_FOLDER, '.wakatime-internal.cfg')
GITHUB_RELEASES_STABLE_URL = 'https://api.github.com/repos/wakatime/wakatime-cli/releases/latest'
GITHUB_DOWNLOAD_PREFIX = 'https://github.com/wakatime/wakatime-cli/releases/download'
SETTINGS_FILE = 'WakaTime.sublime-settings'
SETTINGS = {}
LAST_HEARTBEAT = {
    'time': 0,
    'file': None,
    'is_write': False,
}
LAST_HEARTBEAT_SENT_AT = 0
LAST_FETCH_TODAY_CODING_TIME = 0
FETCH_TODAY_DEBOUNCE_COUNTER = 0
FETCH_TODAY_DEBOUNCE_SECONDS = 60
LATEST_CLI_VERSION = None
WAKATIME_CLI_LOCATION = None
HEARTBEATS = queue.Queue()
HEARTBEAT_FREQUENCY = 2  # minutes between logging heartbeat when editing same file
SEND_BUFFER_SECONDS = 30  # seconds between sending buffered heartbeats to API








def update_status_bar(status=None, debounced=False, msg=None):
    global LAST_FETCH_TODAY_CODING_TIME, FETCH_TODAY_DEBOUNCE_COUNTER 
    try:
        if not msg and SETTINGS.get('status_bar_mesage') is not false and SETTINGS.get('status_bar_enabled'):
            if SETTINGS.get('status_bar_code_activity' and status == 'OK'):
                if debounced:
                    FETCH_TODAY_DEBOUNCE_COUNTER -= 1
                if debounced or not LAST_FETCH_TODAY_CODING_TIME:
                    now = int(time.time())
                    if LAST_FETCH_TODAY_CODING_TIME and (FETCH_TODAY_DEBOUNCE_COUNTER > 0 or LAST_FETCH_TODAY_CODING_TIME > now - FETCH_TODAY_DEBOUNCE_SECONDS):
                        return
                else:
                    LAST_FETCH_TODAY_CODING_TIME += 1
                    set_timeout(lambda: update_status_bar(status, debounced=True, FETCH_TODAY_DEBOUNCE_SECONDS))
                    return
            else:
                msg = "Wakatime: {status}".format(status=status)  
        if msg:
            ui.messageBox(msg)
    except RuntimeError:
        set_timeout(lambda: update_status_bar(status=status, debounced=debounced, msg=msg), 0)

class UpdateCLI(threading.Thread):

    def run(self):
        if CLiLatest:
            return
        log(INFO, "Downloading latest wakatime CLI")

        if os.path.isdir(os.path.join(RESOURCES_FOLDER, "wakatime-cli")):
            shutil.rmtree(os.path.join(RESOURCES_FOLDER, "wakatime-cli"))
        if not os.path.exists(RESOURCES_FOLDER):
            os.makedirs(RESOURCES_FOLDER)
        try:
            url = GetCliDownloadURL()
            ui.messageBox(f"Downloading wakatime-cli from {ur}")
            zip_file = os.path.join(RESOURCES_FOLDER, "wakatime-cli.zip")
            download(url, zip_file)


            if CliInstalled():
                try: 
                    os.remove(getCliLocation())
            ui.messageBox("Extracting wakatime-cli...")
            with ZipFile(zip_file) as zf:
                zf.extractAll(RESOURCES_FOLDER)
            if not is_win:
                os.chmod(getCliLocation(), 509)
            try:
                os.remove(os.path.join(RESOURCES_FOLDER, "wakatime-cli.zip"))
            except:
                log(DEBUG, traceback.format_exc())     
        except:
            log(DEBUG, traceback.format_exc())
        createSymLink()
        ui.messageBox("Finished excracting wakatime-cli")
def getCliLocation:
    global WAKATIME_CLI_LOCATION

    if not WAKATIME_CLI_LOCATION:
        binary = 'wakatime-cli-{osname}-{arch}{ext}'.format(
            osname=platform.system().lower(),
            arch=architecture(),
            ext='.exe' if is_win else '',
        )
        WAKATIME_CLI_LOCATION = os.path.join(RESOURCES_FOLDER, binary)

    return WAKATIME_CLI_LOCATION

def architecture():
    arch = platform.machine() or platform.processor()
     if arch == 'armv7l':
        return 'arm'
    if arch == 'aarch64':
        return 'arm64'
    if 'arm' in arch:
        return 'arm64' if sys.maxsize > 2**32 else 'arm'
    return 'amd64' if sys.maxsize > 2**32 else '386'

def isCliInstalled():
    return os.path.exists(getCliLocation())

def isCliLatest():
 
    if not isCliLatest:
        return false
     args = [getCliLocation(), '--version']
    try:
        stdout, stderr = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
    except:
        return False
    stdout = (stdout or b'') + (stderr or b'')
    localVer = extractVersion(stdout.decode('utf-8'))
    if not localVer:
        log(DEBUG, 'Local wakatime-cli version not found.')
        return False

    log(INFO, 'Current wakatime-cli version is %s' % localVer)
    log(INFO, 'Checking for updates to wakatime-cli...')

    remoteVer = getLatestCliVersion()

    if not remoteVer:
        return True

    if remoteVer == localVer:
        log(INFO, 'wakatime-cli is up to date.')
        return True

    log(INFO, 'Found an updated wakatime-cli %s' % remoteVer)
    return False
def getLatestCliVersion():
    global LATEST_CLI_VERSION

    if LATEST_CLI_version:
        return LATEST_CLI_VERSION
    configs = None
    last_version = None
    last_modified = None

    try: 
        configs = parseConfigFile( INTERNAL_CONFIG_FILE)
        if configs:
            last_modified, last_version = lasstModifiedVersion(configs)

    except:
        log(DEBUG, traceback.format_exc())
    try:
        headers, contents, code = request(GITHUB_RELEASES_STABLE_URL, last_modified = last_modified)
        if code == 304:
            LATEST_CLI_VERSION = last_version
            return last_version
        data = json.loads(contents.decode('utf-8'))
        ver = data['tag_name']  
        if configs:
            last_modified = headers.get('last-modified')
            if not configs.has_section('internal'):
                configs.add_section('internal')
            configs.set('internal', 'cli_version', ver)
            config.set('internal', 'cli_version_last_modified', last_modified)