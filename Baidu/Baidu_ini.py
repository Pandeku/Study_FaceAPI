# -*- coding = utf-8 -*-
# 百度API配置文件
import configparser

config = configparser.ConfigParser()

config["File_Path"] = {}
File_Path = config["File_Path"]
File_Path["Write_Txt_Path"] = "E:\\All_Face_Txt_Msg"
# Baidu Key
config["Baidu_Key"] = {}
Baidu_Key = config["Baidu_Key"]
Baidu_Key['APP_ID'] = "11041253"
Baidu_Key['API_KEY'] = "VYtF8vGIdFrfVTUk8GwBr9yh"
Baidu_Key['SECRET_KEY'] = "19UBQXeCtLwv6Ea48ugSsaNGt9jU2yKK"
# 图片上传
config["Baidu_Upload"] = {}
Baidu_Upload = config["Baidu_Upload"]
Baidu_Upload['Upload_Path'] = "E:\\Build_Face_DB\\upload_students_face\\"  # 上传百度人脸库图片路径
Baidu_Upload['Upload_Group'] = "test_add"  # 要上传图片所在的组，没有则新创建
# 添加学号
config["Baidu_AddID"] = {}
Baidu_AddID = config["Baidu_AddID"]
Baidu_AddID['AddId_Id_Path'] = "E:\\Build_Face_DB\\stu.txt"  # 给图片加学号，学号路径
Baidu_AddID['AddId_Img_Path'] = "E:\\Build_Face_DB\\add_students_face\\"  # 给图片加学号，图片路径
# 人脸库删除
config["Baidu_Delete"] = {}
Baidu_Delete = config["Baidu_Delete"]
Baidu_Delete['Delete_Stu_Path'] = "E:\\Build_Face_DB\\delete_students_face\\all_stu_id.txt"  # 批量删除学号路径
Baidu_Delete['Delete_Group'] = "test_add"  # 删除人脸库组名
# 人脸检测
config["Baidu_Detect"] = {}
Baidu_Detect = config["Baidu_Detect"]
Baidu_Detect["Detect_Url"] = "https://aip.baidubce.com/rest/2.0/face/v1/detect"
Baidu_Detect["Detect_Path"] = "E:\\Test_Face_Set\\"
# 人脸查找
config["Baidu_Search"] = {}
Baidu_Detect = config["Baidu_Search"]
Baidu_Detect["Search_Url"] = "https://aip.baidubce.com/rest/2.0/face/v2/identify"
Baidu_Detect["Search_Path"] = "E:\\Test_Face_Set\\"
Baidu_Detect["Search_Group"] = "test_add"

# 给图片分组
config["Move_Img"] = {}
Move_Img = config["Move_Img"]
Move_Img["Move_Path"] = "E:\\study\\all_pic\\"

# 保存配置文件
with open("Baidu_INI.ini", 'w') as configfile:
    config.write(configfile)
