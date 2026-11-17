import logging

def configurar_logger(ficheiro_log: str = "marina_audit.log") -> logging.Logger:
    """Configura o sistema de auditoria em ficheiro de texto."""
    logger = logging.getLogger("MarinaAudit")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(ficheiro_log, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    