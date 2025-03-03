import logging
import os
import sys
import traceback
import warnings

import transformers
from PySide6.QtGui import QImageReader
from PySide6.QtWidgets import QApplication, QMessageBox

from utils.settings import get_settings
from widgets.main_window import MainWindow

from loguru import logger

def custom_formatter(record):
    link = f"\033]8;;file://{record['file'].path}:{record['line']}\033\\{record['file'].name}:{record['line']}\033]8;;\033\\"
    return (
        # "<green>{time:HH:mm:ss}</green>|"
        "<level>{level:<5.5}</level>|"
        # for some loguru reason the space or pipe after the link
        # has to be there, or it throws an error
        f"<magenta>{link} |</magenta>"
        "<cyan>{message}</cyan>\n"
    )

filter_dict = {
    "": "DEBUG",
    "django": "INFO",
    # "nordigen_cli.apiclient.base": "TRACE",
}

# inspect(logger, methods=True)
logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    filter=filter_dict,
    level="TRACE",
    format=custom_formatter,
)

# try:
#     import pydevd_pycharm
#
#     pydevd_pycharm.settrace(
#         "localhost",
#         port=5678,  # Arbitrary, but remember it for later. Pick a port that is not in use.
#         stdoutToServer=True,
#         stderrToServer=True,
#         suspend=False,
#     )
# except Exception as exc:
#     logger.error(f"Failed to connect to python debug server")


def suppress_warnings():
    """Suppress all warnings when not in a development environment."""
    environment = os.getenv('TAGGUI_ENVIRONMENT')
    if environment == 'development':
        print('Running in development environment.')
        return
    logging.basicConfig(level=logging.WARN)
    warnings.simplefilter('ignore')
    transformers.logging.set_verbosity_error()
    try:
        import auto_gptq
        auto_gptq_logger = logging.getLogger(auto_gptq.modeling._base.__name__)
        auto_gptq_logger.setLevel(logging.ERROR)
    except ImportError:
        pass


def run_gui():
    app = QApplication([])
    # The application name is shown in the taskbar.
    app.setApplicationName('TagGUI')
    # The application display name is shown in the title bar.
    app.setApplicationDisplayName('TagGUI')
    app.setStyle('Fusion')
    # Disable the allocation limit to allow loading large images.
    QImageReader.setAllocationLimit(0)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # Suppress all warnings when not in a development environment.
    suppress_warnings()
    try:
        run_gui()
    except Exception as exception:
        settings = get_settings()
        settings.clear()
        error_message_box = QMessageBox()
        error_message_box.setWindowTitle('Error')
        error_message_box.setIcon(QMessageBox.Icon.Critical)
        error_message_box.setText(str(exception))
        error_message_box.setDetailedText(traceback.format_exc())
        error_message_box.exec()
        raise exception
