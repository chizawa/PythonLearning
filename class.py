# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:55:29 2018

@author: Administrator
"""
#子类的类型判断 issubclass
#实例类型判断 isinstance
class Programmer(object):
    hobby = 'Play computer'
    
    def __init__(self,name,age,*weight): #实例方法的第一参数
        self.name = name
        if isinstance(age,int):
            self._age = age  #protect
        self.__weight = weight  #private
    
    
    #运算符
    
    #比较运算符
    #__cmp__(self,other)(包含所有比较情况 一般用于排序)
    #__eq__(self,other),__lt__(self,other),__gt__(self,other)
    def __eq__ (self,other):
        if isinstance(other,Programmer):
            if other._age == self._age:
                return True
            else:
                return False
        else:
            raise Exception('The type of object must be a Programmer')
    
    #数字运算符
    #__add__(self,other),__sub__(self,other),__mul__(self,other),__div__(self,other)
    def __add__(self,other):
        if isinstance(other,Programmer):
            return self._age + other._age
        else:
            raise Exception('The type of object must be a Programmer')
        
    #逻辑运算符
    #__or__(self,other),__and__(self,other)
    def __and__(self,other):
        if isinstance(other,Programmer):
            return other._age + Programmer._age
        else:
            raise Exception('The type of object must be a Programmer')


    #转化为字符串
    #__str__ 转化为适合人看的字符串
    #__repr__转化为适合机器看的字符串 输出可以直接使用eval
    #__unicode__
    def __str__(self):
        return '%s is %d years old.'%(self.name,self._age)

    
    
    #选择性地展现对象属性
    #__dir__
    def __dir__(self):
        return self.__dict__.keys()

    
    #设置对象属性
    def __setattr__(self,name,value):
        self.__dict__[name] = value
                     
    #查询对象属性
    #__getattr__(self,name) #默认属性没有被查询到
    #__getattribute(self,name) #每次访问 容易引起无限调用
    def __getattribute__(self,name):
        #__dict__[name]调用getattribute 造成无限调用
        return super(Programmer,self).__getattribute__(name) #调用父类方法
                   
    #删除对象属性
    #__delattr__(self,name)


   
    @classmethod #调用的时候用类名，而不是某个对象
    def get_hobby(cls):  #类方法的第一参数
        return cls.hobby
    
    @property  #像访问属性一样调用方法      
    def get_weight(self):
        return self.__weight
    
    def self_introduction(self):
        print('My name is %s\nMy age is %d years old\n' %(self.name,self._age))
    
    
class BackendProgrammer(Programmer):
    
    def __init__(self,name,age,weight,language):
        super(BackendProgrammer,self).__init__(name,age,weight) #调用父类
        # Programmer.__init__(name,age,weight)  
        self.language = language
        
    def self_introduction(self):
        print('My name is %s\nMy favorite language is %s\n' %(self.name,self.language))
        
        
def introduce(programmer):
    if isinstance(programmer,Programmer):
        programmer.self_introduction()
    
        
if __name__ == '__main__':
    programmer = Programmer('Tim',23,74)
    back_end_programmer = BackendProgrammer('Albert',26,65,'Python')
    print(programmer.get_weight)
    print(Programmer.hobby)
    introduce(programmer)
    introduce(back_end_programmer)
    
    p1 = Programmer('Jack',56)
    p2 = Programmer('Rose',48)
    print(p1 == p2)
    print(p1+p2)
    
    
    
    