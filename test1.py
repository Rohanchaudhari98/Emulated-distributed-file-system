from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
import requests
import pymysql
import json

app = Flask(__name__)
CORS(app)
app.config["CORS_SUPPORTS_CREDENTIALS"] = True



db = pymysql.connect(host="127.0.0.1",user = "root",password= "Qwerty123",database = "edfs" )
cursor = db.cursor()


@app.route("/mkdir/<path:name>", methods = ['POST', 'GET','DELETE','PUT'])
def make_directory(name):
    if request.method == "POST":
        # bar = request.args.to_dict()
        lst = []
        name = "/" + name
        temp = name.split("/")
        current_name="/"+temp[-1]
        path = ""
        for i in range(0,len(temp)-1):
            path = path + "/" + temp[i]
        anscestral_path=path[1:]
        print("1",anscestral_path)
        
        root_id=1
        parent_id=0
        print("2",temp)
        if len(temp)>2:
            parent_id=1
            current_id=1
            child_id=None
            
            sql = "select current_id from FS_Structure where name = '%s'" %(current_name)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            parent_id=results
            print(parent_id)
        #return parent_id    
        sql = "select max(current_id)+1 as current_id from FS_Structure"
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if results[0][0] == None:
            current_id = 1
        else:
            current_id=results[0][0]
        child_id=None
        file_directory="Directory"
        print(root_id,parent_id,child_id,current_id,current_name,anscestral_path,file_directory)
        if child_id == None:
            sql = "insert into FS_Structure(Root_id,Parent_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%s','%s','%s')" %(root_id,parent_id,current_id,current_name,anscestral_path,file_directory)
        else:
            sql = "insert into FS_Structure(Root_id,Parent_id,Child_id,Current_id,name,Ancestral_path,File_or_Directory) values('%d','%d','%d','%d','%s','%s','%s')" %(root_id,parent_id,child_id,current_id,current_name,anscestral_path,file_directory)
        cursor.execute(sql)
        db.commit()
        print(temp)
        if len(temp)>=3:
            print(current_name)
            print(type(current_name))
            sql="select current_id from FS_Structure where name='%s'" %(current_name)
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            child_id_table=results[0][0]
        #return child_id_table
            sql="update FS_Structure set child_id='%d' where name = '%s'" %(child_id_table,anscestral_path)
            cursor.execute(sql)
            db.commit()
        #sql = "update child_id as max(child_id)+1 from FS_Structure
        #cursor.execute(sql)
        #results = cursor.fetchall()
        #child_id=results
        
        
        # sql = "select max(current_id) from FS_Structure"
        # cursor.execute(sql)
        # results = cursor.fetchone()
        # # print(results[0])
        # parent = name.split("/")
        # print(parent)
        # sql = "insert into FS_Structure values ('%s')" %name
        # cursor.execute(sql)
        # db.commit()
        print("Directory "+name+" has been created")
        return "Directory "+name+" has been created"
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
        sql = "Select Current_id from FS_Structure where Ancestral_Path = '%s' and name = '%s' and File_or_Directory = 'File'" %(path,temp[-1])
        cursor.execute(sql)
        results = cursor.fetchone()
        if results == None:
            return "No such file"
        sql = "Select content from partition_file where File_id = '%s'" %(results[0])
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
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
        sql = "delete from partition_file where File_id = '%s'" %(results[0])
        cursor.execute(sql)
        db.commit()
        sql = "delete from FS_Structure where Current_id = '%d'" %(results[0])
        cursor.execute(sql)
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
        sql = ""
        cursor.execute(sql)
        db.commit()
        print("File "+name+" has been uploaded to directory"+dirname)
        return "File "+name+" has been uploaded to directory"+dirname
    else:
        print("Wrong Request Call for put "+name+", Expected PUT")
        return "Wrong Request Call for put "+name+", Expected PUT"


# @app.route("/uploadfile", methods = ['POST','GET','DELETE','PUT'])
# def upload_file():
#     if request.method == "PUT":
#         details = request.form
#         command = details['command']
#         path = details['path']
#         filename = details['filename']
#         partitions = details['partitions']
#         sql = ""
#         cursor.execute(sql)
#         db.commit()


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = "80", debug = True)
