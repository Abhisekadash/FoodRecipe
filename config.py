import mysql.connector

# To connect mysql databases.
def config_db():
	mydb=mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="chiku123",
		database="foodrecipe"
		)
	return mydb
# Secret Key of session.
secret_key='Abhisek123'
DEBUG=True