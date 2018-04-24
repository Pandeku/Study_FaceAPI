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


def Get_File_Content(path):  # 获取图片
    with open(path, 'rb') as fp:
        return fp.read()


def Write_Txt_Msg(txt_name, msg):  # 写文件
    with open(Write_Txt_Path + "\\" + txt_name, 'a') as f:
        f.write(msg)


def Back_StuId_List(id_path):  # 返回学号列表
    lines = []
    file = open(id_path, encoding='UTF-8')
    for line in file:  # line = 1706020211 	姜彤	财务172	13：00-14：10	201	工2-201-1	未注册！	未签到！
        lines.append(line[0:10])  # line[0:10] = 学号
        # Lines.append(line[10:14]) # line[10:14] = 姓名
    file.close()
    return lines


def Back_Student_Name(uid):  # 连接mysql 获取学号对应的学生姓名
    result = []
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT User_Name FROM login_register_attend_user WHERE User_Id='%s' " % uid
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


def Update_Table(uid):  # 连接mysql 更新学号对应学生的人脸签到记录
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE login_register_attend_user SET Is_Add_Face='%s' WHERE User_Id = '%s'" % ("人脸已注册!", uid)
    try:
        cursor.execute(sql)  # 执行更新
        db.commit()  # 提交
    except:
        db.rollback()  # 发生错误,回滚
        print("Error: unable to update data")
    db.close()
    return


def Get_AccessToken(api_key, secret_key):  # 获取 A_T
    http_url = 'https://aip.baidubce.com/oauth/2.0/token' \
               '?grant_type=client_credentials&client_id=%s&client_secret=%s' % (api_key, secret_key)
    response = requests.post(http_url)
    req_con = response.content.decode(encoding='UTF-8')
    req_dict = JSONDecoder().decode(req_con)
    return req_dict['access_token']


def Upload_FaceImg(upload_path, upload_group):  # 图片上传人脸库
    count = 1
    for Img in os.listdir(upload_path):  # if Img.endswith('.JPG'):
        image = Get_File_Content(upload_path + Img)  # 得到图片
        uid, ends = os.path.splitext(Img)  # 得到图片名
        user_info = Back_Student_Name(uid)  # 读Mysql表,查询学生名字
        start = time.clock()  # 记录上传时间
        result = client.addUser(uid, user_info, upload_group, image)  # 上传人脸库
        end = time.clock()
        if "error_msg" in result:
            txt = "Baidu_Upload_Fail.txt"
            msg = uid + "," + upload_group + "," + result["error_msg"] + "，添加人脸的错""\n"
        else:
            use_time = end - start
            Update_Table(uid)  # 更新数据库
            txt = 'Baidu_Upload_TimeUse.txt'
            msg = str(count) + "," + uid + "," + upload_group + "," + str(use_time) + "\n"
            print(str(count) + ",图片上传人脸库成功！")
            count += 1
        Write_Txt_Msg(txt, msg)
        time.sleep(0)  # 让程序等1.0s 再上传图片.因为 QPS 为每秒2 个;时间最佳区间在0.7 ~ 1.2 之间
    print("共计上传成功:", count - 1, "张图片!")
    return


def FaceBase_Add_ID(path, group):
    # path = config.get("Baidu", "upload_groupid") # 未加注图片路径
    # Group_Id = config.get("Baidu", "upload_groupid")  # 已构建好的人脸库组名
    # FaceBase_Add_ID(path, Group_Id) #使用人脸库加注学号
    os.chdir(path)
    for Img in os.listdir(path):
        options = {
            "ext_fields": "faceliveness",
            "user_top_num": 1
        }
        image = Get_File_Content(Img)  # 获取图片
        res = client.identifyUser(group, image, options)  # 人脸认证分数
        print(res)
        if res['result'][0]['scores'][0] > 66:  # 人脸认证分数，一般为80分最合适
            name = res['result'][0]['uid']  # 给图片加学号
            # name = res['result'][0]['user_info']  # 给图片加名字
            src = os.path.join(os.path.abspath(path), Img)
            dst = os.path.join(os.path.abspath(path), str(name) + '.JPG')
            try:
                os.rename(src, dst)
            except FileExistsError:
                print(FileExistsError)
        time.sleep(0.3)
    return


def Table_Add_User(id_path, img_path):  # 加注图片名
    lines = Back_StuId_List(id_path)  # 返回学号列表
    count = 0  # 表的第一条记录
    for Img in os.listdir(img_path):  # 打开图片
        try:
            src = os.path.join(img_path, Img)
            dst = os.path.join(img_path, str(lines[count]) + ".JPG")
            os.rename(src, dst)  # 重命名
            count += 1  # 第二张图
        except FileExistsError:
            print(FileExistsError)
    return


def Delete_Face_Pic(delete_stu, delete_group):  # 删除人脸库
    lines = Back_StuId_List(delete_stu)  # 返回学号列表
    for uid in lines:
        try:
            res = client.deleteGroupUser(delete_group, uid)
            # res = client.deleteUser(uid) # 删除全部
            if "error_msg" in res:
                txt = "Delete_FacePic_Fail.txt"
                msg = uid + " ," + delete_group + "\n"
                Write_Txt_Msg(txt, msg)  # 出错信息写入文件中
            else:
                print(uid + ",删除成功！")
        except:
            pass
        time.sleep(0.4)
    return


def Detect_Face_SDK(detect_path):  # 人脸检测 SDK 方法
    count = 1
    for Img in os.listdir(detect_path):
        uid, ends = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(detect_path + Img)  # 获取图片
        # image = base64.b64encode(image)
        options = {"max_face_num": 1, "face_fields": "beauty,gender,age"}
        start_time = time.clock()  # 加时间记录
        result = client.detect(image, options)
        end_time = time.clock()
        if result["result_num"] == 0:
            msg = uid
            txt = "Baidu_FaceDetect_SDK_Fail.txt"
        else:
            use_time = end_time - start_time
            msg = uid + "," + str(use_time) + "," + str(result) + "\n"
            txt = "Baidu_FaceDetect_SDK_TimeUse.txt"
            count += 1
        Write_Txt_Msg(txt, msg)
        time.sleep(0)
    print("共计检测成功:", count - 1, "张图片!")
    return


def Detect_Face_API(detect_path, detect_url):
    http_url = detect_url + "?access_token=" + Access_token
    count = 1
    for Img in os.listdir(detect_path):
        #       if Img.endswith('.JPG'):
        uid, ends = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(detect_path + Img)  # 获取图片
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
            use_time = end_time - start_time
            msg = uid + "," + str(use_time) + "," + str(req_dict)
            file = "Baidu_FaceDetect_API_TimeUse.txt"
            count += 1
        Write_Txt_Msg(file, msg)
        time.sleep(0)
    print("共计检测成功:", count - 1, "张图片!")
    return


def Search_Faces(search_path, search_group, search_url):
    http_url = search_url + "?access_token=" + Access_token
    count = 1
    for Img in os.listdir(search_path):
        uid, ends = os.path.splitext(Img)  # 得到图片名
        image = Get_File_Content(search_path + Img)  # 获取图片
        image = base64.b64encode(image)  # 图片base64 编码
        params = {"face_top_num": "1", "group_id": search_group, "images": image, "user_top_num": "1"}
        start_time = time.clock()
        response = requests.post(http_url, data=params)  # 发送requests请求
        end_time = time.clock()
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        use_time = end_time - start_time
        msg = uid + "," + str(use_time) + "," + str(req_dict) + "\n"
        Write_Txt_Msg("Baidu_SearchFace_API_TimeUse.txt", msg)
        count += 1
        time.sleep(0)
        print(uid + str(req_dict))
    print("共计检测成功:", count - 1, "张图片!")
    return


def Move_Pic(move_path):
    os.chdir(move_path)
    for Img in os.listdir(move_path):
        uid, ends = os.path.splitext(Img)  # 得到图片名
        res = Back_Time_Site(uid)  # 查询得到时间和考场
        if res is None:
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
    Upload_Group = config.get("Baidu_Upload", "Upload_Group")
    # 学号和图片路径
    AddId_Id_Path = config.get("Baidu_AddID", "AddId_Id_Path")
    AddId_Img_Path = config.get("Baidu_AddID", "AddId_Img_Path")
    # 学号和学号所在的组
    Delete_Stu_Path = config.get("Baidu_Delete", "Delete_Stu_Path")  # 要删除的学号路径
    Delete_Group = config.get("Baidu_Delete", "Delete_Group")  # 学号所在组
    # 图片路径和请求的API url
    Detect_Path = config.get("Baidu_Detect", "Detect_Path")  # 人脸检测图片路径
    Detect_Url = config.get("Baidu_Detect", "Detect_Url")
    # 图片路径和组名
    Search_Path = config.get("Baidu_Search", "Search_Path")
    Search_Group = config.get("Baidu_Search", "Search_Group")
    Search_Url = config.get("Baidu_Search", "Search_Url")
    # 移动图片所在文件夹
    Move_Path = config.get("Move_Img", "Move_Path")

    # ## 上传人脸库 ###
    Upload_FaceImg(Upload_Path, Upload_Group)  # 上传人脸库
    Table_Add_User(AddId_Id_Path, AddId_Img_Path)  # 加注学号
    Delete_Face_Pic(Delete_Stu_Path, Delete_Group)  # 批量删除人脸库
    Detect_Face_SDK(Detect_Path)  # 人脸检测 SDK
    Detect_Face_API(Detect_Path, Detect_Url)  # 人脸检测 API
    Search_Faces(Search_Path, Search_Group, Search_Url)  # 人脸查找 API
    Move_Pic(Move_Path)  # 移动图片到指定文件夹
