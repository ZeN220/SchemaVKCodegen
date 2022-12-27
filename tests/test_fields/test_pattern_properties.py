import pytest

from src.fields import IntegerField, PatternField, StringField

# For testing, need to create a fake class to use as the pattern properties
MINIMUM_DATA: dict = {
    "name": "test_name",
    "type": "object",
    "patternProperties": {"this_is_regexp": StringField(name="test_name", type="string")},
    "additionalProperties": False,
}

DEFAULT_DESCRIPTION = (
    "\n    Patterns of dict (as regexp) in the form of key-value:\n    this_is_regexp: str\n"
)


class TestPatterField:
    @pytest.mark.parametrize(
        "data, expected",
        [
            (
                MINIMUM_DATA,
                f"    test_name: typing.Optional[dict[str, str]] = None\n"
                f'    """{DEFAULT_DESCRIPTION}    """\n',
            ),
            (
                {**MINIMUM_DATA, "required": True},
                f"    test_name: dict[str, str]\n" f'    """{DEFAULT_DESCRIPTION}    """\n',
            ),
            (
                {**MINIMUM_DATA, "description": "Test description"},
                f"    test_name: typing.Optional[dict[str, str]] = None\n"
                f'    """\n    Test description{DEFAULT_DESCRIPTION}    """\n',
            ),
            (
                {
                    **MINIMUM_DATA,
                    "patternProperties": {
                        "this_is_regexp": StringField(name="test_name", type="string"),
                        "this_is_regexp2": IntegerField(name="test_name2", type="integer"),
                    },
                },
                f"    test_name: typing.Optional[dict[str, typing.Union[str, int]]] = None\n"
                f'    """{DEFAULT_DESCRIPTION}    this_is_regexp2: int\n    """\n',
            ),
        ],
    )
    def test_to_field_class(self, data: dict, expected: str):
        field = PatternField(**data)
        assert field.to_field_class() == expected