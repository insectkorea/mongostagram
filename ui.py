def on_start():
    print("")
    print("-" * 100)


def on_end():
    input("\nPress Enter to go back...")


def handle_error(message):
    print(message)
    on_end()
