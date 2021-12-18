# def update_dict(key, value, defaults={}):
#     defaults[key] = value
#     print(defaults)
    
    
# update_dict(key='fruit', value='apple')
# update_dict(key='vegetable', value='tomato', defaults = {'tree': 'oak'})
# update_dict(key='car', value='ferrari')


# class Animal:
#     def say(self):
#         print('i am animal')
 
 
# class Cat(Animal):
#     pass
 
 
# class Robot:
#     def say(self):
#         print('i am robot')
 
 
# class RoboCat(Cat, Robot):
#     pass
 
 
# robo = RoboCat()
# robo.say()


# first_list = [[0, 1, 2], [3, 4, 5]]
# second_list = list(first_list)
# first_list.append([6, 7, 8])
# print(second_list)
# first_list[1][0] = 9
 
# print(first_list)
# print(second_list)


def multipliers():
    return [lambda x: i * x for i in range(4)]
 
print([m(2) for m in multipliers()])

def multipliers():
    return [lambda x: i * x for i in range(10)]
 
print([m(4) for m in multipliers()])


# for site in Site.objects.get(self.email)
#     print(site.user.email)