import string

import pytest

from pygenpass.args import PasswordOptions
from pygenpass.errors import GeneratingPasswordError
from pygenpass.password import generate_password


class TestGeneratePassword:
    @pytest.mark.parametrize("length", [19, 24, 25, 15, 16, 30, 31, 27, 18, 20])
    def test_generate_password_all_characters(self, length: int) -> None:
        """
        Test case 1: Should create a password with n characters and contain all character options
        """
        options: PasswordOptions = PasswordOptions(
            length=length, all=True, letters=False, digits=False, special_chars=False
        )
        password: str = generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(
            set(string.ascii_letters + string.digits + string.punctuation)
        )
        assert any(c.isdigit() for c in password)
        assert any(c.isalpha() for c in password)
        assert any(c in string.punctuation for c in password)

    @pytest.mark.parametrize("length", [15, 19, 21, 23, 24, 25, 26, 28, 29, 30])
    def test_generate_password_just_letters(self, length: int) -> None:
        """
        Test case 2: Should create a password with n characters and contain just letters uppercase or lowercase
        """
        options: PasswordOptions = PasswordOptions(
            length=length, all=False, letters=True, digits=False, special_chars=False
        )
        password: str = generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.ascii_letters))
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert not any(c.isdigit() for c in password)
        assert not any(c in string.punctuation for c in password)

    @pytest.mark.parametrize("length", [18, 17, 21, 15, 16, 10, 24, 23, 11, 20])
    def test_generate_password_just_digits(self, length: int) -> None:
        """
        Test case 3: Should create a password with n characters and contain just digits
        """
        options: PasswordOptions = PasswordOptions(
            length=length, all=False, letters=False, digits=True, special_chars=False
        )
        password: str = generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.digits))
        assert any(c.isdigit() for c in password)
        assert not any(c.isalpha() for c in password)
        assert not any(c in string.punctuation for c in password)

    @pytest.mark.parametrize("length", [15, 16, 17, 22, 25, 26, 27, 28, 29, 30])
    def test_generate_password_just_special_characters(self, length: int) -> None:
        """
        Test case 4: Should create a password with n characters and contain just special character
        """
        options: PasswordOptions = PasswordOptions(
            length=length, all=False, letters=False, digits=False, special_chars=True
        )
        password: str = generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.punctuation))
        assert not any(c.isdigit() for c in password)
        assert not any(c.isalpha() for c in password)

    @pytest.mark.parametrize("length", [16, 17, 21, 23, 27, 28, 32, 34, 40, 50])
    def test_generate_password_letters_and_special_characters(
        self, length: int
    ) -> None:
        """
        Test case 5: Should create a password with n characters and contain letters and special characters
        """
        options: PasswordOptions = PasswordOptions(
            length=length, all=False, letters=True, digits=False, special_chars=True
        )
        password: str = generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.ascii_letters + string.punctuation))
        assert not any(c.isdigit() for c in password)

    def test_generate_password_no_options(self) -> None:
        """
        Test case 6: Should raise an error if no options are passed
        """
        options: PasswordOptions = PasswordOptions(
            length=8, all=False, letters=False, digits=False, special_chars=False
        )
        with pytest.raises(GeneratingPasswordError):
            generate_password(options=options)

    def test_generate_password_invalid_options(self) -> None:
        """
        Test case 7: Should raise an error if invalid options are passed
        """
        options: PasswordOptions = PasswordOptions(
            length=8, all=True, letters=True, digits=True, special_chars=True
        )
        with pytest.raises(GeneratingPasswordError):
            generate_password(options=options)
