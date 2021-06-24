# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个InfluxDB专属的ORM模型基础模块
"""
模块介绍
-------

这是一个InfluxDB专属的ORM模型基础模块

设计模式：

    （1）  无 

关键点：    

    （1）type与__new__技术

主要功能：            

    （1）InfluxDB专属ORM模型                                   

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from Ptolemy.influxdb_base import *
import time 



####### InfluxDBORM模型类 ##################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）type与__new__技术                                               ###
### 主要功能：                                                           ###
### （1）InfluxDB专属ORM模型                                             ###
############################################################################


####### 数据类型类 #############################################################
###############################################################################



class Field(object):
    """
    类介绍：

        这是一个数据模型中的表达数据变量类型的基础类
    """


    def __init__(self,name,field_type,tag_key,default):
        """
        属性功能：

            定义一个初始化属性的方法

        参数：
            name (str): 数据类型名称
            field_type (str): 数据类型
            tag_key （bool): 是否是标签数据类型
            default (obj): 默认值
        """

        self.name = name
        self.field_type = field_type
        self.tag_key = tag_key
        self.default = default



class FieldsField(Field):
    """
    类介绍：

        这是一个数据模型中的表达fields数据变量类型的基础类
    """    


    def __init__(self,name,field_type = 'all',tag_key = False,default = None):
        """
        属性功能：

            定义一个初始化属性的方法

        参数：
            name (str): 数据类型名称
            field_type (str): 数据类型all
            tag_key （bool): 是否是标签数据类型False
            default (obj): 默认值
        """

        super().__init__(name,field_type,tag_key,default)




class TagsField(Field):
    """
    类介绍：

        这是一个数据模型中的表达fields数据变量类型的基础类
    """    


    def __init__(self,name,field_type = 'str',tag_key = True,default = None):
        """
        属性功能：

            定义一个初始化属性的方法

        参数：
            name (str): 数据类型名称
            field_type (str): 数据类型str
            tag_key （bool): 是否是标签数据类型True
            default (obj): 默认值
        """        

        super().__init__(name,field_type,tag_key,default)



####### 数据模型元类 #########################################################
#############################################################################



class ModelMetaClass(type):
    """
    类介绍：

        这是一个InfluxDB数据模型构建类，主要用于抽象数据类型的构建过程。
    """


    def __new__(cls,name,obj,attr):
        """
        属性功能：

            定义一个InfluxDB数据模型构建的魔法方法

        参数：
            无

        返回：
            构建类
        """

        if name == 'Models':
            return type.__new__(cls,name,obj,attr)
        mappings = {}
        for k,v in attr.items():
            if isinstance(v,Field):
                mappings[k] = v
        for k in mappings.keys():
            attr.pop(k)
        attr['__table_name__'] = name
        attr['__mappings__'] = mappings
        return type.__new__(cls,name,obj,attr)



####### 数据模型基础类 #####################################################
###########################################################################



class Models(dict,metaclass = ModelMetaClass):
    """
    类介绍：

        这是一个InfluxDB数据模型类，主要用于抽象InfluxDB数据表结果。
    """


    def __init__(self,**kwargs):
        """
        属性功能：

            定义一个初始化的方法
        """

        super().__init__(**kwargs)


    def __getattr__(self,key):
        """
        方法功能：

            定义一个获取属性并检查的魔法方法

        参数：
            key (str): 属性关键字

        返回：
            属性对象
        """

        try:
            return self[key]
        except KeyError:
            raise AttributeError("No attribute '{}'".format(key))


    def __setattr__(self,key,value):
        """
        方法功能：

            定义一个设置属性的魔法方法

        参数：
            key (str): 属性关键字
            value (Object): 数据值对象

        返回：
            无
        """

        self[key] = value


    def save_json(self,influxdb_obj,save_time = time.time()):
        """
        方法功能：

            定义一个以JSON格式保存数据模型对象的方法

        参数：
            influxdb_obj (Object): InfluxDB数据库对象
            save_time (str): 保存数据时间

        返回：
            保存成功提示
        """

        tags = {}
        fields = {}
        measurement = self.__table_name__
        time = save_time
        json_body = []
        json_body_dict = {}
        for k,v in self.__mappings__.items():
            if v.tag_key == False:
                fields[k] = getattr(self,k,None)
            elif v.tag_key == True:
                tags[k] = getattr(self,k,None)
        json_body_dict['measurement'] = measurement
        json_body_dict['tags'] = tags
        json_body_dict['time'] = time
        json_body_dict['fields'] = fields
        json_body.append(json_body_dict)
        try:
            write_result = influxdb_obj.write_json(json_body)
            print(write_result)
        except:
            print('No InfluxDB Object!')

        return 'Save JSON Data Successful!'

    
    def save_dataframe(self,influxdb_obj):
        """
        方法功能：

            定义一个以DataFrame格式保存数据模型对象的方法

        参数：
            influxdb_obj (Object): InfluxDB数据库对象

        返回：
            保存成功提示
        """        
        datatable = self.__table_name__
        dataframe = self.dataframe 
        tags = self.tag_dict
        protocol = 'line'
        write_result = influxdb_obj.write_dataframe(dataframe,datatable,tags,protocol)
        print(write_result)

        return 'Save DataFrame Data Successful!'        


    def query(self,influxdb_obj):
        """
        方法功能：

            定义一个统一查询方法

        参数：
            influxdb_obj (Object): InfluxDB数据库对象

        返回：
            query_result (ResultSet): 查询结果        
        """

        datatable = self.__table_name__
        query_influxql = 'select * from {}'.format(datatable)
        query_result = influxdb_obj.query(query_influxql)

        return query_result



##########################################################################################################
##########################################################################################################


