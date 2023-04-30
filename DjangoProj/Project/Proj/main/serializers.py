from rest_framework import serializers
from . import models
from django.core.mail import send_mail

#TEACHER	
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Teacher
        fields=['id', 'full_name', 'email', 'password', 'qualification', 'mobile_no', 'profile_img', 'skills', 'verify_status','otp_digit', 'facebook_url', 'twitter_url', 'instagram_url', 'website_url']

    def create(self, validated_data):
        email=self.validated_data['email']
        otp_digit=self.validated_data['otp_digit']
        instance=super(TeacherSerializer, self).create(validated_data)
        send_mail(
            'Аккаунтты растау!',
            'Өтініш, аккаунтыңызды растаңыз.',
            '190103021@stu.sdu.edu.kz',
            [email],
            fail_silently=False,
            html_message=f'<p>Өтініш, аккаунтыңызды растаңыз.</p> <p>6 цифрлы код:{otp_digit}</p>'
        )
        return instance
		

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model=models.CourseCategory
		fields=['id', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Course
		fields=['id', 'category', 'teacher', 'title', 'description', 'featured_img', 'technologies', 'total_enrolled_students']

	def __init__(self, *args, **kwargs):
		super(CourseSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2
		
		

class ChapterSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Chapter
		fields=['id', 'course', 'title', 'description', 'upload', 'remarks']

	def __init__(self, *args, **kwargs):
		super(ChapterSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=1


#USER
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Student
		fields=['id', 'full_name', 'email', 'password', 'username','interested_categories', 'profile_img', 'verify_status','otp_digit']

	def create(self, validated_data):
		email=self.validated_data['email']
		otp_digit=self.validated_data['otp_digit']
		instance=super(UserSerializer, self).create(validated_data)
		send_mail(
            'Аккаунтты растау!',
            'Өтініш, аккаунтыңызды растаңыз.',
            '190103021@stu.sdu.edu.kz',
            [email],
            fail_silently=False,
            html_message=f'<p>Өтініш, аккаунтыңызды растаңыз.</p> <p>6 цифрлы код:{otp_digit}</p>'
        )
		return instance

class UserCourseEnrollSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.UserCourseEnrollment
		fields=['id', 'course', 'user', 'enrolled_time']
	def __init__(self, *args, **kwargs):
		super(UserCourseEnrollSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2
	


class UserFavoriteCourseSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.StudentFavoriteCourse
		fields=['id', 'course', 'user', 'status']
	def __init__(self, *args, **kwargs):
		super(UserFavoriteCourseSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2


class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.Quiz
		fields=['id', 'teacher', 'title', 'detail', 'assign_status', 'add_time']
	def __init__(self, *args, **kwargs):
		super(QuizSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.QuizQuestions
		fields=['id', 'quiz', 'question', 'ans1', 'ans2', 'ans3', 'ans4','right_ans']

	def __init__(self, *args, **kwargs):
		super(QuestionSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2


class QuizAssignCourseSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.CourseQuiz
		fields=['id','teacher', 'course', 'quiz', 'add_time']
	def __init__(self, *args, **kwargs):
		super(QuizAssignCourseSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2


class AttemptQuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.AttemptQuiz
		fields=['id','user', 'quiz', 'question','right_ans', 'add_time']
	def __init__(self, *args, **kwargs):
		super(AttemptQuizSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=2


class StudyMaterialSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.StudyMaterial
		fields=['id', 'course', 'title', 'description', 'upload', 'remarks']

	def __init__(self, *args, **kwargs):
		super(StudyMaterialSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=1


class TeacherUserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.TeacherUserChat
        fields=['id', 'teacher', 'user', 'msg_text', 'msg_from', 'msg_time']

    def to_representation(self, instance):
	    representation = super(TeacherUserChatSerializer, self).to_representation(instance)
	    representation['msg_time'] = instance.msg_time.strftime('%Y-%m-%d %H:%M')
	    return representation


class UserAssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=models.UserAssignment
		fields=['id', 'course', 'title', 'detail', 'upload', 'add_time']

	def __init__(self, *args, **kwargs):
		super(UserAssignmentSerializer, self).__init__(*args, **kwargs)
		request=self.context.get('request')
		self.Meta.depth=0
		if request and request.method == 'GET':
			self.Meta.depth=1


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Contact
        fields=['id', 'full_name', 'email', 'detail']
		


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.FAQ
        fields=['id', 'question', 'answer']



