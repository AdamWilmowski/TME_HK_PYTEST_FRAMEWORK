import sqlite3


class SQLFunctions:
    def __init__(self):
        self.sql = sqlite3.connect('TMEHK.db')
        self.cursor = self.sql.cursor()

    def getEmailValue(self):
        self.cursor.execute("SELECT value FROM used_values WHERE parameter='email';")
        email_value = self.cursor.fetchone()[0]
        self.cursor.execute(f"UPDATE used_values SET value = {email_value + 1}")
        self.sql.commit()
        return email_value

    def inputCustomerData(self, _id, company_name, email, company_phone, company_city, company_street, company_zip,
                          customer_job, customer_phone, customer_name, customer_surname, version):
        insert_query = "INSERT INTO customers (id, company_name, email, company_phone, company_city, " \
                       "company_street, company_zip, customer_job, customer_phone, customer_name, " \
                       "customer_surname, version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        self.cursor.execute(insert_query, (_id, company_name, email, company_phone, company_city, company_street,
                                      company_zip, customer_job, customer_phone, customer_name,
                                      customer_surname, version))
        insert_flag_query = "INSERT INTO customers_flags (id) VALUES (?);"
        self.cursor.execute(insert_flag_query, (_id,))

        self.sql.commit()

    def inputOrderData(self, email, sap_number, ecom_number, total, date, db_version, registered_user):
        insert_query = "INSERT INTO orders (email, sap_number, ecom_number, total, date, db_version, registered_user) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?);"
        self.cursor.execute(insert_query, (email, sap_number, ecom_number, total, date, db_version, registered_user))
        self.sql.commit()

    def getRandomCustomerEmail(self, version):
        self.cursor.execute(f"SELECT customers.email FROM customers LEFT JOIN customers_flags ON"
                       f" customers.id = customers_flags.id WHERE customers.version='{version}' "
                       f"AND customers_flags.password = 0 ORDER BY random()")
        email = self.cursor.fetchone()[0]
        return email

    def getCustomerData(self, data, column, search_by):
        self.cursor.execute(f"SELECT {data} FROM customers WHERE {column}='{search_by}'")
        record = self.cursor.fetchone()[0]
        return record

    def changeCustomerFlag(self, flag, index, value):
        if not isinstance(value, bool):
            raise TypeError("The argument must be a boolean value")
        if value:
            update_query = f"UPDATE customers_flags SET {flag} = {1} where id = {index}"
        else:
            update_query = f"UPDATE customers_flags SET {flag} = {0} where id = {index}"
        self.cursor.execute(update_query)
        self.sql.commit()

    def close(self):
        self.sql.close()
