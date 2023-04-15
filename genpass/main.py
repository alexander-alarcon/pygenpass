#!/usr/bin/env python3

import string
from argparse import ArgumentParser, Namespace
from random import choices
from typing import LiteralString, NamedTuple

import pyperclip
from attr import dataclass


@dataclass
class PasswordOptions:
    all: bool
    length: int = 16
    letters: bool = False
    digits: bool = False
    special_chars: bool = False


class Args(NamedTuple):
    copy_to_clipboard: bool
    password_options: PasswordOptions


class ArgsParsingError(Exception):
    pass


class GeneratingPasswordError(Exception):
    pass


def read_args() -> Args:
    parser = ArgumentParser(description="Generate password")
    parser.add_argument(
        "-l", "--length", type=int, default=16, help="Desired password length"
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="Include letters, digits and special characters in the password",
    )
    parser.add_argument(
        "-L",
        "--letters",
        action="store_true",
        default=False,
        help="Include letters in the password",
    )
    parser.add_argument(
        "-d",
        "--digits",
        action="store_true",
        default=False,
        help="Include digits in the password",
    )
    parser.add_argument(
        "-s",
        "--special-chars",
        action="store_true",
        default=False,
        help="Include special characters in the password",
    )
    parser.add_argument(
        "-c",
        "--copy-to-clipboard",
        default=False,
        help="Copy output to clipboard",
        action="store_true",
    )
    args: Namespace = parser.parse_args()

    if args.all and (args.letters or args.digits or args.special_chars):
        raise ArgsParsingError(
            "Error: The --all flag cannot be combined with --letters, --digits or --special-chars"
        )

    if not args.all and not (args.letters or args.digits or args.special_chars):
        args.all = True

    if args.length < 8:
        raise ArgsParsingError("Error: Password length must be at least 8 characters")

    return Args(
        password_options=PasswordOptions(
            all=args.all,
            length=args.length,
            letters=args.letters,
            digits=args.digits,
            special_chars=args.special_chars,
        ),
        copy_to_clipboard=args.copy_to_clipboard,
    )


def generate_password(options: PasswordOptions) -> str:
    chars: LiteralString = ""
    if options.all:
        if options.letters or options.digits or options.special_chars:
            raise GeneratingPasswordError(
                "Error: The --all flag cannot be combined with --letters, --digits or --special-chars"
            )
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        if options.letters:
            chars += string.ascii_letters
        if options.digits:
            chars += string.digits
        if options.special_chars:
            chars += string.punctuation

        if not chars:
            raise GeneratingPasswordError(
                "Error: At least one of --all, --letters, --digits or --special-chars must be specified"
            )

    return "".join(choices(chars, k=options.length))


def main() -> None:
    try:
        args: Args = read_args()
        password: str = generate_password(options=args.password_options)
        if args.copy_to_clipboard:
            pyperclip.copy(password)
            print("Password was copied to clipboard...")
        else:
            print(password)
    except ArgsParsingError as e:
        print(str(e))
    except GeneratingPasswordError as e:
        print(str(e))


if __name__ == "__main__":
    main()
