






a = Faculty("Minerva McGonagall","041122","CSE",322)
b = Faculty("Severus Snape","054321","SWCON",433)
c = Student("Harry Potter","2016103701","SWCON")
d = Student("Hermione Granger","2017103702","CSE")
e = Student("Ron Weasley","2012103703","CSE") 

a.course_teaching = ["English"]
b.course_teaching = ["Python","Javascript"]

c.courses = ["English, Python", "Javascript"]
c.grades = ["B","A","B"]
d.courses = ["English, Python", "Javascript"]
d.grades = ["A","A","B"]
e.courses = ["English, Python", "Javascript", "Network"]
e.grades = ["D","A","B","C"]

print(a)
print(b)
print(c)
print(d)
print(e)
print()

