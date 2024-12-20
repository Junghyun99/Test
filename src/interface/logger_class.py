import logging
import inspect
from logging.handlers import RotatingFileHandler


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # 호출 스택에서 실제 호출 위치 추출
        stack = inspect.stack()       
        for frame in stack:
            module_name = frame.frame.f_globals["__name__"]
            if not module_name.startswith("logging") and not module_name.startswith("src.interface.logger_class"):  # 로깅 모듈 제외
                record.caller_info = f"{module_name}:{frame.lineno}"
                break
        else:
            record.caller_info = "Unknown"

        return super().format(record)

class BaseLogger:
    def __init__(self, logger_name, log_file, level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        self.logger.setLevel(level)
        if not self.logger.hasHandlers():
            self._setup_handlers(log_file)

    def _setup_handlers(self, log_file):
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

        # 파일 핸들러
        file_handler = RotatingFileHandler(
    log_file, maxBytes=5*1024*1024, backupCount=3  # 5MB, 3개의 백업 파일
)
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

    def _get_formatter(self):
        return CustomFormatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s (호출위치: %(caller_info)s)')

    def get_logger(self):
        return self.logger

    def log(self, level, message, *args, **kwargs):
        if args:
            self.logger.log(level, message, *args, **kwargs)
        else:
            self.logger.log(level, message, **kwargs)

    def log_debug(self, message, *args):
        self.log(logging.DEBUG, message, *args)

    def log_info(self, message, *args):
        self.log(logging.INFO, message, *args)

    def log_warning(self, message, *args):
        self.log(logging.WARNING, message, *args)

    def log_error(self, message, *args):
        self.log(logging.ERROR, message, *args)
