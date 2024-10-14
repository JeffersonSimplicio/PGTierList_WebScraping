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
    def _print_message(style, *args, sep=" ", end="\n"):
        """Exibe uma mensagem com o estilo fornecido."""
        message = sep.join(map(str, args))
        print(f"{style}{message}{TerminalStyles.RESET}", end=end)

    @staticmethod
    def default(*args, sep=" ", end="\n"):
        """Simula o comportamento do print sem personalizações."""
        print(sep.join(map(str, args)), end=end)

    @staticmethod
    def success(*args, sep=" ", end="\n"):
        """Exibe uma mensagem de sucesso em verde."""
        Terminal._print_message(TerminalStyles.GREEN, *args, sep=sep, end=end)

    @staticmethod
    def warning(*args, sep=" ", end="\n"):
        """Exibe uma mensagem de aviso em amarelo."""
        Terminal._print_message(TerminalStyles.YELLOW, *args, sep=sep, end=end)

    @staticmethod
    def error(*args, sep=" ", end="\n"):
        """Exibe uma mensagem de erro em vermelho."""
        Terminal._print_message(TerminalStyles.RED, *args, sep=sep, end=end)

    @staticmethod
    def info(*args, sep=" ", end="\n"):
        """Exibe uma mensagem de informação em azul."""
        Terminal._print_message(TerminalStyles.BLUE, *args, sep=sep, end=end)

    @staticmethod
    def bold(*args, sep=" ", end="\n"):
        """Exibe uma mensagem em negrito."""
        Terminal._print_message(TerminalStyles.BOLD, *args, sep=sep, end=end)

    @staticmethod
    def italic(*args, sep=" ", end="\n"):
        """Exibe uma mensagem em itálico."""
        Terminal._print_message(TerminalStyles.ITALIC, *args, sep=sep, end=end)

    @staticmethod
    def underline(*args, sep=" ", end="\n"):
        """Exibe uma mensagem sublinhada."""
        Terminal._print_message(
            TerminalStyles.UNDERLINE,
            *args,
            sep=sep,
            end=end
        )

    @staticmethod
    def colored_message(*args, color: str = None, sep=" ", end="\n"):
        """Permite ao usuário selecionar uma das cores disponíveis."""
        try:
            message = sep.join(map(str, args))
            selected_color = Terminal._select_color(color)
            if selected_color:
                print(
                    f"{selected_color}{message}{TerminalStyles.RESET}",
                    end=end
                )
            else:
                print(message, end=end)
        except ValueError as e:
            print(f"{TerminalStyles.RED}Erro: {e}{TerminalStyles.RESET}")

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
