from django.db import models
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
class Teacher(models.Model):
	full_name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=100, blank=True, null=True)
	qualification=models.CharField(max_length=200)
	mobile_no=models.CharField(max_length=20)
	profile_img=models.ImageField(upload_to='teacher_profile_imgs/', null=True)
	skills=models.TextField()
	verify_status=models.BooleanField(default=False)
	otp_digit=models.CharField(max_length=10, null=True)

	facebook_url=models.URLField(null=True)
	twitter_url=models.URLField(null=True)
	instagram_url=models.URLField(null=True)
	website_url=models.URLField(null=True)


	class Meta:
		verbose_name_plural="1. Teachers"
	
	def __str__(self) :
		return self.full_name


class CourseCategory(models.Model):
	title=models.CharField(max_length=150)
	description=models.TextField()

	class Meta:
		verbose_name_plural="2. Course Categories"

	def __str__(self) :
		return self.title


class Course(models.Model):
	category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
	teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
	title=models.CharField(max_length=150)
	description=models.TextField()
	featured_img=models.ImageField(upload_to='course_imgs/', null=True)
	technologies=models.TextField(null=True)

	def __str__(self) :
		return self.title

	def total_enrolled_students(self):
		total_enrolled_students=UserCourseEnrollment.objects.filter(course=self).count()
		return total_enrolled_students

	class Meta:
		verbose_name_plural="3. Courses"


class Chapter(models.Model):
	course=models.ForeignKey(Course, on_delete=models.CASCADE)
	title=models.CharField(max_length=150)
	description=models.TextField()
	upload=models.FileField(upload_to='chapter_materials/', null=True)
	remarks=models.TextField(null=True)

	def __str__(self) :
		return self.title

	class Meta:
		verbose_name_plural="4. Chapters"


class Student(models.Model):
	full_name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=100,blank=True, null=True)
	username=models.CharField(max_length=200)
	interested_categories=models.TextField()
	profile_img=models.ImageField(upload_to='user_profile_imgs/', null=True)
	verify_status=models.BooleanField(default=False)
	otp_digit=models.CharField(max_length=10, null=True)

	def __str__(self) :
		return self.full_name

	class Meta:
		verbose_name_plural="5. Students"


class UserCourseEnrollment(models.Model):
	course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_courses')
	user=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_student')
	enrolled_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="6. Enrolled Courses"

	def __str__(self) :
		return f"{self.course}-{self.user}"


class StudentFavoriteCourse(models.Model):
	course=models.ForeignKey(Course, on_delete=models.CASCADE)
	user=models.ForeignKey(Student, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)

	class Meta:
		verbose_name_plural="7. User Favorite Courses"

	def __str__(self) :
		return f"{self.course}-{self.user}"  


class Quiz(models.Model):
	teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	title=models.CharField(max_length=200)
	detail=models.TextField()
	add_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="8. Quiz"

	def __str__(self) :
		return self.title

	def assign_status(self) :
		return CourseQuiz.objects.filter(quiz=self).count()

class QuizQuestions(models.Model):
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
	question=models.CharField(max_length=200)
	ans1=models.CharField(max_length=200)
	ans2=models.CharField(max_length=200)
	ans3=models.CharField(max_length=200)
	ans4=models.CharField(max_length=200)
	right_ans=models.CharField(max_length=200)
	add_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="9. Quiz Questions"

#Add quiz to course
class CourseQuiz(models.Model):
	teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
	add_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="10. Course Quizzes"

class AttemptQuiz(models.Model):
	user=models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
	question=models.ForeignKey(QuizQuestions, on_delete=models.CASCADE, null=True)
	right_ans=models.CharField(max_length=200, null=True)
	add_time=models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name_plural="11. Attempted Questions"



class StudyMaterial(models.Model):
	course=models.ForeignKey(Course, on_delete=models.CASCADE)
	title=models.CharField(max_length=150)
	description=models.TextField()
	upload=models.FileField(upload_to='study_materials/', null=True)
	remarks=models.TextField(null=True)

	def __str__(self) :
		return self.title

	class Meta:
		verbose_name_plural="12. Study Materials"


class TeacherUserChat(models.Model):
	teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
	user=models.ForeignKey(Student, on_delete=models.CASCADE)
	msg_text=models.TextField()
	msg_from=models.CharField(max_length=100)
	msg_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="13. Teacher Student Chat"


class UserAssignment(models.Model):
	course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
	title=models.CharField(max_length=200)
	detail=models.TextField(null=True)
	upload=models.FileField(upload_to='assignments/', null=True)
	user_status=models.BooleanField(default=False, null=True)
	add_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="14. User Assignments"

	def __str__(self) :
		return self.title


class Contact(models.Model):
	full_name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	detail=models.TextField(null=True)
	add_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="15. Contacts"

	def __str__(self) :
		return self.full_name

	def save(self, *args, **kwargs):
		send_mail(
            'Сәлеметсіз бе!',
            'Байланысқа шыққаныңыз үшін рахмет! Біздің менеджер сізбен қысқа уақыт аралығында хабарласады.',
            '190103021@stu.sdu.edu.kz',
            [self.email],
            fail_silently=False,
            
        )
		return super(Contact, self).save(*args, **kwargs)


class FAQ(models.Model):
	question=models.CharField(max_length=300)
	answer=models.TextField(null=True)

	class Meta:
		verbose_name_plural="16. FAQ"

	def __str__(self) :
		return self.question






