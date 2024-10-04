from os import system, name
from src.utilities.terminal_styles import TerminalStyles


class Terminal:
    @staticmethod
    def clear():
        if name == "posix":  # Unix (Linux, macOS)
            system("clear")
        elif name == "nt":  # Windows
            system("cls")

    @staticmethod
    def success(message: str):
        """Exibe uma mensagem de sucesso em verde."""
        print(f"{TerminalStyles.GREEN}{message}{TerminalStyles.RESET}")

    @staticmethod
    def warning(message: str):
        """Exibe uma mensagem de aviso em amarelo."""
        print(f"{TerminalStyles.YELLOW}{message}{TerminalStyles.RESET}")

    @staticmethod
    def error(message: str):
        """Exibe uma mensagem de erro em vermelho."""
        print(f"{TerminalStyles.RED}{message}{TerminalStyles.RESET}")

    @staticmethod
    def info(message: str):
        """Exibe uma mensagem de informação em azul."""
        print(f"{TerminalStyles.BLUE}{message}{TerminalStyles.RESET}")

    @staticmethod
    def bold(message: str):
        """Exibe uma mensagem em negrito."""
        print(f"{TerminalStyles.BOLD}{message}{TerminalStyles.RESET}")

    @staticmethod
    def italic(message: str):
        """Exibe uma mensagem em itálico."""
        print(f"{TerminalStyles.ITALIC}{message}{TerminalStyles.RESET}")

    @staticmethod
    def underline(message: str):
        """Exibe uma mensagem sublinhada."""
        print(f"{TerminalStyles.UNDERLINE}{message}{TerminalStyles.RESET}")

    @staticmethod
    def _select_color(color: str):
        valid_colors = {
            "RED": TerminalStyles.RED,
            "GREEN": TerminalStyles.GREEN,
            "YELLOW": TerminalStyles.YELLOW,
            "BLUE": TerminalStyles.BLUE,
            "MAGENTA": TerminalStyles.MAGENTA,
            "CYAN": TerminalStyles.CYAN,
            "WHITE": TerminalStyles.WHITE,
        }

        if color is None:
            return None

        if color.upper() in valid_colors:
            return valid_colors[color.upper()]
        else:
            raise ValueError(
                f"Cor '{color}' inválida. "
                f"Escolha entre: {', '.join(valid_colors.keys())}"
            )

    @staticmethod
    def colored_message(message: str, color: str = None):
        """Permite ao usuário selecionar uma das cores disponíveis."""
        try:
            selected_color = Terminal._select_color(color)
            if selected_color:
                print(f"{selected_color}{message}{TerminalStyles.RESET}")
            else:
                print(message)
        except ValueError as e:
            print(f"{TerminalStyles.RED}Erro: {e}{TerminalStyles.RESET}")
