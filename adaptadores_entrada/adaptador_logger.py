import logging



class AdaptadorLogger:

    def __init__(self):
        
        logging.basicConfig(
            filename='adaptador_logger.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Logger initialized successfully.")

    def log(self, endpoint, estado, resultado):
        logging.info(f" Endpoint: {endpoint}, Estado: {estado}, Resultado: {resultado}")
