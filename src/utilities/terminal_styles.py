# Fonte:
# https://stackoverflow.com/questions/39473297/how-do-i-print-colored-output-with-python-3

class TerminalStyles:
    # Cores de texto
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Estilos de texto
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Reseta cor e estilo
    RESET = "\033[0m"
