import string
from random import choices
from typing import LiteralString

from pygenpass.args import PasswordOptions
from pygenpass.errors import GeneratingPasswordError


def generate_password(options: PasswordOptions) -> str:
    chars: LiteralString = ""
    if options.all:
        if options.letters or options.digits or options.special_chars:
            raise GeneratingPasswordError(
                "Error: The --all flag cannot be combined with --letters, --digits, or --special-chars."
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
                "Error: At least one of --all, --letters, --digits, or --special-chars must be specified. Please choose at least one."
            )

    return "".join(choices(chars, k=options.length))
