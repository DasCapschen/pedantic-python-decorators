from datetime import datetime, timedelta
from typing import Union

from pedantic import overrides
from pedantic.decorators.fn_deco_validate.exceptions import ValidationError
from pedantic.decorators.fn_deco_validate.validators import Validator


class DateTimeUnixTimestamp(Validator):
    @overrides(Validator)
    def validate(self, value: Union[int, float, str]) -> datetime:
        if not isinstance(value, (int, float, str)):
            raise ValidationError(f'Invalid seconds since 1970: {value}')

        try:
            seconds = float(value)
        except ValueError:
            raise ValidationError(f'Could parse {value} to float.')

        return datetime(year=1970, month=1, day=1) + timedelta(seconds=seconds)
