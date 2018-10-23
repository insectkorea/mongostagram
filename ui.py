def on_start():
    print("")
    print("-" * 100)


def on_end():
    input("\nPress Enter to go back...")


def handle_error(message):
    print(message)
    on_end()

def handle_follow_error(message):
    print(message)

try:
    import msvcrt
    def getkey():
        return msvcrt.getch()

except ImportError:
    import sys
    import tty
    import termios

    def getkey():
        fd = sys.stdin.fileno()
        original_attributes = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
        return ch

