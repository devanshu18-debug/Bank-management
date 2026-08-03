#Bank account
#deposite money
#withdraw money
#details
#update detail
#delete account
import json
import random
import string
from pathlib import Path
 
class Bank:
    db = 'data.json'
    data = []
    try:
        if Path (db).exists():
            with open(db) as file:
                data  = json.loads(file.read())
        else:
            print("No such file exist ")
    except Exception as err:
        print(f"an exception occured as {err}")
    @classmethod
    def __update(cls):
        with open(Bank.db,'w') as file:
            file.write(json.dumps(Bank.data))
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k = 3)
        num = random.choices(string.digits,k = 3)
        spchar = random.choices("!@#$%&*^",k = 1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
    def createaccount(self):
        info = {
            "name" : input("Tell me your Name :- "),
            "age" : int(input("Tell me your Age :- ")),
            "email" : input("Tell me your Email :- "),
            "pin" : int(input("Tell me your 4 digit pin :- ")),
            "accountNO." : Bank.__accountgenerate(),
            "balance" : 0
        }
        if info['age'] <18 or len(str(info['pin'])) != 4:
            print("sorry you cannot create account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note down your account number ")
            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        accnumber = input("please tell your account number")
        pin = int(input("please tell your pin as well"))
        userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("sorry no data found")
        else:
            amount = int(input("how much you want to deposit"))
            if amount>10000 or amount<=0:
                print("sorry the amount is too much you can deposite below 10000")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount deposited successfully")
    def withdrawmoney(self):
        accnumber = input("please tell your account number")
        pin = int(input("please tell your pin as well"))
        userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("sorry no data found")
        else:
            amount = int(input("how much you want to withdraw"))
            if amount>10000 or amount<=0:
                print("sorry the amount is too much you can withdraw below 10000")
            else:
                if userdata[0]['balance'] >= amount:
                    userdata[0]['balance'] -= amount
                    Bank.__update()
                    print("Amount withdrew successfully")
                else:
                    print("insufficient balance")

    def showdetails(self):
        accnumber = input("please tell your account number")
        pin = int(input("please tell your pin as well"))
        userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
        print("your information are \n\n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
    def updatedetails(self):
        accnumber = input("please tell your account number")
        pin = int(input("please tell your pin as well"))
        userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("sorry no data found")
        else:
            print("you cannot change the age, account number,balance")

            print("fill the details for change or leave it empty if no change")
            newdata = {
                "name" : input("please tell your new name or press enter"),
                "email" : input("please tell your new Email or press enter to skip"),
                "pin" : input("enter new Pin or press enter to skip")
            }
            if newdata["name"] =="":
                newdata["name"] = userdata[0]['name'] 
            if newdata["email"] =="":
                newdata["email"] = userdata[0]['email'] 
            if newdata["pin"] =="":
                newdata["pin"] = int(userdata[0]['pin']) 

            newdata['age'] = userdata[0]['age']
            newdata['accountNO.'] = userdata[0]['accountNO.']
            newdata['balance'] = userdata[0]['balance']

            if type(newdata['pin']) == str:
                newdata['pin'] = newdata['pin']

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]
                print("details updated successfully")
            Bank.__update()


    def deleteaccount(self):
        accnumber = input("please tell your account number")
        pin = int(input("please tell your pin as well"))
        userdata = [i for i in Bank.data if i['accountNO.'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("sorry no such data exist")
        else:
            choice = input("press y if you actully want to delete your account if no press n ")
            if choice == 'n' or choice =='N':
                print("bypassed")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account deleated successfully")
                Bank.__update()

                
user = Bank()

while True:
    print("========== Bank Account Management System ==========")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Account Details")
    print("5. Update Account Details")
    print("6. Delete Account")
    print("7. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        user.createaccount()

    elif choice == 2:
        user.depositmoney()

    elif choice == 3:
        user.withdrawmoney()

    elif choice == 4:
        user.showdetails()

    elif choice == 5:
        user.updatedetails()

    elif choice == 6:
        user.deleteaccount()

    elif choice == 7:
        print("Thank you for using the Bank Account Management System.")
        break

    else:
        print("Invalid Choice! Please enter a number between 1 and 7.")
