from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Teacher)
admin.site.register(models.CourseCategory)
admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.Student)
admin.site.register(models.UserCourseEnrollment)
admin.site.register(models.StudentFavoriteCourse)
admin.site.register(models.Quiz)
admin.site.register(models.QuizQuestions)
admin.site.register(models.CourseQuiz)
admin.site.register(models.AttemptQuiz)
admin.site.register(models.StudyMaterial)
admin.site.register(models.TeacherUserChat)
admin.site.register(models.UserAssignment)
admin.site.register(models.Contact)
admin.site.register(models.FAQ)