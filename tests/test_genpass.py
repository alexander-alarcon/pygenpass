import string

import pyperclip
import pytest
from pytest import MonkeyPatch

import pygenpass.main as m


class TestReadArgs:
    def test_read_args_default_values(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 1: all flags are off, length is default, should set all to True
        """
        monkeypatch.setattr("sys.argv", ["genpass"])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=16, letters=False, digits=False, special_chars=False, all=True
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    def test_read_args_only_all_flag(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 2: only --all flag is on
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-a"])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=16, letters=False, digits=False, special_chars=False, all=True
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    def test_read_args_only_letters_flag(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 3: only --letters flag is on
        """
        monkeypatch.setattr("sys.argv", ["genpass", "--letters"])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=16, letters=True, digits=False, special_chars=False, all=False
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    def test_read_args_only_digits_flag(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 4: only --digits flag is on
        """
        monkeypatch.setattr("sys.argv", ["genpass", "--digits"])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=16, letters=False, digits=True, special_chars=False, all=False
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    def test_read_args_only_special_chars_flag(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 5: only --special-chars flag is on
        """
        monkeypatch.setattr("sys.argv", ["genpass", "--special-chars"])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=16, letters=False, digits=False, special_chars=True, all=False
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    @pytest.mark.parametrize("length", ["10", "9", "12", "8", "11"])
    def test_read_args_length_is_10(
        self, monkeypatch: MonkeyPatch, length: str
    ) -> None:
        """
        Test case 6: -l is set to 10
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-l", length])
        args: m.Args = m.read_args()
        expected_args: m.Args = m.Args(
            password_options=m.PasswordOptions(
                length=int(length),
                letters=False,
                digits=False,
                special_chars=False,
                all=True,
            ),
            copy_to_clipboard=False,
        )
        assert args == expected_args

    @pytest.mark.parametrize("invalid_length", ["0", "-1", "7", "-8", "-16"])
    def test_read_args_length_raise_exception(
        self, monkeypatch: MonkeyPatch, invalid_length: str
    ) -> None:
        """
        Test case 7: -l is set to 5 and should raise exception
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-l", invalid_length])
        with pytest.raises(m.ArgsParsingError) as err_info:
            args: m.Args = m.read_args()
        assert (
            str(err_info.value)
            == "Error: Password length must be at least 8 characters"
        )

    @pytest.mark.parametrize("option", ["-L", "-d", "-s"])
    def test_read_args_all_combinations(
        self, monkeypatch: MonkeyPatch, option: str
    ) -> None:
        """
        Test case 8: if -a is set -L, -d or -s cannot be set
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-a", option])
        with pytest.raises(m.ArgsParsingError) as err_info:
            args: m.Args = m.read_args()
        assert (
            str(err_info.value)
            == "Error: The --all flag cannot be combined with --letters, --digits or --special-chars"
        )


class TestGeneratePassword:
    @pytest.mark.parametrize("length", [19, 24, 25, 15, 16, 30, 31, 27, 18, 20])
    def test_generate_password_all_characters(self, length: int) -> None:
        """
        Test case 1: Should create a password with n characters and contain all character options
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=length, all=True, letters=False, digits=False, special_chars=False
        )
        password: str = m.generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(
            set(string.ascii_letters + string.digits + string.punctuation)
        )

    @pytest.mark.parametrize("length", [15, 19, 21, 23, 24, 25, 26, 28, 29, 30])
    def test_generate_password_just_letters(self, length: int) -> None:
        """
        Test case 2: Should create a password with n characters and contain just letters uppercase or lowercase
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=length, all=False, letters=True, digits=False, special_chars=False
        )
        password: str = m.generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.ascii_letters))

    @pytest.mark.parametrize("length", [18, 17, 21, 15, 16, 10, 24, 23, 11, 20])
    def test_generate_password_just_digits(self, length: int) -> None:
        """
        Test case 3: Should create a password with n characters and contain just digits
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=length, all=False, letters=False, digits=True, special_chars=False
        )
        password: str = m.generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.digits))

    @pytest.mark.parametrize("length", [15, 16, 17, 22, 25, 26, 27, 28, 29, 30])
    def test_generate_password_just_special_characters(self, length: int) -> None:
        """
        Test case 4: Should create a password with n characters and contain just special character
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=length, all=False, letters=False, digits=False, special_chars=True
        )
        password: str = m.generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.punctuation))

    @pytest.mark.parametrize("length", [16, 17, 21, 23, 27, 28, 32, 34, 40, 50])
    def test_generate_password_letters_and_special_characters(
        self, length: int
    ) -> None:
        """
        Test case 5: Should create a password with n characters and contain letters and special characters
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=length, all=False, letters=True, digits=False, special_chars=True
        )
        password: str = m.generate_password(options=options)
        assert len(password) == length
        assert set(password).issubset(set(string.ascii_letters + string.punctuation))

    def test_generate_password_no_options(self) -> None:
        """
        Test case 6: Should raise an error if no options are passed
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=8, all=False, letters=False, digits=False, special_chars=False
        )
        with pytest.raises(m.GeneratingPasswordError):
            m.generate_password(options=options)

    def test_generate_password_invalid_options(self) -> None:
        """
        Test case 7: Should raise an error if invalid options are passed
        """
        options: m.PasswordOptions = m.PasswordOptions(
            length=8, all=True, letters=True, digits=True, special_chars=True
        )
        with pytest.raises(m.GeneratingPasswordError):
            m.generate_password(options=options)


class TestCopyToClipboard:
    def test_main_copy_to_clipboard(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 1: Should copy the generated password to clipboard
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-l", "12", "-c"])
        password = "r3nd0m_p@ssw0rd"
        with monkeypatch.context() as main:
            main.setattr("genpass.main.generate_password", lambda options: password)
            m.main()
            assert pyperclip.paste() == password
