import pytest
from pytest import MonkeyPatch

from pygenpass.args import Args, PasswordOptions, read_args
from pygenpass.errors import ArgsParsingError


class TestReadArgs:
    def test_read_args_default_values(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test case 1: all flags are off, length is default, should set all to True
        """
        monkeypatch.setattr("sys.argv", ["genpass"])
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        args: Args = read_args()
        expected_args: Args = Args(
            password_options=PasswordOptions(
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
        with pytest.raises(ArgsParsingError) as err_info:
            _: Args = read_args()
        assert (
            str(err_info.value)
            == "[ArgsParsingError]: Password length must be at least 8 characters. Please choose a longer length."
        )

    @pytest.mark.parametrize("option", ["-L", "-d", "-s"])
    def test_read_args_all_combinations(
        self, monkeypatch: MonkeyPatch, option: str
    ) -> None:
        """
        Test case 8: if -a is set -L, -d or -s cannot be set
        """
        monkeypatch.setattr("sys.argv", ["genpass", "-a", option])
        with pytest.raises(ArgsParsingError) as err_info:
            _: Args = read_args()
        assert (
            str(err_info.value)
            == "[ArgsParsingError]: The --all flag cannot be used with --letters, --digits, or --special-chars."
        )
