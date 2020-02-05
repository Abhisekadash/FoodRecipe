# import config
import config

# Create cursor.
mydb=config.config_db()
mycursor=mydb.cursor()

#for creating ids
def createdata(firstname,lastname,email,phone,dob,gender,password):
	sql='insert into userdata(firstname,lastname,email,phone,dob,\
	gender,password) values(%s,%s,%s,%s,%s,%s,%s);'
	val=(firstname,lastname,email,phone,dob,gender,password)
	mycursor.execute(sql,val)
	mydb.commit()
	print(mycursor.rowcount, "record inserted.")

# To login to the website.
def show(email,password):	
	mycursor.execute('select email,password from userdata')
	mylist=mycursor.fetchall()
	for x in range(len(mylist)):
		if mylist[x][0]==email and mylist[x][1]==password:
			return True

# Check Duplicate.
def check_duplicate(email):
	mycursor.execute('select email from userdata')
	mylist=mycursor.fetchall()
	for x in range(len(mylist)):
		if email == mylist[x][0]:
			return False
	else:
		return  True
# To show the profile.
def profile(email):
	sql='select firstname,lastname,email,phone,dob,gender from userdata where email=%s'
	val=(email,)
	mycursor.execute(sql,val)
	mylist=mycursor.fetchall()
	return mylist

# To show the foood content on that profile only.
def foodrecipe(email):
	sql='select item,ingredients,process from food where email=%s'
	val=(email,)
	mycursor.execute(sql,val)
	recipe=mycursor.fetchall()
	return recipe

# To show all the food recipe.
def food():
	mycursor.execute('select * from food')
	food=mycursor.fetchall()
	return food

# Add food to the database.
def addfood(email,item,ingredients,process):
	sql='insert into food(email,item,ingredients,process) values(%s,%s,%s,%s)'
	val=(email,item,ingredients,process)
	mycursor.execute(sql,val)
	mydb.commit()

# Edit/update the food contents.
def edit(id1,email,foodname,ingredients,process,time):
	sql='update food set item=%s,ingredients=%s,process=%s,time=%s where id=%s and email=%s'
	val=(foodname,ingredients,process,time,id1,email)
	mycursor.execute(sql,val)
	mydb.commit()
