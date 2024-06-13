from controllers.login import LoginController
import sys

def handle_keyboard_interrupt(func):
    try:
        func()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    def main_program():
        login_controller = LoginController()
        login_controller.login()

    handle_keyboard_interrupt(main_program)