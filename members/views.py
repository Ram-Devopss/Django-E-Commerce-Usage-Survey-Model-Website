from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from requests import request
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import random

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#import the sklearn libraries
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score


account={}
otp_number = str(random.randint(100000, 999999))
detection ={}



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def main(request):
    return render(request,"main.html")


def index(request):
    # If the login was unsuccessful or it's not a POST request, render the login page
    return render(request, 'login.html')


@csrf_protect   
def welcome(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
            
        user=authenticate(username=username,password=password)
        print(username,password)
        if user is not None:
           login(request,user)
           messages.success(request,"Welcome,You are Successfully Logged in!!!")
           return render(request,"dashboard.html")
        else:
            messages.error(request,"Username or Password is incorrect.Please try again..")
            return render(request,"error.html")
    
    return render(request,"index.html")

# Creating a Account
def register(request):
            
 return render(request,"signup.html")
        


def detect(request):
    df = pd.read_csv('./dataset/Ecommerce Customers.csv')
    print(df.head())
    print(df.info())
    df.shape
    print(df.describe())
    print(df.keys())
    print(df.isna().sum())


    #plots

    sns.pairplot(df)


    #machine learning algorithm

    X = df.iloc[:,3:7]
    y = df.iloc[:,7:8]
    X.head()
    y.head()


    #Seperate the data into the training and test data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=63) 

    from sklearn.linear_model import LinearRegression
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)

    score = linreg.score(X_test,y_test)
    print("Prediction Score of the model is:",score)

    plt.scatter(y_test,y_pred)
    plt.ylabel("Y - Prediction")
    plt.xlabel("Y - Test")
    plt.title("y_test vs y_pred scatter plot")
    plt.show()

    
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    print("Weekly A Customer Spend:",mean_absolute_error(y_test,y_pred))
    print("Monthly A Customer Spend:",np.sqrt(mean_squared_error(y_test,y_pred)))
    print("Yearly A Customer Spend:",mean_squared_error(y_test,y_pred))

    datas={}
    datas['week'] = "Weekly A Customer Spend:",mean_absolute_error(y_test,y_pred)
    datas['month'] = "Monthly A Customer Spend:",np.sqrt(mean_squared_error(y_test,y_pred))
    datas['year'] = "Yearly A Customer Spend:",mean_squared_error(y_test,y_pred)

    print('################### --------------- Code Was Succeffully Executed!')
    return render(request,"dashboard.html",datas)

def send_otp(request):
    if request.method == 'POST':

        account['user'] = request.POST.get("username")
        account['email']  = request.POST.get("email")
        account['mobile'] = request.POST.get("mobile")
        account['password'] = request.POST.get("password")
        account['repassword'] = request.POST.get("confirmPassword")
        account['method'] = request.POST.get('Verification')

        credential = {'name':account['user'],'email':account['email'],'mobile':account['mobile'],'password':account['password'],'repassword':account['repassword'],'method':account['method']}
        # Open the file in write mode
        with open('credential.txt', 'w') as file:
        # Write the content to the file
            file.write(str(credential))
        
        if account['method'] == 'email':
            # Your email credentials
            fromaddr = "ramdevops2005@gmail.com"
            toaddr = request.POST.get("email")
            smtp_password = "rcau rkir ffiw megr"

            # Create a MIMEMultipart object
            msg = MIMEMultipart()

            # Set the sender and recipient email addresses
            msg['From'] = fromaddr
            msg['To'] = toaddr
            
            # Set the subject
            msg['Subject'] = "Liver Detection Otp Verification"

            # Set the email body
            body = f"Your OTP is: {otp_number}"
            msg.attach(MIMEText(body, 'plain'))

            try:
                # Connect to the SMTP server
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Log in to the email account
                    server.login(fromaddr, smtp_password)

                    # Send the email
                    server.sendmail(fromaddr, toaddr, msg.as_string())

                # Email sent successfully, render a template
                return render(request, 'verification_otp.html')

            except Exception as e:
                # An error occurred while sending email, redirect with an error message
                messages.error(request, f"Error sending OTP email: {e}")
                return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name
        else:
            # Invalid method, redirect with an error message
            messages.error(request, "Invalid verification method")
            return render(request,'signup.html')  # You need to replace 'verify_it' with the appropriate URL name

    # If the request method is not POST, redirect with an error message
    messages.error(request, "Invalid request method")
    return render(request,'signup.html') # You need to replace 'verify_it' with the appropriate URL name


def verify_it(request):
    
    if request.method=="POST":


       

        verifi_otp1 = request.POST.get("otp1")
        verifi_otp2 = request.POST.get("otp2")
        verifi_otp3 = request.POST.get("otp3")
        verifi_otp4 = request.POST.get("otp4")
        verifi_otp5 = request.POST.get("otp5")
        verifi_otp6 = request.POST.get("otp6")

        six_digits=f"{verifi_otp1}{verifi_otp2}{verifi_otp3}{verifi_otp4}{verifi_otp5}{verifi_otp6}"
        if six_digits==otp_number:

         my_user=User.objects.create_user(account['user'],account['email'],account['password'])
         my_user.save() 
         messages.success(request,"Your account has been Created Successfully!!!")
         redirect(index)


        # else:
        #     messages.success(request,"Registration Failed!!")
        #     return render(request, 'success.html',six_digits)
        
    return render(request,"login.html")  

