import psycopg2
import datetime
from datetime import date
import calendar
import os
import pandas as pd
from tabulate import tabulate
from collections import deque



def findTuple(vocab,results):
    for result in results:
        if vocab == result[1]:
            return result

#####################################################################
#connect to Database
connection = psycopg2.connect(
    database="wordbank",
    user="nan",
    password="ninan0805"
)

if(connection):
    print("connect to database successfully")

#open up a cursor
cursor = connection.cursor()
column_names = ['ID','Vocab','Definition','Usage','Reference','Affiliation','Date']
#####################################################################
prereference = ''
terminator = True
while(terminator):
    command = input(">>").split()

    if(len(command) == 0):
        continue
    elif(command[0] == 'add'):
        # take input from user
        vocab = input("vocabulary: ")
        definition = input("definition: ")
        usage = input("usage: ")
        reference = input("reference: ")
        while (len(reference) == 0):
            if (len(prereference) == 0):
                print("please enter a reference")
                reference = input("reference: ")
            else:
                reference = prereference

        prereference = reference

        affiliation = input("affiliation: ")

        if(len(affiliation) == 0):
            affiliation = 'N/A'


        cursor.execute("Select count(id) from word")
        num = cursor.fetchall()
        val = num[0][0]
        val = val + 1
        print(val)
        sql = "INSERT INTO word(ID,vocab,definition,usage,reference,affiliation,date) VALUES (%s,%s,%s,%s,%s,%s,%s) returning *"
        cursor.execute(sql,(val,vocab,definition,usage,reference,affiliation,date.today()))
        results = cursor.fetchall()
        print(results)
        #close the cursor
        connection.commit()
    elif(command[0] == 'delete' and len(command)>1):
        sql = "select id from word where vocab = %s order by date DESC"
        cursor.execute(sql,(command[1],))
        id = cursor.fetchall()
        id = id[0][0]
        sql = "delete from word where id = %s"
        cursor.execute(sql,(id,))
        connection.commit()
    elif(command[0] == 'edit' and len(command)>1 and len(command)<4):

        sql = "SELECT id from word where vocab = %s order by date DESC"
        cursor.execute(sql, (command[1],))
        most_recent = cursor.fetchall()

        if (len(most_recent) == 0):
            print("vocab not found,please re-enter")

        elif(len(command) == 2):
            id = most_recent[0][0]
            vocab = input("vocabulary: ")
            definition = input("definition: ")
            usage = input("usage: ")
            reference = input("reference: ")
            affiliation = input("affiliation: ")
            sql = "Update WORD SET vocab = %s,definition = %s,usage = %s,reference = %s,affiliation = %s where id = %s"
            cursor.execute(sql,(vocab,definition,usage,reference,affiliation,id))
        else:
            id = most_recent[0][0]
            if(command[2] == 'definition'):
                definition = input("definition: ")
                sql = "Update WORD SET definition = %s where id = %s"
                cursor.execute(sql, (definition,id))

            elif(command[2] == 'usage'):
                usage = input("usage: ")
                sql = "Update WORD SET usage = %s where id = %s"
                cursor.execute(sql, (usage, id))
            elif(command[2] == 'reference'):
                reference = input("reference: ")
                sql = "Update WORD SET reference = %s where id = %s"
                cursor.execute(sql, (reference, id))
            elif(command[2] == 'affiliation'):
                affiliation = input("affiliation: ")
                sql = "Update WORD SET affiliation = %s where id = %s"
                cursor.execute(sql, (affiliation, id))
            else:
                print("command not found,please re-enter the following: --add --edit -- weekly -- monthly -- yearly --common --quit")
        connection.commit()

    elif(command[0] == 'daily'):
        my_date = datetime.date.today()
        sql = 'select * from word where date = %s'
        cursor.execute(sql,(my_date,))
        results = cursor.fetchall()

        df = pd.DataFrame(results,columns=column_names)
        if(len(command) > 1):
            print(tabulate(df,headers='keys',tablefmt='psql'))
        else:
            for result in results:
                print(result[1])
    elif(command[0] == 'weekly'):
        my_date = datetime.date.today()
        year, week_num, day_of_week = my_date.isocalendar()
        startM = date.fromisocalendar(year,week_num,1)
        endS = date.fromisocalendar(year,week_num,7)
        sql = "Select * from word where date > %s and date < %s"
        cursor.execute(sql,(startM,endS))
        results = cursor.fetchall()
        df = pd.DataFrame(results,columns=column_names)
        if(len(command) > 1):
            print(tabulate(df,headers='keys',tablefmt='psql'))
        else:
            for result in results:
                print(result[1])

    elif(command[0] == 'monthly'):
        start = date(date.today().year, date.today().month, 1)
        end = date(date.today().year, date.today().month, calendar.monthrange(date.today().year,date.today().month)[1])
        sql = "Select * from word where date > %s and date < %s"
        cursor.execute(sql, (start, end))
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=column_names)
        if (len(command) > 1):
            print(tabulate(df, headers='keys', tablefmt='psql'))
        else:
            for result in results:
                print(result[1])
        #show words for this month
    elif(command[0] == 'yearly'):
        start = date(date.today().year, 1, 1)
        end = date(date.today().year, 12, 31)
        sql = "Select * from word where date > %s and date < %s"
        cursor.execute(sql, (start, end))
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=column_names)
        if (len(command) > 1):
            print(tabulate(df, headers='keys', tablefmt='psql'))
        else:
            for result in results:
                print(result[1])
        #show words for this year
    elif(command[0] == 'common'):
        print("to be debugged")
        # sql = "select vocab,definition,usage,reference,affiliation from (select vocab,count(*) from word GROUP BY vocab) inner join word on vocab = vocab where count > 1"
        # cursor.execute(sql)
        # results = cursor.fetchall()
        # print(results)
        #show word appears more than once
    elif(command[0] == 'review'):
        if(len(command) > 1):
            if(command[1] == 'daily'):
                my_date = datetime.date.today()
                if(len(command)>2):
                    if(command[2] == '-1'):
                        my_date = my_date - datetime.timedelta(days = 1)

                sql = 'select * from word where date = %s'
                cursor.execute(sql, (my_date,))
                results = cursor.fetchall()
                df = pd.DataFrame(results, columns=column_names)
                Uword = deque([result[1] for result in results])

                while(Uword):
                    uword = Uword.pop()
                    check = input(uword + ": ")
                    if(check == 'y'):
                        continue
                    elif(check == uword):
                        continue
                    else:
                        sql = "select * from word where vocab = %s and date = %s"
                        cursor.execute(sql,(uword,my_date))
                        re = cursor.fetchall()
                        df_sub = pd.DataFrame(re,columns=column_names)
                        print(tabulate(df_sub, headers='keys', tablefmt='psql'))
                        Uword.appendleft(uword)

            elif(command[1] == 'weekly'):
                print("to be implement")
            elif(command[1] == 'monthly'):
                print("to be implement")
            else:
                print("please enter daily,weekly or monthly")

    elif(command[0] == 'quit'):
        terminator = False
    elif(command[0] == 'clear'):
        os.system("clear")
    else:
        sql = "select * from word where vocab = %s"
        cursor.execute(sql,(command[0],))
        results = cursor.fetchall()
        if(len(results) == 0):
            print("vocab not found within WordBank")
        else:
            df = pd.DataFrame(results,columns = column_names)
            print(tabulate(df,headers='keys', tablefmt='psql'))
        #print("command not found,please re-enter the following: --add --edit -- weekly -- monthly -- yearly --common --quit")

###################################################################

cursor.close()
connection.close()