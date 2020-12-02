class Animal:
    
    # 这里是属性定义
    actually = "animal" # 类属性
    
    def __init__(self, name, age): # 定义实例时，放在括号里的才要指定
        self.name = name # 普通属性，要在__init__方法中定义
        self.age = age
    
    # 下面是方法的定义
    def sleep(self): # 普通方法
        print(self.name, "is sleeping")
        
    def eat(self, food): # 普通方法，另带参数
        print(self.name, "is eating", food)
    
    @classmethod
    def sentence(cls, adv): # 类方法，使用装饰器变成类方法
        print("I am", adv, "an", cls.actually)
    
    @staticmethod
    def other(person, do): # 静态方法
        print(person, "is", do+"ing")
    
    @staticmethod
    def print_animal():
        print("这是之后定义子类的父类，主要讲解最基本的属性、方法以及属性的修改")
        print("类属性actually：属于整个类，每个实例都有的属性，内容相同，创建实例时不需要指定，类和实例都可以调用")
        print("普通属性name age：属于各个实例，用于存储实例数据")
        
        print("普通方法sleep eat：由对象调用，至少一个参数self")
        print("类方法sentence：由类、实例调用，至少一个参数cls，可以引用类属性")
        print("静态方法other：类中的普通函数，可由类、实例调用")
        
        print("修改类属性：用类调用修改，所有实例都更改；用实例调用修改不影响类和其他实例")
        print("修改普通属性：直接赋值即可")
        
        
class Dog(Animal): # 类的继承
    
    # 只使用@property装饰器与普通函数做对比
    def eating(self):
        print("I am eating")
    
    @property # 用这个装饰器后这个方法调用就可以不加括号，即将其转化为属性
    def running(self): 
        if self.age >= 3 and self.age < 130:
            print("I am running")
        elif self.age > 0 and self.age <3:
            print("I can't run")
        else:
            print("please input true age")
            
    # 三种装饰器，可以获取、设置、删除这样定义的属性
    @property
    def country(self):
        return self._country # 注意这个属性之前从来没有定义过，是在下面的setter中定义的
    
    @country.setter # 用 函数名.setter 的装饰器
    def country(self, value): # 设置这个属性的值
        self._country = value
        
    @country.deleter
    def country(self):
        print("The attr country is deleted")
        
        
    # 用property函数实现和装饰器相同的功能
    def get_city(self):
        return self._city
    
    def set_city(self, value):
        self._city = value
        
    def del_city(self, value):
        del self._city
        
    city = property(get_city, set_city, del_city, "where it is in")
        
    @staticmethod
    def print_dog():
        print("这是Animal的一个子类，主要讲解三个装饰器进行方法向属性的转换")
        print("类继承，创建实例时仍要指定父类的普通属性")
        print("@property装饰器将方法转化为属性方式调用，此时的方法必须只有一个self参数")
        print("使用@property后可以看做一个属性(country)，用property函数可以达到相同的效果(city)")
        print("注：city中property第四个参数只是一个说明，用Dog.city.__doc__来调用，即返回 where it is in")
        
        
class Cat(Animal):
    
    def __init__(self, weight): # 覆盖了父类的__init__，所以定义实例时不需要指定name和age
        self.__weight = weight
        self._weight = weight + 1
        self.weight = self._weight + 1
    
    def get_myweight(self):
        print("My weight is", self._weight, "kg")
    
    def get_trueweight(self):
        print("Actually the cat's weight is",self.__weight)
    
    @staticmethod
    def print_cat():
        print("这个类是Animal类的子类，也是Blackcat类的父类")
        print("Cat类和Blackcat类结合，主要用于讲解私人属性、方法的继承与覆盖")
        
        print("weight是普通属性，可以在外部访问，即用类调用属性获得，可以被子类内部调用")
        print("_weight这样前面加一个下划线表示希望你不要在外部访问它，但是还是可以访问的，可以被子类内部调用")
        print("__weight这样加两个下划线的是不允许外部访问的，只可以在类中被调用，不可以被子类内部调用")
        
        print("__init__在子类中定义则覆盖了父类中的__init__，不需要指定父类中的属性，也无法调用父类的属性")
        print("在子类中实现和父类同名的方法，也会把父类的方法覆盖掉")
        
class Blackcat(Cat):
    
    def get_weight(self):
        print("My weight is", self.weight)
    
    def get_weight_again(self): # 可以
        print("Actuall my weight is", self._weight)
        
    def get_true_weight(self): # 这个方法因为无法调用self.__weight所以这个方法无法使用
        print("My weight is exactly", self.__weight)
        
    def get_trueweight(self): # 覆盖了Cat父类中定义的方法
        print("My weight is exactly", self._weight+1)
        
        
        
class Tiger:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def eat(self):
        return "I am eating"
    
    def myname(self):
        return "my name is " + self.name

class Whitetiger(Tiger):
    
    def __init__(self, name, age, height):
        super(Whitetiger, self).__init__(name, age) # 1
        self.height = height

    def eatmore(self):
        return super(Whitetiger, self).eat() + " more" # 2
    
    def realname(self):
        return "Actually " + super(Whitetiger, self).myname()