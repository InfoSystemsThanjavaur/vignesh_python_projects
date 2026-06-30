from django.shortcuts import render
import mysql.connector
from datetime import datetime
from django.http import HttpResponse
import numpy as np
import pickle
username = ''
email =''
def database():
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
    mycur = mydb.cursor()
    return mydb , mycur
def home(request):
    return render(request,'home.html',{})
def ad(request):
    return render(request,'admin.html',{})
def user(request):
    if request.method == "POST":
        global username
        global email
        email = request.POST['mail']
        z = request.POST['pwd'] 
        mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="bank")
        mycursor = mydb.cursor()
        sql = "SELECT mail, pwd, un FROM reg WHERE mail = %s AND pwd = %s"
        val = (email, z)
        mycursor.execute(sql, val)
        res = mycursor.fetchall()
        
        if len(res) != 0 and res[0][0] == email and res[0][1] == z:
            username = res[0][2] 
            return render(request, 'use/oguser.html', {'username': username})
        else:
            return render(request, 'use/user.html', {"result": "fail"})
    else:
        return render(request, 'use/user.html', {})

def userreg(request):

    if request.method=='POST':
        
        global username
        global email
        a=request.POST['name1']
        b=request.POST['add']
        c=request.POST['cit'] 
        d=request.POST['brn']
        e=request.POST['zip']
        f=request.POST['un']
        g=request.POST['pwd']
        h=request.POST['cpwd']
        i=request.POST['phno']
        j=request.POST['mail']
        k=request.POST['acctype']
        l=request.POST['accno']
        m=request.POST['ifscno']       
        n=request.POST['amt'] 
        email = j
        if g==h:
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
            mycursor=mydb.cursor()
            sql="insert into reg(name,address,city,branch,zip,un,pwd,phno,mail,acctype,accno,ifsc,amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(a,b,c,d,e,f,g,i,j,k,l,m,n)
            mycursor.execute(sql,values)
            mydb.commit()
            return render(request,'use/oguser.html',{'status':"success"})
        else: 
            return render(request,'use/userreg.html',{"status":"fail"})
    else:
        return render(request,'use/userreg.html',{})

def apply(request):
    if request.method=='POST':
        a=request.POST['full_name']
        b=request.POST['email']
        c=request.POST['phone']
        d=request.POST['dob']
        e=request.POST['income']
        f=request.POST['employment_status']
        g=request.POST['address']
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        
        mycursor=mydb.cursor()
        sql="insert into card(name,mail,phone,dob,income,job,address,status) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        status="pending"
        values=(a,b,c,d,e,f,g,status)
        print(values)
        
        mycursor.execute(sql,values)
        mydb.commit()
        return render(request,'use/oguser.html',{'status':"success"})
    else: 
        return render(request,'cardreg.html',{"status":"fail"})


def transfer(request):
    return render(request,'use/oguser.html',{})

def detail(request):
    if request.method == "GET":

        if email != None:
            mydb , mycur = database()
            mycur.execute("SELECT name,address,city,branch,zip,un,phno,mail,acctype,accno,ifsc,amount FROM reg WHERE mail = %s", (email,))
            data = mycur.fetchall()
            print(data)
        return render(request,'udetail.html',{'result':data})

    else:
        return render(request,'udetail.html',{})



def admin(request):

    if request.method=="POST":
        global username
        username=request.POST['un']
        z=request.POST['pwd'] 
        mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
        mycursor=mydb.cursor()
        sql = "select un, pwd from adreg where un = %s and pwd=%s" 
        val=(username,z)
        mycursor.execute(sql,val)
        
        res= mycursor.fetchall()
        print(res)
        if len(res)!=0:
            if res[0][0]==username and res[0][1]==z:
                return render(request,'admin.html',{})
        else:
            return render(request,'adlogin.html',{"result":"fail"})
    else:
        return render(request,'adlogin.html',{})
def adreg(request):
    if request.method=='POST':
        a=request.POST['adun']
        b=request.POST['admail']
        c=request.POST['pwd']
        d=request.POST['cpwd'] 
        print("hlo")
    
        if c==d:
            print("hlo")
            mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="bank")
            mycursor=mydb.cursor()
            sql="insert into adreg(un,email,pwd) values(%s,%s,%s)"
            values=(a,b,c)
            mycursor.execute(sql,values)
            mydb.commit()
            return render(request,"adreg.html",{'status':"success"})
        else: 
            return render(request,"adreg.html",{"status":"fail"})
    else:
        print("k")
        return render(request,"adreg.html",{})

def bankdetail(request):
   
    if request.method == "GET":

         
        mydb , mycur = database()
        mycur.execute("SELECT name,address,city,phno,mail,acctype,accno,ifsc,amount FROM reg")
        data = mycur.fetchall()
        print(data)
        return render(request,'bd.html',{'result':data})

    else:
        return render(request,'bd.html',{})

def remove(request):
    if request.method == "POST":
        acno = request.POST['acno']
        mydb, mycur = database()
        mycur.execute("DELETE FROM reg WHERE accno = %s", (acno,))
        mydb.commit()
        return render(request,"admin.html",{})
    else:
        return render(request,"remove.html",{})
    
   

def contact(request):
    return render(request,'contact.html',{})
def about(request):
    return render(request,'about.html',{})
def logout(request):
    return render(request,'home.html',{})


def checkPayment(acno):
    mycon , mycur  = database()
    sql = "select amount from reg where accno = %s"
    val =(acno,)

    mycur.execute(sql,val)
    payment = mycur.fetchall()
    if  payment:
        return int(payment[0][0])
    else:
        return 0

def paymentUpdate(payment ,  acno):
    mycon , mycur  = database()
    sql = "update reg set amount = %s where accno = %s"
    val=(payment , acno)
    mycur.execute(sql,val)
    mycon.commit()
    if mycur.rowcount:
        return True
    else:
        return False
    
def insertTransaction(fromac , toac ,payment,date):
    mycon , mycur  = database()
    sql = "insert into  transactionsdetails (FromAccountNumber ,ToAccountNumber ,TransferPayment ,Date) values(%s,%s,%s,%s)"
    val=(fromac,toac , payment ,date)
    mycur.execute(sql,val)
    mycon.commit()
    if mycur.rowcount:
        return True
    else:
        return False

def findUser():
    mycon , mycur  = database()
    sql = "select accno from reg where mail = %s"
    print(email)
    val=(email , )
    mycur.execute(sql,val)
    acc= mycur.fetchall()
    print(acc)
    return acc[0][0]

def DownloadTransaction():
    mycon , mycur  = database()
    account = findUser()
    sql = "select * from transactionsdetails where  fromaccountnumber = %s"
    val=  (account,)
    mycur.execute(sql,val)
    transaction = mycur.fetchall()
    if  transaction:
        return transaction 
    else:
        return 0



def transfer(request):
    if request.method=="POST":
        current_date = datetime.now()

        date = current_date.strftime("%d/%m/%Y")
        ya = request.POST["from-account"]
        ta = request.POST["to-account"]
        payment =int( request.POST["amount"])
        account = findUser()
        pay1 = checkPayment(ya)
        pay2 = checkPayment(ta)
        if pay1 and pay2 and (ya==account):
                
            if payment<=pay1:
                your_payment = pay1 - payment
                transfer_payment = pay2 + payment
                if (paymentUpdate(your_payment ,  ya) and paymentUpdate(transfer_payment , ta) and insertTransaction(ya , ta, payment , date)):
                    return render(request,'use/oguser.html',{'status':1})
                else:
                    return render(request,'transfer.html',{'status':0})
            else:
                return render(request,'transfer.html',{'result':-1})
        else:
            return render(request,'transfer.html',{'result':404})

    else:
        return render(request,'transfer.html',{})
    

def viewTransaction(request):
    print(email)
    if request.method=="GET":
       
        
        data = DownloadTransaction()
        if data:
            return render(request,'ViewTransactions.html',{'result':data})
        else:
            return render(request,'ViewTransactions.html',{'result':0})

    else:
        return render(request,'ViewTransactions.html',{})
    

def download(request):
    content="From Account NO, To Account NO, Transfer Amount, Date\n"
    datas = DownloadTransaction()
    print(datas)
    for data in datas:
        content += str(data[0]) + "," + str(data[1]) + "," + str(data[2])+ ","+str(data[3]) + "," +"\n"
    
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction.csv"'

    return response



def load_model():
    with open("static/new_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("static/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    return model, scaler

def predict_fraud(request):
    prediction_result = None

    if request.method == 'POST':
        try:
            # Retrieve form data
            merchant_id = int(request.POST.get('id'))
            amount = float(request.POST.get('amt'))
            is_declined = 1 if request.POST.get('decline').lower() == 'yes' else 0
            no_decline = int(request.POST.get('no_decline'))
            is_foreign = 1 if request.POST.get('ft').lower() == 'yes' else 0

            # Prepare data for model prediction (Remove merchant_id)
            input_data = np.array([[amount, is_declined, no_decline, is_foreign]])
            print("Input before scaling:", input_data)

            # Load model & scaler
            model, scaler = load_model()

            # Scale the input data
            input_data_scaled = scaler.transform(input_data)
            print("Scaled input:", input_data_scaled)

            # Make prediction
            prediction = model.predict(input_data_scaled)
            prediction_result = "Fraud" if prediction[0] == 1 else "Not Fraud"
            print("Prediction:", prediction_result)

        except Exception as e:
            print("Error:", e)
        

        return render(request, 'check.html', {'result': prediction_result})
    else:
        return render(request, 'check.html', {'result': prediction_result})