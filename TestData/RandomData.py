import random
import string
import names
import randomname

class RandomData:

    def get_random_value(self, length, value_type):
        if value_type == "string":
            letters = string.ascii_letters
            result_value = ''.join(random.choice(letters) for _ in range(length))
        elif value_type == "number":
            digits = string.digits
            result_value = ''.join(random.choice(digits) for _ in range(length))
        else:
            raise ValueError("Invalid type. Use 'string' or 'number'.")

        return result_value

    def get_name(self):
        return names.get_first_name()

    def get_surname(self):
        return names.get_last_name()

    def get_city(self):
        return randomname.generate('nm/cities/alpha')

    def get_street(self):
        street = (randomname.generate('nm/streets/chicago') + " " + str(random.randint(1, 100))).capitalize()
        return street

    def get_CompanyName(self):
        company_name = (randomname.generate('ip/corporate')).capitalize()
        return company_name


