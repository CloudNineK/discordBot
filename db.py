import sqlite3 as lite


async def userInsert(uName: str, rName: str):

    con = lite.connect('user.db')

    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO Members VALUES('%s', '%s')" % (uName, rName))
    pass


async def tableGet(table: str):
    con = lite.connect('user.db')

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM %s" % table)

        rows = cur.fetchall()

        entries = {}
        for row in rows:
            entries[row[0]] = row[1]

        return entries


def display(table: str):
    con = lite.connect('user.db')

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM %s" % table)

        rows = cur.fetchall()

        for row in rows:
            print(row)
            print(type(row))


if __name__ == "__main__":
    display('Members')
