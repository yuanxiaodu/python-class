# 类定义
class People:
    #定义构造方法
    def __init__(self,n,a):
        self.name = n
        self.age = a
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

# 单继承示例
class Student(People):
    def __init__(self,n,a,g):
        #调用父类的构函
        super(Student, self).__init__(n,a)
        self.grade = g
    #覆写父类的方法
    def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))

