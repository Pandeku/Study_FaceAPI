# coding=utf-8
import shutil
from aip import AipFace
import pymysql
import base64
import time
import requests
from json import JSONDecoder
import os
import configparser


# {'result': [{'group_id': 'test_add', 'uid': '1708020212', 'scores': [100], 'user_info': '吕清'}],
# 'result_num': 1, 'log_id': 2580833485041520, 'ext_info': {'faceliveness': '0.40944513678551'}}


def Get_File_Content(FilePath):  # 获取图片
    with open(FilePath, 'rb') as fp:
        return fp.read()


def Write_Txt_Msg(Txt_Name, Msg):  # 写文件
    with open(Write_Txt_Path + "\\" + Txt_Name, 'a') as f:
        f.write(Msg)


def Back_StuId_List(Path):  # 返回学号列表
    Lines = []
    file = open(Path, encoding='UTF-8')
    for line in file:  # line = 1706020211 	姜彤	财务172	13：00-14：10	201	工2-201-1	未注册！	未签到！
        Lines.append(line[0:10])  # line[0:10] = 学号
        # Lines.append(line[10:14]) # line[10:14] = 姓名
    file.close()
    return Lines


def Back_Student_Name(Uid):  # 连接mysql 获取学号对应的学生姓名
    result = []
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT User_Name FROM login_register_attend_user WHERE User_Id='%s' " % Uid
    try:
        cursor.execute(sql)  # 执行sql
        result = cursor.fetchone()  # 获取一条数据
    except:
        print("Error: unable to fetch data")
    db.close()  # 关闭数据库连接
    return result  # 返回 姓名


def Back_Time_Site(uid):  # 连接mysql数据库 获取学号对应的学生姓名
    result = []
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT Exam_Time, Exam_Site FROM login_register_attend_user WHERE User_Id='%s' " % uid
    try:
        cursor.execute(sql)  # 执行sql
        result = cursor.fetchone()  # 获取一条数据
    except:
        print("Error: unable to fetch data")

    db.close()  # 关闭数据库连接
    return result  # 返回 考场时间 和 考试地点


def Update_Table(Uid):  # 连接mysql 更新学号对应学生的人脸签到记录
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE login_register_attend_user SET Is_Add_Face='%s' WHERE User_Id = '%s'" % ("人脸已注册!", Uid)
    try:
        cursor.execute(sql)  # 执行更新
        db.commit()  # 提交
    except:
        db.rollback()  # 发生错误,回滚
        print("Error: unable to update data")
    db.close()
    return


def Get_AccessToken(Key, Secret):  # 获取 A_T
    http_url = 'https://aip.baidubce.com/oauth/2.0/token' \
               '?grant_type=client_credentials&client_id=%s&client_secret=%s' % (Key, Secret)
    response = requests.post(http_url)
    req_con = response.content.decode(encoding='UTF-8')
    req_dict = JSONDecoder().decode(req_con)
    return req_dict['access_token']


def Upload_FaceImgs(Path, groupId):  # 图片上传人脸库
    count = 1
    for Img in os.listdir(Path):    # if Img.endswith('.JPG'):
        image = Get_File_Content(Path+Img)  # 得到图片
        uid, endstr = os.path.splitext(Img)  # 得到图片名
        userInfo = Back_Student_Name(uid)  # 读Mysql表,查询学生名字
        start = time.clock()  # 记录上传时间
        result = client.addUser(uid, userInfo, groupId, image)  # 上传人脸库
        end = time.clock()
        if "error_msg" in result:
            txt = "Baidu_Upload_Fail.txt"
            msg = uid + "," + groupId + "," + result["error_msg"] + "，添加人脸的错""\n"
        else:
            Use_Time = end - start
            Update_Table(uid)  # 更新数据库
            txt = 'Baidu_Upload_TimeUse.txt'
            msg = str(count) + "," + uid + "," + groupId + "," + str(Use_Time) + "\n"
            print(str(count) + ",图片上传人脸库成功！")
            count += 1
        Write_Txt_Msg(txt, msg)
        time.sleep(0)  # 让程序等1.0s 再上传图片.因为 QPS 为每秒2 个;时间最佳区间在0.7 ~ 1.2 之间
    print("共计上传成功:", count - 1, "张图片!")
    return


def FaceBase_Add_ID(Path, Group):
    # path = config.get("Baidu", "upload_groupid") # 未加注图片路径
    # Group_Id = config.get("Baidu", "upload_groupid")  # 已构建好的人脸库组名
    # FaceBase_Add_ID(path, Group_Id) #使用人脸库加注学号
    os.chdir(Path)
    for Img in os.listdir(Path):
        # if Img.endswith('.JPG'):
        options = {
            "ext_fields": "faceliveness",
            "user_top_num": 1
        }
        image = Get_File_Content(Img)  # 获取图片
        groupId = Group  # 云上人脸库组
        Res = client.identifyUser(groupId, image, options)  # 人脸认证分数
        print(Res)
        if Res['result'][0]['scores'][0] > 66:  # 人脸认证分数，一般为80分最合适
            name = Res['result'][0]['uid']  # 给图片加学号
            # name = Res['result'][0]['user_info']  # 给图片加名字
            src = os.path.join(os.path.abspath(Path), Img)
            dst = os.path.join(os.path.abspath(Path), str(name) + '.JPG')
            try:
                os.rename(src, dst)
            except:
                print("修改图片名失败!")
        time.sleep(0.3)
    return


def Table_Add_User(Id_Path, Imgs_Path):  # 加注图片名
    Lines = Back_StuId_List(Id_Path)  # 返回学号列表
    count = 0  # 表的第一条记录
    for Img in os.listdir(Imgs_Path):  # 打开图片
        try:
            src = os.path.join(Imgs_Path, Img)
            dst = os.path.join(Imgs_Path, str(Lines[count]) + ".JPG")
            os.rename(src, dst)  # 重命名
            count += 1  # 第二张图
        except:
            print(FileExistsError)
    return


def Delete_Face_Pic(Stuid_Path, Group):  # 删除人脸库
    Lines = Back_StuId_List(Stuid_Path)  # 返回学号列表
    for uid in Lines:
        try:
            res = client.deleteGroupUser(Group, uid)
            # res = client.deleteUser(uid) # 删除全部
            if "error_msg" in res:
                txt = "Delete_FacePic_Fail.txt"
                msg = uid + " ," + Group + "\n"
                Write_Txt_Msg(txt, msg)  # 出错信息写入文件中
            else:
                print(uid + ",删除成功！")
        except:
            pass
        time.sleep(0.4)
    return


def Detect_Face_SDK(Path):  # 人脸检测 SDK 方法
    count = 1
    for Img in os.listdir(Path):
        uid, endstr = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(Path + Img)  # 获取图片
        # image = base64.b64encode(image)
        options = {"max_face_num": 1, "face_fields": "beauty,gender,age"}
        start_time = time.clock()  # 加时间记录
        Result = client.detect(image, options)
        end_time = time.clock()
        if Result["result_num"] == 0:
            msg = uid
            txt = "Baidu_FaceDetect_SDK_Fail.txt"
        else:
            Use_Time = end_time - start_time
            msg = uid + "," + str(Use_Time) + "," + str(Result) + "\n"
            txt = "Baidu_FaceDetect_SDK_TimeUse.txt"
            count += 1
        Write_Txt_Msg(txt, msg)
        time.sleep(0)
    print("共计检测成功:", count - 1, "张图片!")
    return


def Detect_Face_API(Path, Url):
    http_url = Url + "?access_token=" + Access_token
    count = 1
    for Img in os.listdir(Path):
        #       if Img.endswith('.JPG'):
        uid, endstr = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(Path + Img)  # 获取图片
        image = base64.b64encode(image)  # base64图片
        files = {"image": image}
        start_time = time.clock()
        response = requests.post(http_url, files=files)  # 发送requests请求
        end_time = time.clock()
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        if req_dict["result_num"] == 0:
            msg = uid
            file = "Baidu_FaceDetect_API_Fail.txt"
        else:
            Use_Time = end_time - start_time
            msg = uid + "," + str(Use_Time) + "," + str(req_dict)
            file = "Baidu_FaceDetect_API_TimeUse.txt"
            count += 1
        Write_Txt_Msg(file, msg)
        time.sleep(0)
    print("共计检测成功:", count - 1, "张图片!")
    return


def Search_Faces(Path, Group, Url):
    http_url = Url + "?access_token=" + Access_token
    count = 1
    for Img in os.listdir(Path):
        uid, endstr = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(Path+Img)  # 获取图片
        image = base64.b64encode(image)  # 图片base64 编码
        params = {"face_top_num": "1", "group_id": Group, "images": image, "user_top_num": "1"}
        start_time = time.clock()
        response = requests.post(http_url, data=params)  # 发送requests请求
        end_time = time.clock()
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        Use_Time = end_time - start_time
        msg = uid + "," + str(Use_Time) + "," + str(req_dict) + "\n"
        Write_Txt_Msg("Baidu_SearchFace_API_TimeUse.txt", msg)
        count += 1
        time.sleep(0)
        print(uid + str(req_dict))
    print("共计检测成功:", count - 1, "张图片!")
    return


def Move_Pic(Path):
    os.chdir(Path)
    for Img in os.listdir(Path):
        uid, endstr = os.path.splitext(Img)  # 得到图片名
        res = Back_Time_Site(uid)  # 查询得到时间和考场
        if None == res:
            continue
        else:
            shutil.move(Img, os.path.join("E:\\study", res[0] + "\\" + res[1]))  # 移动到对应的考场
            print("移动成功！")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("Baidu_INI.ini")  # 读配置文件
    # 测试人脸库得到百度 Key
    APP_ID = config.get("Baidu_Key", "APP_ID")
    API_KEY = config.get("Baidu_Key", "API_KEY")
    SECRET_KEY = config.get("Baidu_Key", "SECRET_KEY")
    Access_token = Get_AccessToken(API_KEY, SECRET_KEY)  # 获取 Access_token
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    # 写错误信息路径
    Write_Txt_Path = config.get("File_Path", "Write_Txt_Path")
    # 上传路径和人脸库组名
    Upload_Path = config.get("Baidu_Upload", "Upload_Path")
    Upload_GroupId = config.get("Baidu_Upload", "Upload_GroupId")
    # 学号和图片路径
    AddId_Id_Path = config.get("Baidu_AddID", "AddId_Id_Path")
    AddId_Imgs_Path = config.get("Baidu_AddID", "AddId_Imgs_Path")
    # 学号和学号所在的组
    Delete_Stuid_Path = config.get("Baidu_Delete", "Delete_Stuid_Path")  # 要删除的学号路径
    Delete_GroupId = config.get("Baidu_Delete", "Delete_GroupId")  # 学号所在组
    # 图片路径和请求的API url
    Detect_Path = config.get("Baidu_Detect", "Detect_Path")  # 人脸检测图片路径
    Detect_Url = config.get("Baidu_Detect", "Detect_Url")
    # 图片路径和组名
    Search_Path = config.get("Baidu_Search", "Search_Path")
    Search_Groupid = config.get("Baidu_Search", "Search_Groupid")
    Search_Url = config.get("Baidu_Search", "Search_Url")
    # 移动图片所在文件夹
    Move_Path = config.get("Move_Imgs", "Move_Path")

    # ## 上传人脸库 ###
    # Upload_FaceImgs(Upload_Path, Upload_GroupId)  # 上传人脸库
    # Table_Add_User(AddId_Id_Path, AddId_Imgs_Path)  # 加注学号
    # Delete_Face_Pic(Delete_Stuid_Path, Delete_GroupId)  # 批量删除人脸库
    # Detect_Face_SDK(Detect_Path)  # 人脸检测 SDK
    # Detect_Face_API(Detect_Path, Detect_Url)  # 人脸检测 API
    # Search_Faces(Search_Path, Search_Groupid,Search_Url)  # 人脸查找 API
    # Move_Pic(Move_Path)  # 移动图片到指定文件夹
