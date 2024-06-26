from controllers.login import LoginController
import sentry_sdk
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def handle_keyboard_interrupt(func):
    try:
        func()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)

dsn = os.environ.get('DSN')

if __name__ == "__main__":

    sentry_sdk.init(
        dsn=dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

    def main_program():

        login_controller = LoginController()
        login_controller.login()

    handle_keyboard_interrupt(main_program)