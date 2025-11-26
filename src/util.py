class UserInputError(Exception):
    pass

def validate_year(year):
    if not isinstance(year, int) or year < 0:
        raise UserInputError("Year must be a positive integer.")
