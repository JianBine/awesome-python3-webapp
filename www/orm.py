#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import asyncio,logging
import aiomysql
def log(sql,args=()):
    logging.info('SQL: %s' % sql)

#创建连接池
async def create_pool(loop,**kw):
    logging.info('create database conneciton pool ……')
    global __pool
    __pool = await aiomysql.create(
        host = kw.get('host','localhost'),
        port = kw.get('port',3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset','utf-8),
        autocommit = kw.get('autocommit',True),
        maxsize = kw.get('maxsize',10),
        minsize = kw.get('minsize',1),
        loop = loop
    )

#创建SQL查询语句
#@return list
async def select(sql,args,size=None):
    log(sql,args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
        	#需要回头理解
            await cur.execute(sql.replace('?','%s'),args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs

#创建SQL添加、修改、删除语句
#@return affectNum
async def execute(sql,args,autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?','%s'),args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
            #如果发生raise，后面的语句不能运行
        return affected

#拼接参数字段，如['2','3','4'……]
def create_args_string(num):
    L = []
    for n in range(num):
        L.append(n)
    return ','.join(L)

#字段属性
class Field(object):

    def __init__(self,name,column_type,primary_key,default):
    	self.name = name
    	self.column_type = column_type
    	self.primary_key = primary_key
    	self.default = default

    def __str__():
        return '<%s, %s:%s>' % (self.__class__.__name__,self.column_type,self.name)

#初始化字段类型为varchar(100)
class StringField(Field):

    def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)

#初始化字段类型为bool
class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)
#初始化字段类型为Integer
class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)
#初始化字段类型为Float
class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

#初始化字段类型为Text
class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)



