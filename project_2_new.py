from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
import requests
import pymysql
import json
import pandas as pd
from sqlalchemy import create_engine
import functools
import operator
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
CORS(app)
app.config["CORS_SUPPORTS_CREDENTIALS"] = True



db = pymysql.connect(host="127.0.0.1",user = "root",password= "Qwerty123",database = "edfs" )
cursor = db.cursor()
db_data = 'mysql+pymysql://' + 'root' + ':' + 'Qwerty123' + '@' + 'localhost' + ':3306/' \
       + 'edfs' + '?charset=utf8mb4'

engine = create_engine(db_data)


@app.route("/mkdir/<path:name>", methods = ['POST', 'GET','DELETE','PUT'])
def make_directory(name):
    if request.method == "POST":
        # bar = request.args.to_dict()
        lst = []
        name = "/" + name
        temp = name.split("/")
        current_name="/"+temp[-1]
        #parent_name="/"+temp[-2]
        #print("parent",parent_name)
        print("current",current_name)
        path = ""
        for i in range(0,len(temp)-1):
            path = path + "/" + temp[i]
        anscestral_path=path[1:]
        
        
        print("parent",anscestral_path)
        file_directory="Directory"

          
        if anscestral_path==None or len(temp)<=2 :
            sql = "select count(*) from FS_Structure where name = '%s' and Ancestral_path='%s'" %(current_name,anscestral_path)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            count=results[0][0]
            print(count)
            if count==0:
                print("1",anscestral_path)
                root_id=1
                parent_id=0
                current_id = 1
            #file_directory="Directory"
                sql = "insert into FS_Structure(Root_id,Parent_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%s','%s','%s')" %(root_id,parent_id,current_id,current_name,anscestral_path,file_directory)
                cursor.execute(sql)
                db.commit()
                print("2",temp)
            else:
                print("Directory already exsits")     
        if len(temp)>2:
            n=len(temp)
            anscestral_path="/"+temp[n-2]
            print("1",anscestral_path)
            sql = "select count(*) from FS_Structure where name = '%s' and Ancestral_path='%s'" %(current_name,anscestral_path)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            count=results[0][0]
            print(count)
            if count==0:
                sql = "select max(current_id)+1 from FS_Structure" #where name = '%s'" %(anscestral_path)
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                current_id=results[0][0]
            #current_id=1
                child_id=None
                root_id=1
                sql = "select current_id from FS_Structure where name = '%s'" %(anscestral_path)
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                parent_id=results[0][0]
                print(parent_id)
                print(root_id,parent_id,child_id,current_id,current_name,anscestral_path,file_directory)
            
            
                sql = "insert into FS_Structure(Root_id,Parent_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%s','%s','%s')" %(root_id,parent_id,current_id,current_name,anscestral_path,file_directory)
                cursor.execute(sql)
                db.commit()
                sql="select current_id from FS_Structure where name='%s'" %(current_name)
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                child_id=results[0][0]
                sql = "select count(*) from FS_Structure where Ancestral_path = '%s'" %(anscestral_path)
                cursor.execute(sql)
                results = cursor.fetchall()
                print("count",results)
            
                if results[0][0]>1:
                    print("check",anscestral_path)
                    sql = "select child_id from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    child_id_prev=results[0][0]
                    print("check2",anscestral_path)
                    root_id_prev=0
                    sql = "select Parent_id from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    parent_id_prev=results[0][0]
                    print("check3",anscestral_path)
                    sql = "select current_id from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    current_id_prev=results[0][0]
                    print("check4",anscestral_path)
                    sql = "select name from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    name_prev=results[0][0]
                    print("check5",anscestral_path)
                    sql = "select Ancestral_path from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    anscestral_path_prev=results[0][0]
                    print("check6",anscestral_path)
                    sql = "select File_or_Directory from FS_Structure where name = '%s'" %(anscestral_path)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    File_Directory_prev=results[0][0]
                    print("3","entering reduntant row")
                
                    sql = "insert into FS_Structure(Root_id,Parent_id,Child_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%d','%s','%s','%s')" %(root_id_prev,parent_id_prev,current_id,current_id_prev,name_prev,anscestral_path_prev,File_Directory_prev)
                    cursor.execute(sql)
                    db.commit()
            
                sql="update FS_Structure set child_id='%d' where name = '%s' and root_id='%d'" %(child_id,anscestral_path,1)
                cursor.execute(sql)
                db.commit()
            else:
                print("Directory already exsits") 
         
        print("Directory creation is been handled")
        return "Directory creation is been handled"     
    else:
        print("Wrong Request Call for mkdir "+name+", Expected POST")
        return "Wrong Request Call for mkdir "+name+", Expected POST"


@app.route("/ls/<path:name>", methods = ['POST', 'GET','DELETE','PUT'])
def get_files(name):
    if request.method == "GET":
        lst = []
        name = "/" + name
        temp = name.split("/")
        path = ""
        for i in range(0,len(temp)-1):
            path = path + "/" + temp[i]
        print(path[1:len(path)])
        # sql = "select * from test where name = '%s'" %name
        sql = "select name from FS_Structure where Ancestral_path = '%s'" %(name)
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        # print(len(results))
        if len(results) == 0:
            sql = "select count(*) from FS_structure where name = '%s' AND Ancestral_path = '%s'" %("/"+temp[-1],path[1:len(path)])
            cursor.execute(sql)
            cnt = cursor.fetchone()
            if cnt[0] > 0:
                return {'files in '+name: "Directory empty"}
            else:
                return {'files in '+name: "No such directory"}
        db.commit()
        for i in results:
            for j in i:
                lst.append(j)
        # if len(lst) == 0:
        #     return {'files in '+name: "Directory empty"}
        res = {'files in '+name: json.dumps(list(set(lst)))}
        print(res)
        return res
    else:
        print("Wrong Request Call for ls "+name+", Expected GET")
        return "Wrong Request Call for ls "+name+", Expected GET"


@app.route("/cat/<path:name>", methods = ['POST','GET','DELETE','PUT'])
def get_file_contents(name):
    if request.method == "GET":
        temp = name.split("/")
        path = ""
        for i in range(0,len(temp)-1):
            path = path + "/" + temp[i]
        # sql = "Select Current_id from FS_Structure where Ancestral_Path = '%s' and name = '%s' and File_or_Directory = 'File'" %(path,temp[-1])
        # cursor.execute(sql)
        # results = cursor.fetchone()
        # if results == None:
            # return "No such file"
        print(name)
        sql = "Select content from partition_file where file_name = '%s'" %(name)
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        print(type(result))
        s = ''.join(result)
        print(type(s))
        # res = json.dumps(result,default=str)
        return s
    else:
        print("Wrong Request Call for cat "+name+", Expected GET")
        return "Wrong Request Call for cat "+name+", Expected GET"


@app.route("/rm/<path:name>", methods = ['POST','GET','DELETE','PUT'])
def delete_file(name):
    if request.method == "DELETE":
        print(name)
        temp = name.split("/")
        path = ""
        for i in range(0,len(temp)-1):
            path = path + "/" + temp[i]
        sql = "Select Current_id from FS_Structure where Ancestral_Path = '%s' and name = '%s' and File_or_Directory = 'File'" %(path,temp[-1])
        cursor.execute(sql)
        results = cursor.fetchone()
        sql = "delete from partition_file where file_name = '%s'" %(temp[-1])
        cursor.execute(sql)
        db.commit()
        sql = "delete from FS_Structure where name = '%s' and Ancestral_path = '%s' and File_or_Directory = 'File'" %(temp[-1],path)
        cursor.execute(sql)
        db.commit()
        sql = "delete from FS_Structure where Child_id = '%d'" %(results[0])
        cursor.execute(sql)
        db.commit()
        print("File "+name+" has been deleted")
        return "File "+name+" has been deleted"
    else:
        print("Wrong Request Call for rm "+name+", Expected DELETE")
        return "Wrong Request Call for rm "+name+", Expected DELETE"


@app.route("/put/<name>/<path:dirname>/<numpart>", methods = ['POST','GET','DELETE','PUT'])
def upload_file(name,dirname,numpart):
    if request.method == "PUT":
        print(name)
        print(dirname)
        print(numpart)
        # sql = ""
        # cursor.execute(sql)
        # db.commit()
        temp = name.split(".")
        print(temp[1])
        format=temp[1]
        print(format)
        print(type(format))
        if format != "csv" and format != "txt":
            return "File format is not valid. Enter .csv or .txt file"
        if format == "csv" or format == "txt":
            directory="/"+dirname
            dir =directory.split("/")
            parent=dir[-1]
            parent_name="/"+parent
            print("parent", parent)
            print("parent_name",parent_name)
            print(name)
            file_directory="file"
            sql = "select count(*) from FS_Structure where name = '%s' and Ancestral_path='%s'" %(name,parent_name)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            count=results[0][0]
            print(count)
            if count==0:
                sql = "select max(current_id)+1 from FS_Structure" #where name = '%s'" %(anscestral_path)
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                current_id=results[0][0]
        #current_id=1
                child_id=None
                root_id=1
                sql = "select current_id from FS_Structure where name = '%s'" %(parent_name)
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                parent_id=results[0][0]
                print(parent_id)
                print(root_id, parent_id, child_id, current_id, name, parent_name, file_directory)
        
        
                sql = "insert into FS_Structure(Root_id,Parent_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%s','%s','%s')" %(root_id,parent_id,current_id,name,parent_name,file_directory)
                cursor.execute(sql)
                db.commit()
                #sql="select current_id from FS_Structure where name='%s' and where Ancestral_path='%s'" %(name,parent_name)
                print(name)
                print(parent_name)
                sql = "select current_id from FS_Structure where name='%s' and Ancestral_path='%s'" % (name,parent_name)
           # else:
            #    print("File exists")
             #   return "File exists"
                cursor.execute(sql)
                results = cursor.fetchall()
                print(results)
                child_id=results[0][0]
                print("child_id",child_id)
                sql = "select count(*) from FS_Structure where Ancestral_path = '%s'" %(parent_name)
                cursor.execute(sql)
                results = cursor.fetchall()
                print("count",results)
        
                if results[0][0]>1:
                    print("check",parent_name)
                    sql = "select child_id from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    child_id_prev=results[0][0]
                    print(child_id_prev)
                    print("check2",parent_name)
                    root_id_prev=0
                    sql = "select Parent_id from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    parent_id_prev=results[0][0]
                    print(parent_id_prev)
                    print("check3",parent_name)
                    sql = "select current_id from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    current_id_prev=results[0][0]
                    print(current_id_prev)
                    print("check4",parent_name)
                    sql = "select name from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    name_prev=results[0][0]
                    print(name_prev)
                    print("check5",parent_name)
                    sql = "select Ancestral_path from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    anscestral_path_prev=results[0][0]
                    print(anscestral_path_prev)
                    print("check6",parent_name)
                    sql = "select File_or_Directory from FS_Structure where name = '%s'" %(parent_name)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    File_Directory_prev=results[0][0]
                    print("3","entering reduntant row")
            
                    sql = "insert into FS_Structure(Root_id,Parent_id,Child_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%d','%s','%s','%s')" %(root_id_prev,parent_id_prev,current_id,current_id_prev,name_prev,anscestral_path_prev,File_Directory_prev)
                    cursor.execute(sql)
                    db.commit()
        
                    sql="update FS_Structure set child_id='%d' where name = '%s' and root_id='%d'" %(child_id,parent_name,1)
                    cursor.execute(sql)
                    db.commit()
            else:
                print("File exists")
                return "File exists"
        else:
            print("File format is not valid. Enter .csv or .txt file ")
            return "File format is not valid. Enter .csv or .txt file"
         
        print("File insert handled ")
        
        if format == "txt":
            f = open(name, "r")
            # print(f.read())
            a = f.read()
            print(a)
            sql = "insert into partition_file(file_name,content) values('%s','%s')" %(name,a)
            cursor.execute(sql)
            db.commit()
            


        
        if name == "match_data.csv":
            df = pd.read_csv(name)
            print("inserting data file to table")
            df.to_sql('match_data', engine, if_exists = 'replace', index=False)
            sql = "DROP table if exists match_data_1304071"
            cursor.execute(sql)
            db.commit()
            sql = "DROP table if exists match_data_1304096"
            cursor.execute(sql)
            db.commit()
            sql = "DROP table if exists match_data_1312200"
            cursor.execute(sql)
            db.commit()
            sql = "CREATE TABLE `match_data_1304071` (\
                    `ID` int DEFAULT NULL,\
                    `City` varchar(100) DEFAULT NULL,\
                    `Date` date DEFAULT NULL,\
                    `Season` year DEFAULT NULL,\
                    `MatchNumber` varchar(100) DEFAULT NULL,\
                    `Team1` varchar(100) DEFAULT NULL,\
                    `Team2` varchar(100) DEFAULT NULL,\
                    `Venue` varchar(100) DEFAULT NULL,\
                    `TossWinner` varchar(100) DEFAULT NULL,\
                    `TossDecision` varchar(100) DEFAULT NULL,\
                    `SuperOver` varchar(100) DEFAULT NULL,\
                    `WinningTeam` varchar(100) DEFAULT NULL,\
                    `WonBy` varchar(100) DEFAULT NULL,\
                    `Margin` int DEFAULT NULL,\
                    `method` varchar(10) DEFAULT NULL,\
                    `Player_of_Match` varchar(100),\
                    `Umpire1` varchar(100),\
                    `Umpire2` varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()

            sql = "insert into match_data_1304071 select * from match_data where  ID> 1304046 and ID<=1304071" 
            cursor.execute(sql)
            db.commit()
            sql="insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("match_data.csv","match_data_1304071",1)
            cursor.execute(sql)
            db.commit()
            print("inserted p1")
            sql = "CREATE TABLE `match_data_1304096` (\
                    `ID` int DEFAULT NULL,\
                    `City` varchar(100) DEFAULT NULL,\
                    `Date` date DEFAULT NULL,\
                    `Season` year DEFAULT NULL,\
                    `MatchNumber` varchar(100) DEFAULT NULL,\
                    `Team1` varchar(100) DEFAULT NULL,\
                    `Team2` varchar(100) DEFAULT NULL,\
                    `Venue` varchar(100) DEFAULT NULL,\
                    `TossWinner` varchar(100) DEFAULT NULL,\
                    `TossDecision` varchar(100) DEFAULT NULL,\
                    `SuperOver` varchar(100) DEFAULT NULL,\
                    `WinningTeam` varchar(100) DEFAULT NULL,\
                    `WonBy` varchar(100) DEFAULT NULL,\
                    `Margin` int DEFAULT NULL,\
                    `method` varchar(10) DEFAULT NULL,\
                    `Player_of_Match` varchar(100),\
                    `Umpire1` varchar(100),\
                    `Umpire2` varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()
            sql = "insert into match_data_1304096 select * from match_data where id> 1304071 and id<=1304096;" 
            cursor.execute(sql)
            db.commit()
            sql = "insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("match_data.csv", "match_data_1304096", 2)
            cursor.execute(sql)
            db.commit()
            print("inserted p2")
            sql = "CREATE TABLE `match_data_1312200` (\
                    `ID` int DEFAULT NULL,\
                    `City` varchar(100) DEFAULT NULL,\
                    `Date` date DEFAULT NULL,\
                    `Season` year DEFAULT NULL,\
                    `MatchNumber` varchar(100) DEFAULT NULL,\
                    `Team1` varchar(100) DEFAULT NULL,\
                    `Team2` varchar(100) DEFAULT NULL,\
                    `Venue` varchar(100) DEFAULT NULL,\
                    `TossWinner` varchar(100) DEFAULT NULL,\
                    `TossDecision` varchar(100) DEFAULT NULL,\
                    `SuperOver` varchar(100) DEFAULT NULL,\
                    `WinningTeam` varchar(100) DEFAULT NULL,\
                    `WonBy` varchar(100) DEFAULT NULL,\
                    `Margin` int DEFAULT NULL,\
                    `method` varchar(10) DEFAULT NULL,\
                    `Player_of_Match` varchar(100),\
                    `Umpire1` varchar(100),\
                    `Umpire2` varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()
            sql = "insert into match_data_1312200 select * from match_data where id> 1304096 and id<=1312200;" 
            cursor.execute(sql)
            db.commit()
            sql = "insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("match_data.csv", "match_data_1312200", 3)
            cursor.execute(sql)
            db.commit()
            print("inserted p3")
        elif name == "ball_data.csv":
            df = pd.read_csv(name)
            print("inserting data file to table")
            df.to_sql('ball_data', engine, if_exists = 'replace', index=False)
            sql = "DROP table if exists ball_data_1304071"
            cursor.execute(sql)
            db.commit()
            sql = "DROP table if exists ball_data_1304096"
            cursor.execute(sql)
            db.commit()
            sql = "DROP table if exists ball_data_1312200"
            cursor.execute(sql)
            db.commit()
            sql = "CREATE TABLE `ball_data_1304071` (\
                    ID int(50),\
                    Innings int(50),\
                    Overs int(50),\
                    ballnumber int(50),\
                    Batter varchar(100),\
                    Bowler varchar(100),\
                    non_striker varchar(100),\
                    extra_type varchar(100),\
                    batsman_run int(50),\
                    extras_run int(50),\
                    total_run int(50),\
                    non_boundary int(50),\
                    isWicketDelivery varchar(100),\
                    player_out varchar(100),\
                    Kind varchar(100),\
                    fielders_involved varchar(100),\
                    BattingTeam varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()
            sql = "insert into ball_data_1304071 select * from ball_data where  ID> 1304046 and ID<=1304071" 
            cursor.execute(sql)
            db.commit()
            sql = "insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("ball_data.csv", "ball_data_1304071", 1)
            cursor.execute(sql)
            db.commit()
            print("inserted p1")
            sql = "CREATE TABLE `ball_data_1304096` (\
                    ID int(50),\
                    Innings int(50),\
                    Overs int(50),\
                    ballnumber int(50),\
                    Batter varchar(100),\
                    Bowler varchar(100),\
                    non_striker varchar(100),\
                    extra_type varchar(100),\
                    batsman_run int(50),\
                    extras_run int(50),\
                    total_run int(50),\
                    non_boundary int(50),\
                    isWicketDelivery varchar(100),\
                    player_out varchar(100),\
                    Kind varchar(100),\
                    fielders_involved varchar(100),\
                    BattingTeam varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()
            sql = "insert into ball_data_1304096 select * from ball_data where id> 1304071 and id<=1304096;" 
            cursor.execute(sql)
            db.commit()
            sql = "insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("ball_data.csv", "ball_data_1304096", 2)
            cursor.execute(sql)
            db.commit()
            print("inserted p2")
            sql = "CREATE TABLE `ball_data_1312200` (\
                    ID int(50),\
                    Innings int(50),\
                    Overs int(50),\
                    ballnumber int(50),\
                    Batter varchar(100),\
                    Bowler varchar(100),\
                    non_striker varchar(100),\
                    extra_type varchar(100),\
                    batsman_run int(50),\
                    extras_run int(50),\
                    total_run int(50),\
                    non_boundary int(50),\
                    isWicketDelivery varchar(100),\
                    player_out varchar(100),\
                    Kind varchar(100),\
                    fielders_involved varchar(100),\
                    BattingTeam varchar(100)\
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
            cursor.execute(sql)
            db.commit()
            sql = "insert into ball_data_1312200 select * from ball_data where id> 1304096 and id<=1312200;" 
            cursor.execute(sql)
            db.commit()

            sql = "insert into partition_file(file_name,table_name,partitions) values('%s','%s','%d')" % ("ball_data.csv", "ball_data_1312200", 3)
            cursor.execute(sql)
            db.commit()

            print("inserted p3")



        print("File "+name+" has been uploaded to directory /"+dirname)
        return "File "+name+" has been uploaded to directory /"+dirname
    else:
        print("Wrong Request Call for put "+name+", Expected PUT")
        return "Wrong Request Call for put "+name+", Expected PUT"


@app.route("/getPartitionLocations/<name>", methods = ['POST','GET','DELETE','PUT'])
def getPartition(name):
    if request.method == "GET":
        lst = []
        sql = "select partitions from partition_file where file_name = '%s'" %(name)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if len(results) == 0:
            return name +" does not exist"
        for i in results:
            lst.append(int(i[0][0]))
        res = {'Partition Locations of ' +name: json.dumps(list(set(lst)))}
        print(res)
        return res
    else:
        print("Wrong Request Call for getPartitionLocations "+name+", Expected GET")
        return "Wrong Request Call for getPartitionLocations "+name+", Expected GET"

@app.route("/readPartition/<name>/<partnum>", methods = ['POST','GET','DELETE','PUT'])
def readPartition(name,partnum):
    if request.method == "GET":
        print(name)
        print(partnum)
        sql = "select table_name from partition_file where file_name = '%s' and partitions = '%s'" %(name,partnum)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results[0][0])
        if len(results) == 0:
            return "Does not exist"
        sql = "select * from " +results[0][0]
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        res = json.dumps(results,indent=4, sort_keys=True, default=str)
        return res
    else:
        print("Wrong Request Call for readPartition "+name+", Expected GET")
        return "Wrong Request Call for readPartition "+name+", Expected GET"

# @app.route("/mapPartition/<query>", methods = ['POST','GET','DELETE','PUT'])
# def executequery(query):
#     if request.method == "GET":
#         partitionnumlst = []
#         map1 = []
#         map2 = []
#         map3 = []
#         reducefinal = []
#         final = []
#         cnt = 1
#         sql = query
#         temp = query.split(" ")
#         if "match_data" in temp:
#             t1 = query.split("match_data")
#             print(t1)
#             sql = "select table_name from partition_file where file_name = 'match_data.csv'"
#             cursor.execute(sql)
#             results = cursor.fetchall()
#             for i in results:
#                 print(i[0])
#                 sql = t1[0]+i[0]+t1[1]
#                 print(sql)
#                 cursor.execute(sql)
#                 results = cursor.fetchall()
#                 if len(results) != 0:
#                     sql = "select partitions from partition_file where table_name = '%s'" %(i[0])
#                     cursor.execute(sql)
#                     r = cursor.fetchone()
#                     partitionnumlst.append(r[0])
#                     if cnt == 1:
#                         map1.append(results)
#                         print(map1)
#                         map1 = functools.reduce(operator.iconcat, map1, [])
#                     elif cnt == 2:
#                         map2.append(results)
#                         map2 = functools.reduce(operator.iconcat, map2, [])
#                     elif cnt == 3:
#                         map3.append(results)
#                         map3 = functools.reduce(operator.iconcat, map3, [])
#                 cnt = cnt + 1
#             print(map1)
#             print()
#             print(map2)
#             print()
#             print(map3)
#             print()
#             reducefinal = map1+map2+map3
#
#             print(reducefinal)
#             res1 = {'Mapper1 ': json.dumps(functools.reduce(operator.iconcat, map1, []))}
#             res2 = {'Mapper2 ': json.dumps(functools.reduce(operator.iconcat, map2, []))}
#             res3 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, map3, []))}
#             res4 = {'Reducer ': json.dumps(functools.reduce(operator.iconcat, reducefinal, []))}
#             res5 = {'Partitions Read ': json.dumps(list(partitionnumlst))}
#             final.append(res1)
#             final.append(res2)
#             final.append(res3)
#             final.append(res4)
#             final.append(res5)
#             final = json.dumps(final,indent=4, sort_keys=True, default=str)
#             return final
#
#         elif 'ball_data' in temp:
#             t1 = query.split("ball_data")
#             print(t1)
#             sql = "select table_name from partition_file where file_name = 'ball_data.csv'"
#             cursor.execute(sql)
#             results = cursor.fetchall()
#             for i in results:
#                 print(i[0])
#                 sql = t1[0]+i[0]+t1[1]
#                 print(sql)
#                 cursor.execute(sql)
#                 results = cursor.fetchall()
#                 if len(results) != 0:
#                     sql = "select partitions from partition_file where table_name = '%s'" %(i[0])
#                     cursor.execute(sql)
#                     r = cursor.fetchone()
#                     partitionnumlst.append(r[0])
#                     if cnt == 1:
#                         map1.append(results)
#                         map1 = functools.reduce(operator.iconcat, map1, [])
#                     elif cnt == 2:
#                         map2.append(results)
#                         map2 = functools.reduce(operator.iconcat, map2, [])
#                     elif cnt == 3:
#                         map3.append(results)
#                         map3 = functools.reduce(operator.iconcat, map3, [])
#                 cnt = cnt + 1
#             print(map1)
#             print()
#             print(map2)
#             print()
#             print(map3)
#             print()
#             reducefinal = map1+map2+map3
#
#             print(reducefinal)
#             res1 = {'Mapper1 ': json.dumps(functools.reduce(operator.iconcat, map1, []))}
#             res2 = {'Mapper2 ': json.dumps(functools.reduce(operator.iconcat, map2, []))}
#             res3 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, map3, []))}
#             res4 = {'Reducer ': json.dumps(functools.reduce(operator.iconcat, reducefinal, []))}
#             res5 = {'Partitions Read ': json.dumps(list(partitionnumlst))}
#             final.append(res1)
#             final.append(res2)
#             final.append(res3)
#             final.append(res4)
#             final.append(res5)
#             final = json.dumps(final,indent=4, sort_keys=True, default=str)
#             return final
#
#     else:
#         print("Wrong Request Call, Expected GET")
#         return "Wrong Request Call, Expected GET"
#

@app.route("/mapPartition/<query>", methods = ['POST','GET','DELETE','PUT'])
def executequery(query):
    if request.method == "GET":
        partitionnumlst = []
        map1 = []
        map2 = []
        map3 = []
        reducefinal = []
        final = []
        cnt = 1
        sql = query
        temp = query.split(" ")
        if "match_data" in temp:
            t1 = query.split("match_data")
            print(t1)
            sql = "select table_name from partition_file where file_name = 'match_data.csv'"
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                print(i[0])
                sql = t1[0]+i[0]+t1[1]
                print(sql)
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) != 0:
                    sql = "select partitions from partition_file where table_name = '%s'" %(i[0])
                    cursor.execute(sql)
                    r = cursor.fetchone()
                    partitionnumlst.append(r[0])
                    if cnt == 1:
                        map1.append(results)
                        print(map1)
                        map1 = functools.reduce(operator.iconcat, map1, [])
                    elif cnt == 2:
                        map2.append(results)
                        map2 = functools.reduce(operator.iconcat, map2, [])
                    elif cnt == 3:
                        map3.append(results)
                        map3 = functools.reduce(operator.iconcat, map3, [])
                cnt = cnt + 1
            print(map1)
            print()
            print(map2)
            print()
            print(map3)
            print()

            mapfinal = map1+map2+map3
            print(dict(map1))
            # print(mapfinal)
            # print(dict(mapfinal))
            reducefinal = {}
            for d in dict(map1).keys():
                    reducefinal[d] = reducefinal.get(d, 0) + dict(map1)[d]
            for d in dict(map2).keys():
                    reducefinal[d] = reducefinal.get(d, 0) + dict(map2)[d]
            for d in dict(map3):
                    reducefinal[d] = reducefinal.get(d, 0) + dict(map3)[d]
            print(reducefinal)

            print(reducefinal)
            res1 = {'Mapper1 ': json.dumps(functools.reduce(operator.iconcat, map1, []))}
            res2 = {'Mapper2 ': json.dumps(functools.reduce(operator.iconcat, map2, []))}
            res3 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, map3, []))}
            res4 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, mapfinal, []))}
            res5 = {'Reducer ': json.dumps(functools.reduce(operator.iconcat, reducefinal, []))}
            res6 = {'Partitions Read ': json.dumps(list(partitionnumlst))}
            final.append(res1)
            final.append(res2)
            final.append(res3)
            final.append(res4)
            final.append(res5)
            final.append(res6)
            final = json.dumps(final,indent=4, sort_keys=True, default=str)
            return final

        elif 'ball_data' in temp:
            t1 = query.split("ball_data")
            print(t1)
            sql = "select table_name from partition_file where file_name = 'ball_data.csv'"
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                print(i[0])
                sql = t1[0]+i[0]+t1[1]
                print(sql)
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) != 0:
                    sql = "select partitions from partition_file where table_name = '%s'" %(i[0])
                    cursor.execute(sql)
                    r = cursor.fetchone()
                    partitionnumlst.append(r[0])
                    if cnt == 1:
                        map1.append(results)
                        map1 = functools.reduce(operator.iconcat, map1, [])
                    elif cnt == 2:
                        map2.append(results)
                        map2 = functools.reduce(operator.iconcat, map2, [])
                    elif cnt == 3:
                        map3.append(results)
                        map3 = functools.reduce(operator.iconcat, map3, [])
                cnt = cnt + 1
            print(map1)
            print()
            print(map2)
            print()
            print(map3)
            print()
            mapfinal = map1 + map2 + map3
            reducefinal = {}
            for d in mapfinal:
                for k in d.keys():
                    reducefinal[k] = reducefinal.get(k, 0) + d[k]

            print(reducefinal)
            res1 = {'Mapper1 ': json.dumps(functools.reduce(operator.iconcat, map1, []))}
            res2 = {'Mapper2 ': json.dumps(functools.reduce(operator.iconcat, map2, []))}
            res3 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, map3, []))}
            res4 = {'Mapper3 ': json.dumps(functools.reduce(operator.iconcat, mapfinal, []))}
            res5 = {'Reducer ': json.dumps(functools.reduce(operator.iconcat, reducefinal, []))}
            res6 = {'Partitions Read ': json.dumps(list(partitionnumlst))}
            final.append(res1)
            final.append(res2)
            final.append(res3)
            final.append(res4)
            final.append(res5)
            final.append(res6)
            final = json.dumps(final, indent=4, sort_keys=True, default=str)
            return final

    else:
        print("Wrong Request Call, Expected GET")
        return "Wrong Request Call, Expected GET"



@app.route("/interactiveui/<name>", methods = ['POST','GET','DELETE','PUT'])
def ui(name):
    if request.method == "GET":
        temp1 = temp
        temp = name
        if temp == "back":
            return temp1

        else:
            temp = "/"+temp
            return temp


    else:
        print("Wrong Request Call, Expected GET")
        return "Wrong Request Call, Expected GET"





if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = "80", debug = True)
