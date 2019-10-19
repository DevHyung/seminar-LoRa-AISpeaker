class Member:
    """A member of a university"""

    def __init__(self, name, mid, dept):
        """(Member, str, str, str) -> NoneType
        """
        self.name = name
        self.id = mid
        self.dept = dept

    def __str__(self):
        """(Member) -> str
        """
        rep = "{} ({}): {}".format(self.name, self.id, self.dept)
        return rep

class Faculty(Member):
    """A faculty member at a university"""
    

    def __init__(self, name, mid, dept, roomnum):
        """(Faculty, str, str, str, int) -> NoneType
        """
        super().__init__(name, mid, dept)
        self.roomnum = roomnum
        self.course_teaching = []

    def __str__(self):
        """(Faculty) -> str
        """
        member_string = super().__str__()
        rep = "{}\nRoom #{}\nTeaching: {}".format(
            member_string, self.roomnum, self.course_teaching)
        return rep
        

class Student(Member):
    """A Student member at a university"""

    def __init__(self, name, mid, dept):
        """(Faculty, str, str, str, int) -> NoneType
        """
        super().__init__(name, mid, dept)
        self.enteryear = int(mid[:4])
        self.courses = []
        self.grades = []
    

    def getYear(self, thisyear):
        year = thisyear - self.enteryear + 1
        year_str = ""
        if year == 1:
            year_str = "Freshmen"
        elif year == 2:
            year_str = "Sophomore"
        elif year == 3:
            year_str = "Junior"
        elif year == 4:
            year_str = "Senior"
        else:
            year_str = "About to graduate"
        return year_str

    def getGPA(self):
        total = 0.0
        for g in self.grades:
            if g == "A":
                total += 4.0
            elif g == "B":
                total += 3.0
            elif g == "C":
                total += 2.0
            elif g == "D":
                total += 1.0
            else:
                total += 0.0
        gpa = total / len(self.grades)
        return gpa


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
print(c.name,"is",c.getYear(2017))
print(d.name,"is",d.getYear(2017))
print(e.name,"is",e.getYear(2017))
print(c.name,"GPA is",round(c.getGPA(),2))
print(d.name,"GPA is",round(d.getGPA(),2))
print(e.name,"GPA is",round(e.getGPA(),2))
