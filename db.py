import mysql.connector
import re
def connect():
    # if the connection fails for some reason, an exception could be thrown,
    # which the function calling connect() must handle
    return mysql.connector.connect(host="127.0.0.1", port=3306,
                                   user='root', password='judelillico19*',
                                   database='ooplah',
                                   autocommit=True,
                                   use_pure=True,
                                   charset='utf8',
                                   collation='utf8_general_ci')


def query(sql, args=None):
    # sql is the query string, args is a tuple (which may or may not be used)
    # if args are used, then have to use a prepared statement for security
    try:
        conn = connect()
        cur, result = None, None
        if args is None:
            cur = conn.cursor()
            cur.execute(sql)
        else:
            # uses a prepared statement to protect against injection attacks
            cur = conn.cursor(prepared=True)
            cur.execute(sql, args)
        # select queries return a list, but the connector can return strings in text fields
        # as bytearrays, so they are converted to strings before returning results.
        # MySQLCursorPrepared has no fetchAll() so use a loop
        # Also, rows are tuples, so have to convert them to lists if changing values
        # SELECT could be in brackets, so regex checks for those
        if re.match("^\(*Select", sql, re.IGNORECASE) is not None:
            result = []
            for row in cur:
                r = []
                for field in row:
                    if type(field) is bytearray:
                        r.append(str(field))
                    else:
                        r.append(field)
                result.append(r)
        elif re.match("^Insert", sql, re.IGNORECASE) is not None:
            # inserted a new record, so return the new ID in case it's needed
            result = cur.lastrowid
        else:
            # update, delete - just need to know if it worked
            result = True
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        # return False to indicate that the query didn't work
        return False

def query_value(sql, args=None):
    # some select queries should only return a single value, but query above
    # always returns that single value in a 2D list, i.e. in result[0][0]
    # this function extracts the single value from result
    result = query(sql, args)
    if result and len(result) == 1:
        return result[0][0]
    else:
        return None

def query_row(sql, args=None):
    # some select queries should only return a single row, but query above
    # always returns that row in a 2D list, i.e. in result[0]
    # this function extracts the single row from result
    result = query(sql, args)
    if result and len(result) == 1:
        return result[0]
    else:
        return None

def query_column(sql, args=None):
    # some select queries should return the value in a single field
    # (column) for each matching row, in a 2D list of lists with
    # one element.  This query puts the values in a 1D list
    result = query(sql, args)
    if result and len(result) > 0:
        return [row[0] for row in result]
    else:
        return None
