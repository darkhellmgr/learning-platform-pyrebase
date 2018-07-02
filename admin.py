from django.contrib import admin
from mainapp.models import (
    Course,
    School,
    Room,
    Building,
    Program,
    Topic,
    CourseSchedule,
    SchoolAnnouncement,
    CourseAnnouncement,
    ProgramAnnouncement
)

admin.site.register(School)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(CourseSchedule)
admin.site.register(CourseAnnouncement)
admin.site.register(ProgramAnnouncement)
admin.site.register(SchoolAnnouncement)