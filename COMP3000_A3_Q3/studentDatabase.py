
# inport the required libraries
#psycopg2 is a postgresql database adapter specifically for python
import psycopg2

# create a function that establishes a connection to the database
def create_connection():
    
    try:
        # connect to the database using the psycopg2.connect() method
        # the method takes in the following parameters: 
        #*update password*
        connection = psycopg2.connect( user="postgres", password="XXXX",
            host="localhost",
            port="5432",
            database="StudentDB"
        )
        # return the connection
        return connection
    # if error occurs assign it to the variable 'e
    #except Error as e:
    except:
        print("Unable to connect to the database")
        return None

# function that retrieves all the students from the database
def getAllStudents(connection):
    try:
        #cursor is a connection method used to execute the sql commands
        #store it in the variable query
        query= connection.cursor()

        #execute is method used to execute the sql commands
        # select all the students from the students table
        query.execute("SELECT * FROM students;")

        #fetchall is used to  get all the rows from the table
        students = query.fetchall()
        #loop through each stuent in the stuents variable which contains all the rows 
        for student in students:

            print(student)

    except:
        print("Could not retrieve students from the database")

# function that adds a new student to the database
def addStudent(connection, first_name, last_name, email, enrollment_date):
    try:
        #store the connection.cursor() object in the variable query
        query = connection.cursor()

        #execute the sql command to insert a new student into the students table with the given parameters
        query.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);",
                       (first_name, last_name, email, enrollment_date))
       
       #commit is a method of the connection object used to save changed made to the database
        connection.commit()

        print(f"Student {first_name} {last_name} has been successfully added to the database")
    except:
        print(f"Could not add {first_name} {last_name} to the database")

# function to update the the email of a given student
def updateStudentEmail(connection, student_id, new_email):
    try:
        #store the connection.cursor() object in the variable query
        query= connection.cursor()

        #execute the sql command to update email of student at a given id
        #this sql comand sets the email of the student at the given id to the new email
        query.execute("UPDATE students SET email = %s WHERE student_id = %s;",
                       (new_email, student_id))
        
        #save the changes made to the database
        connection.commit()

        #get the first and last name of the student at the given id and print as string
        query.execute("SELECT first_name, last_name FROM students WHERE student_id = %s;", (student_id,))
        student = query.fetchone()
        
        #if student is not None, assign the first and last name to the variables fName and lName
        if student:
            fName, lName = student
            fullName = fName + " " + lName

        print(f"Email for {fullName} has been successfully updated to {new_email} in the database")
    except:
        print(f"Could not update email for {fullName} in the database")

# function that deletes a student from the database
def deleteStudent(connection, student_id):
    try:
        #store the connection.cursor() object in the variable query
        query = connection.cursor()

        #get the name of the student at the given id using execute
        query.execute("SELECT first_name, last_name FROM students WHERE student_id = %s;", (student_id,))
        student = query.fetchone()

        if student:
            fName, lName = student
            fullName = fName + " " + lName

        #execute the sql command to delete a student from the students table with the given id
        query.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        
        #save the changes made to the database
        connection.commit()

        print(f"The student {fullName} has been successfully deleted from the database")
    except:
        print(f"Could not delete student {fullName} from the database")

# Main function to demonstrate usage
def main():
    # Establish connection
    connection = create_connection()
    
    #if connection is None:
        #return

    #display all students before adding, updating and deleting
    print("Here are all the students in the database: ")
    getAllStudents(connection)
    print("\n")

    #CRUD operations
    addStudent(connection, "Amy", "Smith", "amy.smith@example.com", "2023-09-03")
    updateStudentEmail(connection, 2, "new.email@example.com")
    deleteStudent(connection, 3)
    
    #display all students after adding, updating and deleting
    print("\nHere are all the students in the database after adding, updating and deleting: ")
    getAllStudents(connection)

    #close the connection to the database
    connection.close()

# Call the main function
if __name__ == "__main__":
    main()