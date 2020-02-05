'''
Food Recipe web app to learn different types  food recipes.

'''
from flask import *
import database
import config

#To start the application.
app=Flask(__name__)
app.secret_key=config.secret_key


# Main function of application.
@app.route('/')
def main():
	return render_template('main.html')

# To signup into database.
@app.route('/signup')
def signup():
	return render_template('signup.html')

# To create your new own account.
@app.route('/create',methods=['POST'])
def create():
	first=request.form['firstname']
	last=request.form['lastname']
	# Check if email is already exist or not.
	if database.check_duplicate(request.form['email'])==True:
		email=request.form['email']
	else:
		return render_template('signup.html',error1='Email id is already exist')
	# if phone is given or not.
	if request.form['phone']!=None:
		phone=request.form['phone']
	else:
		phone=None
	dob=request.form['date']
	gender=request.form['gender']
	password=request.form['password']
	# To store in database.
	database.createdata(first,last,email,phone,dob,gender,password)
	return redirect('/')

#login to session.
@app.route('/login',methods=['POST'])
def login():
	email=request.form['email']
	password=request.form['password']
	# Check whether email and password is exist or not.
	if database.show(email,password)==True:
		#To create session object.
		session['email']=request.form['email']
		return redirect('/food')
	else:
		return render_template('main.html',error='Incorrect email or Password')

#logout of session.
@app.route('/logout')
def logout():
	# To check whether the email is exist in session or not. 
	if 'email' in session:
		# To logout pop the email from session.
		session.pop('email')
		return render_template('main.html',error='You logged out of this account.')
	else:
		return render_template('main.html',error="Login First.") 

# See your profile
@app.route('/profile/<email>')
def profile(email):
	# Check whether the email is exist in session or not.
	if 'email' in session:
		profile=database.profile(email)
		food=database.foodrecipe(email)
		first=profile[0][0]
		last=profile[0][1]
		email=profile[0][2]
		phone=profile[0][3]
		dob=profile[0][4]
		gender=profile[0][5]

		return render_template('profile.html',first=first,last=last,\
			email=email,phone=phone,dob=dob,gender=gender,food=food)
	else:
		return render_template('main.html',error="Login First.")

# Food list on main frame.
@app.route('/food')
def food():
	# Check whether the email is exist in session or not.
	if 'email' in session:
		profile=database.profile(session['email'])
		food=database.food()

		# To show the last uploaded content in database in first.
		food1=food[::-1]
		first=profile[0][0]
		last=profile[0][1]
		email=profile[0][2]
		
		# Add the profile and food to show that at the main frame.
		foodrecipe=[[y[0],y[1],x[0],x[1],x[2],x[3],x[4],x[5]] for x in food1 \
		for y in database.profile(x[1])]

		return render_template('food.html',first=first,last=last,\
			email=email,foodrecipe=foodrecipe)
	else:
		return render_template('main.html',error="Login First.")

# Search the item name or ingredients.
@app.route('/search',methods=['POST'])
def search():
	# Check whether the email is exist in session or not.
	if 'email' in session:
		food=database.food()
		searched=(request.form['search']).lower()
		detailed=[]
		for x in food:
			if (x[2]).lower()==searched:
				detailed.append(x)
			elif searched in (x[3]).lower().split(','):
				detailed.append(x)
		foodrecipe=[[y[0],y[1],x[0],x[1],x[2],x[3],x[4],x[5]] for x in detailed\
		 for y in database.profile(x[1])]
		return render_template('foodsearch.html',foodrecipe=foodrecipe)

# Searched Item list.
@app.route('/searched/<item>')
def searched(item):
	# Check whether the email is exist in session or not.
	if 'email' in session:
		food=database.food()
		foodrecipe=[[y[0],y[1],x[0],x[1],x[2],x[3],x[4],x[5]] for x in food \
		for y in database.profile(x[1]) if item == x[2]]
		return render_template('searched.html',foodrecipe=foodrecipe)
	else:
		return render_template('main.html',error="Login First.")

# Edit that particular item.
@app.route('/edit',methods=['POST'])
def edit():
	# Check whether the email is exist in session or not.
	if 'email' in session:
		# To check whether the edit person is owner or not.
		if request.form['email']==session['email']:
			id1=request.form['id']
			foodname=request.form['foodname']
			ingredients=request.form['ingredients']
			process=request.form['process']
			time=request.form['time']
			# Edit the item list.
			database.edit(id1,request.form['email'],foodname,ingredients,process,time)
			return redirect(url_for('searched',item=foodname))
		else:
			return render_template('searched.html',error='The owner can update the information only.')


# Add recipe to your account.
@app.route('/addrecipe',methods=['POST'])
def addrecipe():
	# Check whether the email is exist in session or not.
	if 'email' in session:
		item_name=request.form['items']
		ingredients=request.form['ingredients']
		process=request.form['process']
		
		#Add food to the database.
		database.addfood(session['email'],item_name,ingredients,process)
		return redirect(url_for('profile',email=session['email']))
if __name__=='__main__':
	app.run(debug=True)