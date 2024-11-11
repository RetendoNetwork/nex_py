import logging
import os
import sys
import time
import inspect
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Log prefixes with colors
critical_prefix = "CRITICAL"
critical_prefix_colored = Fore.WHITE + Back.RED + Style.BRIGHT + critical_prefix

error_prefix = "ERROR"
error_prefix_colored = Fore.RED + Style.BRIGHT + error_prefix

warning_prefix = "WARNING"
warning_prefix_colored = Fore.YELLOW + Style.BRIGHT + warning_prefix

success_prefix = "SUCCESS"
success_prefix_colored = Fore.GREEN + Style.BRIGHT + success_prefix

info_prefix = "INFO"
info_prefix_colored = Fore.CYAN + Style.BRIGHT + info_prefix

log_template = "[{date}] [{prefix}] {func} {package} {file}:{line} : {message}"

max_prefix_length = len(critical_prefix)


def create_log_file(path):
    try:
        log_dir = os.path.dirname(path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return open(path, 'a')
    except Exception as e:
        print(f"Error creating log file: {e}")
        return None


def log_line(message, prefix, prefix_colored, log_file):
    date = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    frame = inspect.stack()[2]
    file = os.path.basename(frame[1])
    line = frame[2]
    func = frame[3]
    package = frame[0].f_globals["__name__"]

    prefix_length = len(prefix)
    spacing = " " * (max_prefix_length - prefix_length + 1)

    log_plain = log_template.format(date=date, prefix=prefix, func=func, package=package, file=file, line=line, message=message)
    log_plain_spaced = log_template.format(date=date, prefix=prefix, func=func, package=package, file=file, line=line, message=message)

    if colorama_supported():
        print(log_template.format(date=Fore.LIGHTBLACK_EX + date, prefix=prefix_colored, func=Fore.MAGENTA + "func " + Fore.CYAN + func, package=Fore.GREEN + package, file=Fore.GREEN + file, line=Fore.YELLOW + str(line), message=Style.BRIGHT + message))
    else:
        print(log_plain_spaced)

    log_file.write(log_plain + '\n')
    log_file.flush()


def colorama_supported():
    try:
        return sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'
    except Exception:
        return False


def critical(message):
    log_line(message, critical_prefix, critical_prefix_colored, critical_log_file)


def error(message):
    log_line(message, error_prefix, error_prefix_colored, error_log_file)


def warning(message):
    log_line(message, warning_prefix, warning_prefix_colored, warning_log_file)


def success(message):
    log_line(message, success_prefix, success_prefix_colored, success_log_file)


def info(message):
    log_line(message, info_prefix, info_prefix_colored, info_log_file)


def criticalf(message, *args):
    log_line(message % args, critical_prefix, critical_prefix_colored, critical_log_file)


def errorf(message, *args):
    log_line(message % args, error_prefix, error_prefix_colored, error_log_file)


def warningf(message, *args):
    log_line(message % args, warning_prefix, warning_prefix_colored, warning_log_file)


def successf(message, *args):
    log_line(message % args, success_prefix, success_prefix_colored, success_log_file)


def infof(message, *args):
    log_line(message % args, info_prefix, info_prefix_colored, info_log_file)

# Log files setup
log_folder_root = "."
log_folder_path = os.path.join(log_folder_root, "log")
log_flags = os.O_APPEND | os.O_CREATE | os.O_WRONLY

all_log_file = create_log_file(os.path.join(log_folder_path, "all.log"))
critical_log_file = create_log_file(os.path.join(log_folder_path, "critical.log"))
error_log_file = create_log_file(os.path.join(log_folder_path, "error.log"))
warning_log_file = create_log_file(os.path.join(log_folder_path, "warning.log"))
success_log_file = create_log_file(os.path.join(log_folder_path, "success.log"))
info_log_file = create_log_file(os.path.join(log_folder_path, "info.log"))