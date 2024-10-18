#!/usr/bin/env python3


import pyperclip

from pygenpass.args import Args, read_args
from pygenpass.errors import ArgsParsingError, GeneratingPasswordError
from pygenpass.password import generate_password


def main() -> None:
    try:
        args: Args = read_args()
        password: str = generate_password(options=args.password_options)
        if args.copy_to_clipboard:
            pyperclip.copy(password)
            print("Password was copied to clipboard...")
        else:
            print(password)
    except (ArgsParsingError, GeneratingPasswordError) as e:
        print(str(e))


if __name__ == "__main__":
    main()
