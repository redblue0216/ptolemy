# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个InfluxDB数据库客户端操作类，主要利用InfluxDB的PythonAPI集成了一系列常规操作。
"""
模块介绍
-------

这是一个InfluxDB数据库客户端操作类，主要利用InfluxDB的PythonAPI集成了一系列常规操作。

设计模式：

    无

关键点：    

    （1）InfluxDBAPI  

主要功能：            

    （1）写数据

    （2）读数据                                                     

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from influxdb import InfluxDBClient
from influxdb import DataFrameClient



####### InfluxDB基础功能类 ##################################################
### 设计模式：                                                            ###
###     无                                                               ###
### 关键点：                                                              ###
### （1）InfluxDBapi                                                     ###
### 主要功能：                                                            ###
### （1）写数据                                                           ###
### （2）读数据                                                           ###
############################################################################



###### 基础模块类 #####################################################################
######################################################################################



class InfluxDB(object):
    """
    类介绍：

        这是一个InfluxDB数据库客户端操作类，主要利用InfluxDB的PythonAPI集成了一系列常规操作。
    """


    ### InfluxDB实例
    _instance = None


    def __init__(self,host,port,user,password,database,method):
        """
        属性功能：

            定义一个收集数据库连接信息的属性功能

        参数：
            host (str): 数据库HOST
            port (int): 数据库PORT
            user (str): 用户名
            password (str): 密码
            database （str): 数据库名称
            method (str): 连接方式
        """

        self.host = host
        self.port = port 
        self.user = user
        self.password = password
        self.database = database
        if method == 'DataFrame':
            self.client = self.create_dataframe_client()
        else:
            self.client = self.create_json_client()


    def create_json_client(self):
        """
        方法功能：

            定义一个创建json数据传输的客户端

        参数：
            无

        返回：
            InfluxDB_JSON_Client (Object): InfluxDB的JSON格式数据传输客户端
        """

        InfluxDB_JSON_Client = InfluxDBClient(self.host,self.port,self.user,self.password,self.database)
        databases_list = InfluxDB_JSON_Client.get_list_database()
        dababases_set = set([item.values() for item in databases_list])
        if self.database in dababases_set:    
            return InfluxDB_JSON_Client
        else:
            InfluxDB_JSON_Client.create_database(self.database)
            return InfluxDB_JSON_Client


    def create_dataframe_client(self):
        """
        方法功能：

            定义一个创建dataframe数据传输的客户端

        参数：
            无

        返回：
            InfluxDB_DataFrame_Client (Object): InfluxDB的DataFrame格式数据传输客户端
        """        

        InfluxDB_DataFrame_Client = DataFrameClient(self.host,self.port,self.user,self.password,self.database)
        databases_list = InfluxDB_DataFrame_Client.get_list_database()
        dababases_set = set([item.values() for item in databases_list])
        if self.database in dababases_set:    
            return InfluxDB_DataFrame_Client
        else:
            InfluxDB_DataFrame_Client.create_database(self.database)
            return InfluxDB_DataFrame_Client        
        

    def get_client(self):
        """
        方法功能：

            定义一个获取客户端的方法

        参数：
            无

        返回：
            客户端
        """

        return self.client


    def write_json(self,points):
        """
        方法功能：

            定义一个以json格式写入数据库的方法

        参数：
            points (list): json格式的数据列表

        返回：
            写入成功提示
        """

        self.client.write_points(points)        
        return 'Write JSON InfulxDB Successful!!'


    def read_json(self,query):
        """
        方法功能：

            定义一个以json格式读取数据的方法

        参数：
            query (str): str格式的数据查询语句

        返回：
            query_result (ResultSet): 查询结果
        """        

        query_result = self.client.query(query)
        return query_result


    def write_dataframe(self,dataframe,datatable,tag_dict,protocol):
        """
        方法功能：

            定义一个以DataFrame格式写入数据库的方法

        参数：
            dataframe (DataFrame): DataFrame格式的数据
            datatable (str): 数据表名
            tag_dict (Dict): 标签字典
            protocol (str): 协议格式

        返回：
            写入成功提示
        """        
        
        self.client.write_points(dataframe = dataframe,measurement = datatable,tags = tag_dict,protocol = protocol)
        return 'Write DataFrame InfluxDB Successful!'


    def read_dataframe(self,query):
        """
        方法功能：

            定义一个以DataFrame格式读取数据的方法

        参数：
            query (str): str格式的数据查询语句

        返回：
            query_result (ResultSet): 查询结果
        """         
        query_result = self.client.query(query)
        return query_result
    

    def query(self,query):
        """
        方法功能：

            定义一个统一读取数据的方法

        参数：
            query (str): str格式的数据查询语句

        返回：
            result_set (ResultSet): 查询结果
        """      

        client = InfluxDBClient(self.host,self.port,self.user,self.password,self.database)
        result_set = client.query(query)
        return result_set
        


#############################################################################################################
#############################################################################################################


