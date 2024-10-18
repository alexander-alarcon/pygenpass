import string
from random import choices, shuffle
from typing import LiteralString

from pygenpass.args import PasswordOptions
from pygenpass.errors import GeneratingPasswordError


def generate_password(options: PasswordOptions) -> str:
    """
    Generates a password with the specified options.

    Args:
        options (PasswordOptions): Options for generating the password.

    Returns:
        str: Generated password.
    """
    chars = ""
    required_chars = []

    if options.all and (options.letters or options.digits or options.special_chars):
        raise GeneratingPasswordError(
            "Error: --all cannot be used with --letters, --digits, or --special-chars."
        )

    if options.all:
        required_chars.append(choices(string.ascii_letters, k=1)[0])
        required_chars.append(choices(string.digits, k=1)[0])
        required_chars.append(choices(string.punctuation, k=1)[0])

        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        if options.letters:
            chars += string.ascii_letters
            required_chars.append(choices(string.ascii_letters, k=1)[0])
        if options.digits:
            chars += string.digits
            required_chars.append(choices(string.digits, k=1)[0])
        if options.special_chars:
            chars += string.punctuation
            required_chars.append(choices(string.punctuation, k=1)[0])

        if not chars:
            raise GeneratingPasswordError(
                "At least one of --all, --letters, --digits, or --special-chars must be specified."
            )

    if len(chars) < 1:
        raise GeneratingPasswordError(
            "Error: No characters available for password generation."
        )

    if options.length > len(required_chars):
        password = required_chars + choices(
            chars, k=options.length - len(required_chars)
        )
    else:
        password = required_chars[: options.length]

    password = required_chars + choices(chars, k=options.length - len(required_chars))
    shuffle(password)

    return "".join(password)
