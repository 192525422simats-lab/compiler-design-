from flask import Flask,render_template,request,redirect,url_for,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3,json
from datetime import datetime
from compiler import compile_drl
app=Flask(__name__); app.secret_key='replace-this-secret-key'; DB='disaster_relief.db'
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT,email TEXT UNIQUE,password TEXT)')
 c.execute('CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,user_id INTEGER,command TEXT,result TEXT,created TEXT)')
 if c.execute('SELECT COUNT(*) FROM users').fetchone()[0]==0:c.execute('INSERT INTO users(name,email,password) VALUES(?,?,?)',('Demo Officer','demo@relief.local',generate_password_hash('Demo@123')))
def logged(): return 'uid' in session
@app.context_processor
def ctx(): return {'year':datetime.now().year}
@app.route('/')
def home(): return redirect('/dashboard') if logged() else render_template('landing.html')
@app.route('/register',methods=['GET','POST'])
def register():
 if request.method=='POST':
  try:
   with db() as c:c.execute('INSERT INTO users(name,email,password) VALUES(?,?,?)',(request.form['name'],request.form['email'].lower(),generate_password_hash(request.form['password'])))
   flash('Account created. Please sign in.','success'); return redirect('/login')
  except sqlite3.IntegrityError: flash('Email already registered.','danger')
 return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  with db() as c:u=c.execute('SELECT * FROM users WHERE email=?',(request.form['email'].lower(),)).fetchone()
  if u and check_password_hash(u['password'],request.form['password']):session['uid']=u['id'];session['name']=u['name'];return redirect('/dashboard')
  flash('Invalid email or password.','danger')
 return render_template('login.html')
@app.route('/logout')
def logout():session.clear();return redirect('/')
@app.route('/dashboard')
def dashboard():
 if not logged():return redirect('/login')
 with db() as c:
  total=c.execute('SELECT COUNT(*) FROM runs WHERE user_id=?',(session['uid'],)).fetchone()[0]
  recent=c.execute('SELECT * FROM runs WHERE user_id=? ORDER BY id DESC LIMIT 5',(session['uid'],)).fetchall()
 return render_template('dashboard.html',total=total,recent=recent)
SAMPLE='DISASTER FLOOD AT "North Village" PRIORITY HIGH;\\nRESOURCE WATER 500;\\nRESOURCE FOOD 300;\\nRESOURCE MEDICAL_KIT 120;\\nALLOCATE WATER 200 TO "North Village";\\nALLOCATE FOOD 150 TO "North Village";\\nALLOCATE MEDICAL_KIT 50 TO "North Village";'
@app.route('/compiler',methods=['GET','POST'])
def compiler():
 if not logged():return redirect('/login')
 command=request.form.get('command',SAMPLE); result=None
 if request.method=='POST':
  result=compile_drl(command)
  with db() as c:c.execute('INSERT INTO runs(user_id,command,result,created) VALUES(?,?,?,?)',(session['uid'],command,json.dumps(result),datetime.now().strftime('%d %b %Y %I:%M %p')))
 return render_template('compiler.html',command=command,result=result)
@app.route('/history')
def history():
 if not logged():return redirect('/login')
 with db() as c:rows=c.execute('SELECT * FROM runs WHERE user_id=? ORDER BY id DESC',(session['uid'],)).fetchall()
 return render_template('history.html',rows=rows)
if __name__=='__main__':app.run(debug=True)
