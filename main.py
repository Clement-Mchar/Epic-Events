from controllers.login import LoginController
import sentry_sdk
import sys
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def handle_keyboard_interrupt(func):
    # Handle KeyboardInterrupt (Ctrl+C) gracefully
    try:
        func()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)


# Get Sentry DSN from environment variables
dsn = os.environ.get("DSN")

if __name__ == "__main__":
    # Initialize Sentry SDK with the provided DSN
    sentry_sdk.init(
        dsn=dsn,
        # Set traces_sample_rate to capture 100% of transactions
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to profile 100% of sampled transactions
        profiles_sample_rate=1.0,
    )

    def main_program():
        # Create an instance of LoginController and call the login method
        login_controller = LoginController()
        login_controller.login()

    # Run the main program with keyboard interrupt handling
    handle_keyboard_interrupt(main_program)
