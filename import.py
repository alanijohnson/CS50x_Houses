from sys import argv, exit
import csv
import sqlite3

# Method to parse the names in each line of the file
# Returns - tuple of first, middle, and last name. If user doesn't have middle name NULL is returned as a string
# Input - string with space separated first and last names
def parseName(name):
    firstSpaceloc = name.find(" ")
    firstName = name[:firstSpaceloc]
    if name.count(" ") >= 2:
        secondSpaceloc = name.find(" ", firstSpaceloc+1)
        middleName = name[firstSpaceloc+1:secondSpaceloc]
        lastName = name[secondSpaceloc+1:]
    else:
        middleName = "NULL"
        lastName = name[firstSpaceloc+1:]

    return (firstName, middleName, lastName)

def main(argv):

    # Ensure the user enters the right number of arguements
    if len(argv) != 2:
        print("Expecting two arguments. Program name and csv file")
        exit(0)

    # Open csv file and create database connection
    csvfile = argv[1]
    studentfile = open(csvfile)
    reader = csv.DictReader(studentfile)
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

   # Iterate through each line in the CSV file
    for line in reader:
        # Gather data from the line in CSV file
        house = line['house']
        birth = line['birth']
        name = line['name']
        # Parse the student's name using helper methods
        firstName, middleName, lastName = parseName(name)

        # Query the databse to ensure the entry doesn't already exist.
        # If the student doesn't exist, insert student into the database; otherwise print an error
        query = "SELECT * FROM students WHERE first = ? and middle = ? and last = ? and house = ? and birth = ?"
        c.execute(query,(firstName,middleName,lastName,house,birth))
        if c.fetchone() == None:
            query = "INSERT INTO students (first, middle, last, house, birth) VALUES (?,?,?,?,?)"
            c.execute(query,(firstName,middleName,lastName,house,birth))
            conn.commit()
        else:
            print("already in DB %s" % firstName)

    # Close file and terminate db connection
    studentfile.close()
    conn.close()

main(argv)