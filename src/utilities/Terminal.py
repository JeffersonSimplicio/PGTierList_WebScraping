from os import name, system


class Terminal:
    @staticmethod
    def clear():
        os_name = name
        print(os_name)

        if os_name == 'posix':  # Unix (Linux, macOS)
            system('clear')
        elif os_name == 'nt':  # Windows
            system('cls')
        else:
            print(
                "Terminal cleanup is not supported.."
            )
