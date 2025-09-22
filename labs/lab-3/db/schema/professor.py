"""professor.py: create a table named professors in the marist database"""
from db.server import db

class Professor(db.Model):
    __tablename__ = 'Professors'
    ProfessorID = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ProfessorFirst = db.Column(db.String(40))
    ProfessorLast = db.Column(db.String(40))
    ProfessorEmail = db.Column(db.String(40))

    # create relationship with courses table. assoc table name = ProfessorCourse
    course = db.relationship('Courses', secondary = 'ProfessorCourse', back_populates = 'Professors')
    def __init__(self, name):
        self.ProfessorFirst = self.ProfessorFirst
        self.ProfessorLast = self.ProfessorLast
        self.ProfessorEmail = self.ProfessorEmail

    def __repr__(self):
        return f"""
            "PROFESSOR FIRST NAME: {self.ProfessorFirst},
             PROFESSOR LAST NAME: {self.ProfessorLast},
             PROFESSOR EMAIL: {self.ProfessorEmail}
        """
    
    def __repr__(self):
        return self.__repr__()