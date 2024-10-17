from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import NamedTuple

from pygenpass.errors import ArgsParsingError


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


def read_args() -> Args:
    parser = ArgumentParser(description="Generate password")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Set the password length (default: 16).",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="Include letters, digits and special characters.",
    )
    parser.add_argument(
        "-L",
        "--letters",
        action="store_true",
        default=False,
        help="Include letters in the password.",
    )
    parser.add_argument(
        "-d",
        "--digits",
        action="store_true",
        default=False,
        help="Include digits in the password.",
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
        help="Copy the generated password to the clipboard.",
        action="store_true",
    )
    args: Namespace = parser.parse_args()

    if args.all and (args.letters or args.digits or args.special_chars):
        raise ArgsParsingError(
            "Error: The --all flag cannot be used with --letters, --digits, or --special-chars."
        )

    if not args.all and not (args.letters or args.digits or args.special_chars):
        args.all = True

    if args.length < 8:
        raise ArgsParsingError(
            "Error: Password length must be at least 8 characters. Please choose a longer length."
        )

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
