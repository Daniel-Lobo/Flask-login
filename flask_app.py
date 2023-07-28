from flask import Flask
from jinja2 import Template
from flask import request
from json import dumps
from database import Database
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from asyncio import run
from threading import Thread

app = Flask(__name__)

def SendSecret(receiver_email, secret, root):
    print('started')
    sender_email   = 'dabo.loniel@gmail.com'    
    password       = 'qbffrrmwvdthnuuu'

    msg = MIMEMultipart()
    msg['From']    = sender_email
    msg['To']      = receiver_email
    msg['Subject'] = 'Access token'
    message        = f'Access the app using the link:\n{root}access?&user={receiver_email}\nWith the code:\n{secret}'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP(host='smtp.gmail.com', port=587)   
    mailserver.ehlo()   
    mailserver.starttls()    
    mailserver.ehlo()
    mailserver.login(sender_email, password)
    
    mailserver.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
    mailserver.quit()
    print('ended')

def template(file):
    with open(file, 'r') as f: return f.read()

def GetArgs():
    return [request.args.get(arg) for arg in ['email', 'password']]  

@app.route("/")
async def main():
    return Template(template('login.html')).render(items=[hex(n).split('0x')[1] for n in range(16)], rows=[hex(0x1F60 + n).split('0x')[1] for n in [0, 1, 2, 3, 4, 8, 9, 10, 11]])

@app.route('/access')
async def access():
    return Template(template('access.html')).render()

@app.route('/access_submit')
async def access_submit():
    email, code = request.args.get('email'), request.args.get('code')
    db = Database()
    if not db.IsUser(email): return dumps({'code' : f'{email} is not a registered user'})
    else:
        user = db.GetUser(email)
        if user is None          : return dumps({'code' : 'database error'})
        if user['secret'] != code: return dumps({'code' : f'wrong access code {user["secret"] }'}) 
        else: 
            user = db.UpdateSecret(email) 
            Thread(target=SendSecret, args=(email, user['secret'], request.root_url,)).start() #type: ignore      
            return dumps({'code' : 'OK', 'msg' : Template(template('loged.html')).render(user=email)})              

@app.route("/login")
async def login():  
    reply = {'err' : ''}
    email, password = GetArgs()    
    db = Database()
    if not db.IsUser(email):
        reply['err'] = f'{email} is not an user. Please register 1st'        
    else:
        user = db.GetUser(email)
        if user is None:
            reply['err'] = f'{email} databse error'            
        elif password != user['password']:
            reply['err'] = f'{email} wrong password'
        else:  
            user = db.UpdateSecret(email) 
            if user is None or isinstance(user, str):
               reply['err'] = f'{email} databse error'         
            else:
                Thread(target=SendSecret, args=(email, user['secret'], request.root_url,)).start()
                reply['err'] = f'A acess link and access token link was sent to "{email}". Please access that link to finalize login' 
    return dumps(reply, indent=4)

@app.route("/register")
async def register():   
    reply = {'err' : ''}
    email, password = GetArgs()    
    db = Database()
    if db.IsUser(email):
        user = db.GetUser(email)
        reply['err'] = f'{email} is already an user'
    else :
        db.AddUser(email, password)
        user = db.GetUser(email)
        if user is None:
            reply['err'] = f'{email} databse error'
            return dumps(reply, indent=4)
        Thread(target=SendSecret, args=(email, user['secret'], request.root_url,)).start()
        reply['err'] = f'A confirmation link was sent to "{email}". Please access that link to finalize registrations'
    
    return dumps(reply, indent=4)


if __name__ == '__main__': app.run()