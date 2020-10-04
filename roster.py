# Program to query the database for the student roster

from sys import argv, exit
import sqlite3

def main(argv):
    # Ensure user entered the proper number of arguments to start program
    if len(argv) != 2:
        print("Expecting two arguments. Program name and name of house.")
        exit(0)

    house = argv[1]

    # Create db connection and query database
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    query = """SELECT first, middle, last, birth from students
                WHERE house = ?
                ORDER BY last, first"""

    c.execute(query, (house,)) # Parenthesis around house protect it from SQL injection

    # Print results formatted
    for row in c.fetchall():
        name = row[0]

        if row[1] != 'NULL':
            name = name + " " + row[1]

        name = name + " "+ row[2]
        print(name+", born",row[3])

main(argv)