from django.db import models

IMP_CHOICES = (
    ('Nepal', 'Nepal'),
    ('Bhutan', 'Bhutan'),
    ('Sweden', 'Sweden'),
)


class School(models.Model):
    name = models.CharField(max_length=200, blank=False)
    street_address = models.CharField(max_length=200, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=200, blank=False)
    country = models.CharField(max_length=100, choices=IMP_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=500, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    # program = models.ManyToManyField(Program)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=400, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=200, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Building(models.Model):
    name_or_number = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name_or_number


class Room(models.Model):
    room_number = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.room_number


class SchoolAnnouncement(models.Model):
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(max_length=1000, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProgramAnnouncement(models.Model):
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(max_length=1000, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseAnnouncement(models.Model):
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(max_length=1000, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseSchedule(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=False)
    password = models.CharField(max_length=100)
    street_address = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    dob = models.DateField(max_length=8)
    subject_of_interest = models.CharField(max_length=200, blank=True, null=True)
    special_care_needed = models.CharField(max_length=1, choices=(
        ('Y', 'Yes'),
        ('N', 'No')
    ))

class QuizQuestion(models.Model):
    question = models.CharField(max_length = 200)
    ismcq = models.BooleanField()
    correct_answer = models.BooleanField(max_length = 200)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    no_of_question = models.IntegerField()
    full_marks = models.IntegerField()
    pass_marks = models.IntegerField()

class QuizSubjectiveQuestion(models.Model):
    question = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)

class QuizQuestionOption(models.Model):
    quizquestionid = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE)
    option1 = models.CharField(max_length = 200)
    option2 = models.CharField(max_length = 200)
    option3 = models.CharField(max_length = 200)
    option4 = models.CharField(max_length = 200)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now_add=True)

class StudentQuizQuestionAttempt(models.Model):
    student = models.ForeignKey(User, on_delete = models.CASCADE)
    quizquestionid = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    starting_working_on = models.DateTimeField(auto_now_add=True)
    completed_workinig_on = models.DateTimeField(auto_now_add=True)
    no_of_attempts = models.IntegerField()
    answer = models.CharField(max_length = 200)

class Student_Subjective_Quiz_Attempt(models.Model):
    student = models.ForeignKey(User, on_delete = models.CASCADE)
    quizquestionid = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    starting_working_on = models.DateTimeField(auto_now_add=True)
    completed_workinig_on = models.DateTimeField(auto_now_add=True)
    no_of_attempts = models.IntegerField()
    answer = models.CharField(max_length = 200)


