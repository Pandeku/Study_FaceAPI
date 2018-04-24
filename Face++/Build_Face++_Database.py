import time
import requests
from json import JSONDecoder
import os
import configparser


def Get_File_Content(path):  # 获取图片
    with open(path, 'rb') as fp:
        return fp.read()


def Write_Txt_Msg(txt_name, msg):  # 写文件
    with open(Write_Txt_Path + "\\" + txt_name, 'a') as f:
        f.write(msg)


def CreateFaceSet(app_key, faceset_url):
    response = requests.post(faceset_url, data=app_key)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    if "error_message" in req_dict:
        msg = req_dict["error_message"] + "\n"
        Write_Txt_Msg("Face++_CreateFaceSet_Fail.txt", msg)  # 出错信息写入文件中
    else:
        msg = str(req_dict) + "\n"
        print(app_key["outer_id"] + "，创建人脸集合成功！")
        # 返回字段说明
        # request_id ： 用于区分每一次请求的唯一的字符串。除非发生404 或 403，此字段必定返回。
        # # 404 : API_NOT_FOUND;    403 :AUTHORIZATION_ERROR
        # faceset_token ：FaceSet 的标识
        # outer_id ： 用户自定义的 FaceSet 标识，如果未定义则返回值为空
        # face_added ： 本次操作成功加入 FaceSet的face_token 数量
        # face_count ： 操作结束后 FaceSet 中的 face_token 总数量
        # ailure_detail ：无法被加入 FaceSet 的 face_token 以及原因
        # # face_token：人脸标识;
        # # reason：不能被添加的原因，包括 INVALID_FACE_TOKEN 人脸表示不存在; QUOTA_EXCEEDED 已达到 FaceSet 存储上限
        # time_used : 整个请求所花费的时间，单位为毫秒。除非发生404 或 403 错误，此字段必定返回。
        # error_message ： 当请求失败时才会返回此字符串，具体返回内容见后续错误信息章节。否则此字段不存在。
        Write_Txt_Msg("Face++_CreateFaceSet_TimeUse.txt", msg)


def AddFace(add_path, app_key, add_url, detect_url, add_outer_id):
    count = 1
    for Img in os.listdir(add_path):
        uid, endstr = os.path.splitext(Img)
        data_dict = Back_Detect_Dic(add_path+Img, app_key, detect_url)  # 添加人脸前先检测人脸
        if "error_message" in data_dict:
            continue
        face_token = data_dict['faces'][0]['face_token']
        app_key["outer_id"] = add_outer_id
        app_key["face_tokens"] = face_token
        # 添加人脸
        start_time = time.clock()
        response = requests.post(add_url, data=app_key)
        end_time = time.clock()
        use_time = end_time - start_time
        # 返回结果
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        if "error_message" in req_dict:
            msg = uid + "," + req_dict["error_message"] + "，添加人脸的错误" + "\n"
            file = "Face++_Add_Fail.txt"
        else:
            msg = uid + "," + str(use_time) + "," + str(req_dict) + "\n"
            file = "Face++_Add_TimeUse.txt"
            count += 1
        Write_Txt_Msg(file, msg)
        time.sleep(0)
        print(req_dict)
    print("共计添加成功:", count - 1, "张图片!")
    return


def Back_Detect_Dic(img, app_key, detect_url):
    uid, endstr = os.path.splitext(img)
    image = Get_File_Content(img)  # 获取图片
    files = {"image_file": image}
    start_time = time.clock()
    response = requests.post(detect_url, data=app_key, files=files)
    end_time = time.clock()
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    if "error_message" in req_dict:
        msg = uid + "," + req_dict["error_message"] + "，检测的错误" + "\n"
        file = "Face++_Detect_Fail.txt"
    else:
        use_time = end_time - start_time
        msg = uid + "," + str(use_time) + "," + str(req_dict) + "\n"
        file = "Face++_Detect_TimeUse.txt"
    Write_Txt_Msg(file, msg)
    time.sleep(0)
    return req_dict


def Detect_Faces(detect_path, app_key, detect_url):
    count = 1
    for Img in os.listdir(detect_path):
        uid, endstr = os.path.splitext(Img)
        image = Get_File_Content(detect_path + Img)  # 获取图片
        files = {"image_file": image}
        start_time = time.clock()
        response = requests.post(detect_url, data=app_key, files=files)
        end_time = time.clock()
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        if "error_message" in req_dict:
            msg = uid + "," + req_dict["error_message"] + "，检测的错误" + "\n"
            file = "Face++_Detect_Fail.txt"
        else:
            use_time = end_time - start_time
            msg = uid + "," + str(use_time) + "," + str(req_dict) + "\n"
            file = "Face++_Detect_TimeUse.txt"
            count += 1
        print(req_dict)
        Write_Txt_Msg(file, msg)
        time.sleep(0)
    print("共计检测成功:", count - 1, "张图片!")
    return


# search_url
# search_path
# search_outer_id
def Search_Face(search_path, search_key, search_url):
    count = 1
    for Img in os.listdir(search_path):
        uid, ends = os.path.splitext(Img)
        image = Get_File_Content(search_path + Img)  # 获取图片
        files = {"image_file": image}
        start_time = time.clock()
        response = requests.post(search_url, data=search_key, files=files)
        end_time = time.clock()
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)

        if "error_message" in req_dict:

            msg = uid + "," + req_dict["error_message"] + "，查找的错误" + "\n"
            file = "Face++_Search_Fail.txt"
        else:
            use_time = end_time - start_time
            msg = uid + "," + str(use_time) + "," + str(req_dict) + "\n"
            file = "Face++_Search_TimeUse.txt"
            count += 1
        time.sleep(0)
        Write_Txt_Msg(file, msg)
        print(req_dict)
    print("共计识别成功:", count - 1, "张图片!")
    return


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("Face++_ini.ini")
    Key = config.get("Face++_Key", "API_KEY")
    Secret = config.get("Face++_Key", "SECRET_KEY")
    APP_Key = {"api_key": Key, "api_secret": Secret}
    Write_Txt_Path = config.get("File_Path", "Write_Msg_Path")

    # 建Faceset
    FaceSet_Url = config.get("Face++_FaceSet", "FaceSet_Url")
    FaceSet_Name = config.get("Face++_FaceSet", "FaceSet_Name")
    Create_Outer_Id = config.get("Face++_FaceSet", "Create_Outer_Id")
    FaceSet_Key = {"api_key": Key, "api_secret": Secret, "display_name": FaceSet_Name, "outer_id": Create_Outer_Id}
    # 添加人脸
    Add_Url = config.get("Face++_AddFaces", "Add_Url")
    Add_Path = config.get("Face++_AddFaces", "Add_Path")
    Add_Outer_Id = config.get("Face++_AddFaces", "Add_Outer_Id")
    # 人脸检测
    Detect_Url = config.get("Face++_Detect", "Detect_Url")
    Detect_Path = config.get("Face++_Detect", "Detect_Path")
    # 人脸查找
    Search_Path = config.get("Face++_Search", "Search_Path")
    Search_Url = config.get("Face++_Search", "Search_Url")
    Search_Outer_Id = config.get("Face++_Search", "Search_Outer_Id")
    Search_Key = {"api_key": Key, "api_secret": Secret, "outer_id": Search_Outer_Id}

    # 创建人脸集合
    # CreateFaceSet(FaceSet_Key, FaceSet_Url)
    # 添加人脸
    # AddFace(Add_Path, APP_Key, Add_Url, Detect_Url, Add_Outer_Id)
    # 人脸检测
    # Detect_Faces(Detect_Path, APP_Key, Detect_Url)
    # 人脸查找
    # Search_Face(Search_Path, Search_Key, Search_Url)
