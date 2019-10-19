class Student:
    name = ""
    id = 0
    gender = "female"
    course = []

    def num_courses(self):
        return len(self.course)


a = Student()
b = Student()
c = Student()


a.name = "Harry Potter"
a.id = 2017103701
a.gender = "male"

b.name = "Hermione Granger"
b.id = 2018103722
b.birthyear = 1999

c.name = "Ron Weasley"

a.course = ["English","Programming"]
b.course = ["Writing","Physics","Programming"]
c.course = ["Programming"]
    
