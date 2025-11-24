class UserInputError(Exception):
    pass

def validate_year(year):
    if year < 0 or not isinstance(year, int):
        raise UserInputError("Vuoden tulee olla positiivinen kokonaisluku.")
