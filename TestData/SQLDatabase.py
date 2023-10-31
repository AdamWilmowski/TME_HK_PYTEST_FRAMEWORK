import sqlite3


class SQLFunctions:

    def getEmailValue(self):
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        cursor.execute("SELECT value FROM used_values WHERE parameter='email';")
        email_value = cursor.fetchone()[0]
        cursor.execute(f"UPDATE used_values SET value = {email_value + 1}")
        sql.commit()
        sql.close()
        return email_value

    def inputCustomerData(self, _id, company_name, email, company_phone, company_city, company_street, company_zip,
                          customer_job, customer_phone, customer_name, customer_surname, version):
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        insert_query = "INSERT INTO customers (id, company_name, email, company_phone, company_city, " \
                       "company_street, company_zip, customer_job, customer_phone, customer_name, " \
                       "customer_surname, version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(insert_query, (_id, company_name, email, company_phone, company_city, company_street,
                                      company_zip, customer_job, customer_phone, customer_name,
                                      customer_surname, version))
        insert_flag_query = "INSERT INTO customers_flags (id) VALUES (?);"
        cursor.execute(insert_flag_query, (_id,))

        sql.commit()
        sql.close()

    def inputOrderData(self, email, sap_number, ecom_number, total, date, db_version, registered_user):
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        insert_query = "INSERT INTO orders (email, sap_number, ecom_number, total, date, db_version, registered_user) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(insert_query, (email, sap_number, ecom_number, total, date, db_version, registered_user))
        sql.commit()
        sql.close()

    def getRandomCustomerEmail(self, version):
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        cursor.execute(f"SELECT customers.email FROM customers LEFT JOIN customers_flags ON"
                       f" customers.id = customers_flags.id WHERE customers.version='{version}' "
                       f"AND customers_flags.password = 0 ORDER BY random()")
        email = cursor.fetchone()[0]
        sql.close()
        return email

    def getCustomerData(self, data, column, search_by):
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        cursor.execute(f"SELECT {data} FROM customers WHERE {column}='{search_by}'")
        record = cursor.fetchone()[0]
        sql.close()
        return record

    def changeCustomerFlag(self, flag, index, value):
        if not isinstance(value, bool):
            raise TypeError("The argument must be a boolean value")
        sql = sqlite3.connect('TMEHK.db')
        cursor = sql.cursor()
        if value:
            update_query = f"UPDATE customers_flags SET {flag} = {1} where id = {index}"
        else:
            update_query = f"UPDATE customers_flags SET {flag} = {0} where id = {index}"
        cursor.execute(update_query)
        sql.commit()
        sql.close()
