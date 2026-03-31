import logging

def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:  # evita duplicar logs
        handler = logging.StreamHandler()

        formato = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(formato)

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger