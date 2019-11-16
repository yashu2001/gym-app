'''
developed by yash narang
gym management system 
'''
from xlsxwriter.workbook import Workbook
import getpass
import time
import datetime
import os
import sqlite3
from tkinter import Tk
from tkinter.filedialog import askdirectory
from colorama import init, Fore, Back, Style
init(convert=True)
try:
    conn = sqlite3.connect('maindb.sqlite')
    cur = conn.cursor()
except:
    print('CONNECTION ERROR')
    time.sleep(5)
def mk_attd1():
    os.system('cls')
    cur.execute('''
                SELECT c_id FROM Client_data
                '''
                )
    c_ids=cur.fetchall()
    #print(c_ids)
    print('ABC GYM')
    c_id=int(input('enter client id:'))
    t=1
    for x in c_ids:
        if(c_id==x[0]):
            t=0
            break
        else:
            t=1
    if(t==1):
        print('invalid client id')
    else:    
        n=int(input('1.intime\n2.outtime\nenter your choice:'))
        tm=datetime.datetime.now()
        tm=tm.strftime("%X")
        tm="'"+tm+"'"
        dt=datetime.datetime.now()
        dt=dt.strftime('%Y-%m-%d')
        dt="'"+dt+"'"
        if(n==1):
            cur.execute('''
                        INSERT INTO Attendance (c_id,IN_TIME,OUT_TIME,date) VALUES ({},{},{},{});
                        '''.format(c_id,tm,tm,dt)
                        )
            conn.commit()
        if(n==2):
            cur.execute('''
                        UPDATE Attendance SET OUT_TIME={} WHERE(c_id={} AND date={});
                        '''.format(tm,c_id,dt))
            conn.commit()
        
    return None
def mk_attd2():
    os.system('cls')
    cur.execute('''
                SELECT c_id FROM Client_data
                '''
                )
    c_ids=cur.fetchall()
    #print(c_ids)
    print('ABC GYM\n')
    c_id=int(input('enter client id:'))
    t=1
    for x in c_ids:
        if(c_id==x[0]):
            t=0
            break
        else:
            t=1
    if(t==1):
        print('invalid client id')
    else:    
        n=int(input('1.intime\n2.outtime\nenter your choice:'))
        tm=datetime.datetime.now()
        tm=tm.strftime("%X")
        tm="'"+tm+"'"
        dt=datetime.datetime.now()
        dt=dt.strftime('%Y-%m-%d')
        dt="'"+dt+"'"
        if(n==1):
            cur.execute('''
                        INSERT INTO Attendance (c_id,IN_TIME,OUT_TIME,date) VALUES ({},{},{},{});
                        '''.format(c_id,tm,tm,dt)
                        )
            conn.commit()
        if(n==2):
            cur.execute('''
                        UPDATE Attendance SET OUT_TIME={} WHERE(c_id={} AND date={});
                        '''.format(tm,c_id,dt))
            conn.commit()
        
    return None
def chg_pass():
    os.system('cls')
    print('ABC GYM')
    uname=list(input('enter username:'))
    uname.append('\'')
    uname.insert(0,'\'')
    uname=''.join(uname)    
    cur.execute('''
                    SELECT u_pass,u_type FROM Users WHERE u_name={}'''.format(uname))
    psd=cur.fetchall()
    pswd=getpass.getpass(prompt='Current Password:')
    if(psd[0][0]==pswd):
        pswd=getpass.getpass(prompt='NEW Password:')
        pswd="'"+pswd+"'"
        cur.execute('''
                    UPDATE Users SET u_pass={} WHERE(u_name={})
                    '''.format(pswd,uname)
                   )
        conn.commit()
    else:
        chg_pass()
    return None

def attd_rep():
    os.system('cls')
    print('ABC GYM')
    print('1.Retrieve report by date\n2.Retrieve report by client id')
    n=int(input('enter your choice:'))
    if(n==1):
        ent=input('enter name for excel file:')
        root=Tk()
        root.withdraw()
        path = askdirectory(title='Select Folder') # shows dialog box and return the path
        workbook = Workbook('{}/{}.xlsx'.format(path,ent))
        worksheet = workbook.add_worksheet()
        ls=(['client id',0],['name',0],['mob no',0],['in time',0],['out time',0])
        row=0
        col=0
        for x,y in ls:
            worksheet.write(row,col,x)
            col=col+1
        dt=input('enter date in yyyy-mm-dd format:')
        dt="'"+dt+"'"
        cur.execute('''
                    SELECT name,m_no,IN_TIME,OUT_TIME
                    FROM [Attendance] JOIN Client_data
                    ON [Attendance].c_id=Client_data.c_id
                    WHERE date={}
                    '''.format(dt)
                    )
        mysel=cur.execute('''
                    SELECT [Attendance].c_id,name,m_no,IN_TIME,OUT_TIME
                    FROM [Attendance] JOIN Client_data
                    ON [Attendance].c_id=Client_data.c_id
                    WHERE date={}
                    '''.format(dt)
                
                    )
        for i,row in enumerate(mysel):
            for j, value in enumerate(row):
                print(i,j,value)
                worksheet.write(i+1, j,value)
        print('report generated successfully and stored at preferred location')
        time.sleep(5)
        workbook.close()
    if(n==2):
        c_id=int(input('enter client id:'))
        n1=int(input("1.for retrieving clients activity on a particular date\n2.for retrieving clients activity in a date range\nenter your choice:"
                    )
              )
        if(n1==2):
            print('note: while entering date range from and to does not include those particular days so always give one day before for from date and one day after for to date')
            fd="'"+input('enter from date in yyyy-mm-dd format:')+"'"
            td="'"+input('enter to date in yyyy-mm-dd format:')+"'"
            ent=input('enter name for excel file:')
            root=Tk()
            root.withdraw()
            path = askdirectory(title='Select Folder') # shows dialog box and return the path
            workbook = Workbook('{}/{}.xlsx'.format(path,ent))
            worksheet = workbook.add_worksheet()
            ls=(['name',0],['mob no',0],['in time',0],['out time',0],['date',0])
            row=0
            col=0
            for x,y in ls:
                worksheet.write(row,col,x)
                print(row,col,x)
                col=col+1
            cur.execute('''
                        SELECT [Attendance].c_id,name,m_no,IN_TIME,OUT_TIME,date
                        FROM [Attendance] JOIN Client_data
                        ON [Attendance].c_id=Client_data.c_id
                        WHERE [Attendance].c_id={} AND date>{} AND date<{}
                        '''.format(c_id,fd,td)
                        )
            mysel=cur.execute('''
                        SELECT name,m_no,IN_TIME,OUT_TIME,date
                        FROM [Attendance] JOIN Client_data
                        ON [Attendance].c_id=Client_data.c_id
                        WHERE [Attendance].c_id={}  AND date>{} AND date<{};
                        '''.format(c_id,fd,td)
                
                        )
        if(n1==1):
            ent=input('enter name for excel file:')
            root=Tk()
            root.withdraw()
            path = askdirectory(title='Select Folder') # shows dialog box and return the path
            workbook = Workbook('{}/{}.xlsx'.format(path,ent))
            worksheet = workbook.add_worksheet()
            ls=(['client id',0],['name',0],['mob no',0],['in time',0],['out time',0])
            row=0
            col=0
            for x,y in ls:
                worksheet.write(row,col,x)
                col=col+1
            dt=input('enter date in yyyy-mm-dd format:')
            dt="'"+dt+"'"
            cur.execute('''
                        SELECT name,m_no,IN_TIME,OUT_TIME
                        FROM [Attendance] JOIN Client_data
                        ON [Attendance].c_id=Client_data.c_id
                        WHERE date={} AND [Attendance].c_id={}
                        '''.format(dt,c_id)
                        )
            mysel=cur.execute('''
                        SELECT [Attendance].c_id,name,m_no,IN_TIME,OUT_TIME
                        FROM [Attendance] JOIN Client_data
                        ON [Attendance].c_id=Client_data.c_id
                        WHERE date={} AND [Attendance].c_id={}
                        '''.format(dt,c_id)
                        )
            
        for i,row in enumerate(mysel):
            for j,value in enumerate(row):
                print(i,j,value)
                worksheet.write(i+1,j,value)
        print('report generated successfully and stored at preferred location')
        time.sleep(5)
        workbook.close()        
    return None
def pay_ent():
    os.system('cls')
    print('ABC GYM')
    c_id=int(input('enter client id:'))
    print('1.monthly substcription\n2.quarterly subscription\n3.half yearly subscription\n4.yearly subscription')
    n=int(input('enter your choice:'))
    l_d_p=datetime.datetime.now()
    l_d_p=l_d_p.strftime('%Y-%m-%d')
    l_d_p="'"+l_d_p+"'"
    if(n==1):
        cur.execute('''
                    SELECT date('now','+1 month') as "Date";
                    '''
                    )
    if(n==2):
         cur.execute('''
                    SELECT date('now','+3 month') as "Date";
                    '''
                    )
    if(n==3):
        cur.execute('''
                    SELECT date('now','+6 month') as "Date";
                    '''
                    )
    if(n==6):
        cur.execute('''
                    SELECT date('now','+12 month') as "Date";
                    '''
                    )
    n_d_p=cur.fetchall()
    ndp="'"+n_d_p[0][0]+"'"
    amt=int(input('enter amount paid'))
    cur.execute('''
                UPDATE Client_data SET l_d_p={},n_d_p={} WHERE(c_id={});
                '''.format(l_d_p,ndp,c_id)
                )
    conn.commit()
    cur.execute('''
                INSERT INTO Payhistory (c_id,amount,date) VALUES({},{},{})
                '''.format(c_id,amt,l_d_p)
                )
    conn.commit()
    
    
    return None
def ad_emp():
    os.system('cls')
    print('ABC GYM')
    name=str(input('enter name of new employee(this will be used as username):'))
    tp=str(input('0.employee account \n1.admin account\nenter your choice:'))
    pswd=str(input('set password:'))
    conpass=str(input('enter password again:'))
    if(pswd==conpass):
        name='\''+name+'\''
        pswd='\''+pswd+'\''
        tp='\''+tp+'\''
        cur.execute('''
                    INSERT INTO Users (u_name,u_pass,u_type)
                    VALUES ({},{},{});
                    '''.format(name,pswd,tp))
    
    else:
        print('passwords dont match!!!')
        ad_emp()
    conn.commit()
    return None
def ad_cl():
    os.system('cls')
    print('ABC GYM')
    name=input('enter client name:')
    name="'"+name+"'"
    m_no=input('enter mobile number of client:')
    m_no="'"+m_no+"'"
    doj=datetime.datetime.now()
    doj=doj.strftime('%Y-%m-%d')
    doj="'"+doj+"'"
    l_d_p="'addedlater'"
    n_d_p="'addedlater'"
    cur.execute('''
                SELECT p_no,p_name FROM Plan_data
                '''
                )
    pdata=cur.fetchall()
    for x,y in pdata:
        print(x,y)
    
    p_no=input('enter plan number:')
    p_no="'"+p_no+"'"
    cur.execute('''
                INSERT INTO Client_data (name,m_no,doj,p_no,l_d_p,n_d_p) VALUES ({},{},{},{},{},{})
                '''.format(name,m_no,doj,p_no,l_d_p,n_d_p))
    conn.commit()
    cur.execute('''
                SELECT c_id FROM Client_data ORDER BY c_id DESC LIMIT 1
                '''
                )
    c_id=cur.fetchall()
    
    print('Client added \nClient id is :{}'.format(c_id[0][0]))
    time.sleep(5)
    return None
def pl_data():
    print('ABC GYM')
    os.system('cls')
    name=input('enter name of plan :')
    sub_pm=int(input('enter subscription rate per month :'))
    name="'"+name+"'"
    cur.execute('''
                INSERT INTO Plan_data (p_name,sub_pm) VALUES ({},{})
                '''.format(name,sub_pm))
    conn.commit()
def pay_h():
    print('ABC GYM')
    os.system('cls')
    c_id=int(input('ENTER CLIENT ID TO RETRIEVE PAYMENT HISTORY:'))
    mysel=cur.execute('''
                 SELECT c_id,amount,date
                 FROM PayHistory WHERE c_id={}
                '''.format(c_id))
    for i,row in enumerate(mysel):
        count=1
        for j,value in enumerate(row):
            if(count==1):
                print('id:',value)
                count=count+1
                continue
            if(count==2):
                print('amount:',value)
                count=count+1
                continue
            if(count==3):
                print('date:',value)
                count=count+1
                continue
    inp=input('press enter to continue')
    if(inp=='\n'):
        return None
def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')    
def bckp():
    nm=input('enter name for backup file')
    nm=nm+'.sqlite'
    try:
        bckpconn= sqlite3.connect('{}'.format(nm))
        with bckpconn:
            conn.backup(bckpconn, pages=0, progress=progress)
        print("backup successful")
        time.sleep(5)
    except sqlite3.Error as error:
        print("Error while taking backup: ", error)
        time.sleep(5)
def resto():
    nm=input('enter name for backup file')
    nm=nm+'.sqlite'
    try:
        bckpconn= sqlite3.connect('{}'.format(nm))
        with bckpconn:
            bckpconn.backup(conn, pages=0, progress=progress)
        print("restore successful")
        time.sleep(5)
    except sqlite3.Error as error:
        print("Error while restoring: ", error)
        time.sleep(5)
def admin():
    #function to handle what admin wants to do
    while(1):
        os.system('cls')
        print(Fore.RED+'ABC GYM')
        print('ADMIN PANEL:')
        print('1.add client')
        print('2.add employee')
        print('3.make payment entry')
        print('4.mark attendance')
        print('5.retrieve attendance report')
        print('7.change password')
        print('8.add new plan')
        print('9.payment history')
        print('10.backup database')
        print('11.restore backup')
        print('12.logout')
        n=int(input('enter your choice:'))
        if(n==11):
            var=resto()
        if(n==10):
            var=bckp()
        if(n==9):
            var=pay_h()
        if(n==12):
            break
        if(n==8):
            var=pl_data()
        if(n==7):
            var=chg_pass()
        if(n==5):
            var=attd_rep()
        if(n==4):
            var=mk_attd2()
        if(n==3):
            var=pay_ent()
        if(n==2):
            var=ad_emp()
        if(n==1):
            var=ad_cl()
def emp():
    #function to handle what user wants to do
    while(1):
        os.system('cls')
        print(Fore.RED+'ABC GYM')
        print('EMPLOYEE PANEL:')
        print('1.mark attendance')
        print('2.logout')
        n=int(input('enter your choice:'))
        if(n==2):
            break
        if(n==1):
            var=mk_attd1()
                
def fun0():
    #function to handle login of users
    os.system('cls')
    print(Style.BRIGHT+Fore.RED+'WELCOME TO GYM MANAGEMENT SYSTEM')
    time.sleep(1)
    try:
        uname=list(input('enter username:'))
        uname.append('\'')
        uname.insert(0,'\'')
        uname=''.join(uname)    
        cur.execute('''
                        SELECT u_pass,u_type FROM Users WHERE u_name={}'''.format(uname))
        psd=cur.fetchall()
        pswd=getpass.getpass(prompt='Password:')
        if((psd[0][0])==pswd and (psd[0][1])==1):
            admin()
        elif((psd[0][0])==pswd and (psd[0][1])==0):
            emp()
    except:
        print('Invalid credentials')
        fun0()
    
def dbfun():
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Payhistory"
                ("c_id" INTEGER NOT NULL,
                "amount" INTEGER NOT NULL,
                "date" TEXT NOT NULL)
                '''
                )
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Attendance"
                (
                "c_id" INTEGER NOT NULL,
                "IN_TIME" TEXT NOT NULL,
                "OUT_TIME" TEXT NOT NULL,
                "date" TEXT NOT NULL
                );
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Client_data"
                (
                "c_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "name" TEXT NOT NULL,
                "m_no" NUMERIC NOT NULL,
                "doj" TEXT NOT NULL,
                "p_no" INTEGER NOT NULL,
                "l_d_p" TEXT NOT NULL,
                "n_d_p" TEXT NOT NULL
                );
                ''')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Plan_data"
                (
                "p_no" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                "p_name" TEXT NOT NULL,
                "sub_pm" NUMERIC NOT NULL,
                "p_desc" TEXT
                );
                '''
               )
    cur.execute('''
                CREATE TABLE IF NOT EXISTS "Users"
                (
                "u_name" TEXT NOT NULL UNIQUE,
                "u_pass" TEXT NOT NULL,
                "u_type" INTEGER NOT NULL,
                PRIMARY KEY("u_name")
                );
                '''
                )
    cur.execute('''
                SELECT COUNT(*) FROM Users;
                '''
                )
    var=cur.fetchall()
    if(var[0][0]==0):
        cur.execute('''
                    INSERT INTO Users (u_name,u_pass,u_type) VALUES('admin','admin','1');
                    '''
                    )
        cur.execute('''
                    INSERT INTO Users (u_name,u_pass,u_type) VALUES('user','user','0');
                    '''
                    )
        cur.execute('''
                    INSERT INTO Users (u_name,u_pass,u_type) VALUES('sudo','sudo','1');
                    '''
                    )
    conn.commit()    
dbfun()
def main():
    print(Back.WHITE)
    while(1):
        fun0()    
main()
