# -*- coding = utf-8 -*-
# Face++ API配置文件
import configparser

config = configparser.ConfigParser()

config["File_Path"] = {}
File_Path = config["File_Path"]
File_Path["Write_Msg_Path"] = "E:\\All_Face_Txt_Msg"

config["Face++_Key"] = {}
Face_Key = config["Face++_Key"]
Face_Key['API_KEY'] = "SRh6DjVrrxZo_WWqWhIduVc5BNN3_aHB"
Face_Key['SECRET_KEY'] = "NsIEytookHBQa9zVsoOD7qwxz4_4hFcB"
# 添加人脸集合
config["Face++_FaceSet"] = {}
FaceSet = config["Face++_FaceSet"]
FaceSet['FaceSet_Url'] = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
FaceSet['FaceSet_Name'] = "name: 201"  # 识别的名字
FaceSet['Create_Outer_Id'] = "201"  # 人脸集合 ID
# 添加人脸
config["Face++_AddFaces"] = {}
_Add = config["Face++_AddFaces"]
_Add['Add_Url'] = "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
_Add['Add_Path'] = "E:\\Test_Face_Set\\"
_Add['Add_Outer_Id'] = "201"  # 人脸集合 ID
# 人脸检测
config["Face++_Detect"] = {}
_Detect = config["Face++_Detect"]
_Detect['Detect_Url'] = "https://api-cn.faceplusplus.com/facepp/v3/detect"
_Detect['Detect_Path'] = "E:\\Test_Face_Set\\"
# 人脸查找
config["Face++_Search"] = {}
_Search = config["Face++_Search"]
_Search['Search_Url'] = "https://api-cn.faceplusplus.com/facepp/v3/search"
_Search['Search_Path'] = "E:\\Test_Face_Set\\"
_Search['Search_Outer_Id'] = "201"  # 人脸集合 ID

with open("Face++_INI.ini", 'w') as configfile:
    config.write(configfile)
