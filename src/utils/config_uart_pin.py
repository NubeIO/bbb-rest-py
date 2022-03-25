from src.utils.shell import execute_command

UART_PINS = ['p9.26', 'p9.24', 'p9.11', 'p9.13']


def config_uart_pin() -> bool:
    for uart_pin in UART_PINS:
        if not execute_command(f'config-pin {uart_pin} uart'):
            return False
    return True
