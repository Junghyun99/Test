



# LoggerManager 인스턴스 생성
logger_manager = LoggerManager()

# SystemLogger와 TransactionLogger 가져오기
system_logger = logger_manager.get_logger('system')
transaction_logger = logger_manager.get_logger('transaction')

# 로그 메시지 기록
system_logger.info("This is an info message from the system logger.")
transaction_logger.error("This is an error message from the transaction logger.")

# 로그 레벨 변경
logger_manager.set_log_level('system', logging.DEBUG)
system_logger.debug("This debug message will now be shown since the log level is DEBUG.")