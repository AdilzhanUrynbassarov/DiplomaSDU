from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TeacherSerializer, CategorySerializer, CourseSerializer, ChapterSerializer, UserSerializer, UserCourseEnrollSerializer, UserFavoriteCourseSerializer, QuizSerializer, QuestionSerializer, QuizAssignCourseSerializer, AttemptQuizSerializer,  StudyMaterialSerializer, TeacherUserChatSerializer, UserAssignmentSerializer, ContactSerializer, FAQSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.mail import send_mail


#TEACHER
class TeacherList(generics.ListCreateAPIView):
	queryset=models.Teacher.objects.all()
	serializer_class = TeacherSerializer
	#permission_classes=[permissions.IsAuthenticated]


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Teacher.objects.all()
	serializer_class = TeacherSerializer
	#permission_classes=[permissions.IsAuthenticated]

@csrf_exempt
def teacher_login(request):
	email=request.POST['email']
	password=request.POST['password']
	try:
		teacherData=models.Teacher.objects.get(email=email, password=password)
	except models.Teacher.DoesNotExist:
		teacherData=None
	if teacherData:
		if not teacherData.verify_status:
			return JsonResponse({'bool': False, 'msg':'Account is not verified!'})
		else:
			return JsonResponse({'bool': True, 'teacher_id': teacherData.id})
	else:
		return JsonResponse({'bool': False, 'msg':'Invalid email or password!'})

@csrf_exempt
def verify_teacher_via_otp(request, teacher_id):
	otp_digit=request.POST.get('otp_digit')
	verify=models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).first()
	if verify:
		models.Teacher.objects.filter(id=teacher_id, otp_digit=otp_digit).update(verify_status=True)
		return JsonResponse({'bool': True, 'teacher_id': verify.id})
	else:
		return JsonResponse({'bool': False})


class CategoryList(generics.ListCreateAPIView):
	queryset=models.CourseCategory.objects.all()
	serializer_class = CategorySerializer
	#permission_classes=[permissions.IsAuthenticated]


class CourseList(generics.ListCreateAPIView):
	queryset=models.Course.objects.all()
	serializer_class = CourseSerializer

	def get_queryset(self):
		qs=super().get_queryset()
		if 'searchstring' in self.kwargs:
			search=self.kwargs['searchstring']
			qs=models.Course.objects.filter(title__icontains=search)
			
		return qs

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Course.objects.all()
	serializer_class = CourseSerializer


class TeacherCourseList(generics.ListAPIView):
	serializer_class = CourseSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		teacher_id=self.kwargs['teacher_id']
		teacher=models.Teacher.objects.get(pk=teacher_id)
		return models.Course.objects.filter(teacher=teacher)


class TeacherCourseDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Course.objects.all()
	serializer_class = CourseSerializer
	#permission_classes=[permissions.IsAuthenticated]


class ChapterList(generics.ListCreateAPIView):
	queryset=models.Chapter.objects.all()
	serializer_class = ChapterSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		course_id=self.kwargs['course_id']
		course=models.Course.objects.get(pk=course_id)
		return models.Chapter.objects.filter(course=course)


class ChapterCourseList(generics.ListAPIView):
	serializer_class = ChapterSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		course_id=self.kwargs['course_id']
		course=models.Course.objects.get(pk=course_id)
		return models.Chapter.objects.filter(course=course)

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Chapter.objects.all()
	serializer_class = ChapterSerializer
	#permission_classes=[permissions.IsAuthenticated]



#USER
class UserList(generics.ListCreateAPIView):
	queryset=models.Student.objects.all()
	serializer_class = UserSerializer
	#permission_classes=[permissions.IsAuthenticated]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Student.objects.all()
	serializer_class = UserSerializer
	
@csrf_exempt
def user_login(request):
	email=request.POST['email']
	password=request.POST['password']
	try:
		userData=models.Student.objects.get(email=email, password=password)
	except models.Student.DoesNotExist:
		userData=None
	if userData:
		if not userData.verify_status:
			return JsonResponse({'bool': False, 'msg':'Account is not verified!'})
		else:
			return JsonResponse({'bool': True, 'user_id': userData.id})
	else:
		return JsonResponse({'bool': False, 'msg':'Invalid email or password!'})

@csrf_exempt
def verify_user_via_otp(request, user_id):
	otp_digit=request.POST.get('otp_digit')
	verify=models.Student.objects.filter(id=user_id, otp_digit=otp_digit).first()
	if verify:
		models.Student.objects.filter(id=user_id, otp_digit=otp_digit).update(verify_status=True)
		return JsonResponse({'bool': True, 'user_id': verify.id})
	else:
		return JsonResponse({'bool': False})


class UserEnrollCourseList(generics.ListCreateAPIView):
	queryset=models.UserCourseEnrollment.objects.all()
	serializer_class = UserCourseEnrollSerializer
	#permission_classes=[permissions.IsAuthenticated]

class UserEnrollCourseListDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.UserCourseEnrollment.objects.all()
	serializer_class = UserCourseEnrollSerializer
	#permission_classes=[permissions.IsAuthenticated]


def fetch_enroll_status(request, user_id, course_id):
	user=models.Student.objects.filter(id=user_id).first()
	course=models.Course.objects.filter(id=course_id).first()
	enrollStatus=models.UserCourseEnrollment.objects.filter(course=course,user=user).count()
	if enrollStatus:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})


class EnrolledUserList(generics.ListAPIView):
	queryset=models.UserCourseEnrollment.objects.all()
	serializer_class = UserCourseEnrollSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		if 'course_id' in self.kwargs:
			course_id=self.kwargs['course_id']
			course=models.Course.objects.get(pk=course_id)
			return models.UserCourseEnrollment.objects.filter(course=course)
		elif 'teacher_id' in self.kwargs:
			teacher_id=self.kwargs['teacher_id']
			teacher=models.Teacher.objects.get(pk=teacher_id)
			return models.UserCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
		elif 'user_id' in self.kwargs:
			user_id=self.kwargs['user_id']
			user=models.Student.objects.get(pk=user_id)
			return models.UserCourseEnrollment.objects.filter(user=user).distinct()


class EnrolledUserListDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.UserCourseEnrollment.objects.all()
	serializer_class = UserCourseEnrollSerializer


@csrf_exempt
def teacher_change_password(request, teacher_id):
	password=request.POST['password']
	try:
		teacherData=models.Teacher.objects.get(id=teacher_id)
	except models.Teacher().DoesNotExist:
		teacherData=None
	if teacherData:
		models.Teacher.objects.filter(id=teacher_id).update(password=password)
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})


class UserFavoriteCourseList(generics.ListCreateAPIView):
	queryset=models.StudentFavoriteCourse.objects.all()
	serializer_class = UserFavoriteCourseSerializer

	def get_queryset(self):
		if 'user_id' in self.kwargs:
			user_id=self.kwargs['user_id']
			user=models.Student.objects.get(pk=user_id)
			return models.StudentFavoriteCourse.objects.filter(user=user).distinct()


@csrf_exempt
def fetch_fav_status(request, user_id, course_id):
	user=models.Student.objects.filter(id=user_id).first()
	course=models.Course.objects.filter(id=course_id).first()
	favStatus=models.StudentFavoriteCourse.objects.filter(course=course,user=user).first()
	if favStatus and favStatus.status==True:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})



@csrf_exempt
def remove_fav_course(request, course_id, user_id):
	user=models.Student.objects.filter(id=user_id).first()
	course=models.Course.objects.filter(id=course_id).first()
	favStatus=models.StudentFavoriteCourse.objects.filter(course=course,user=user).delete()
	if favStatus:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})



@csrf_exempt
def user_change_password(request, user_id):
	password=request.POST['password']
	try:
		userData=models.Student.objects.get(id=user_id)
	except models.Student.DoesNotExist:
		userData=None
	if userData:
		models.Student.objects.filter(id=user_id).update(password=password)
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})


class QuizList(generics.ListCreateAPIView):
	queryset=models.Quiz.objects.all()
	serializer_class = QuizSerializer
	#permission_classes=[permissions.IsAuthenticated]



class TeacherQuizList(generics.ListAPIView):
	serializer_class = QuizSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		teacher_id=self.kwargs['teacher_id']
		teacher=models.Teacher.objects.get(pk=teacher_id)
		return models.Quiz.objects.filter(teacher=teacher)

class TeacherQuizDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Quiz.objects.all()
	serializer_class = QuizSerializer
	#permission_classes=[permissions.IsAuthenticated]


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.Quiz.objects.all()
	serializer_class = QuizSerializer

class QuestionQuizList(generics.ListCreateAPIView):
	serializer_class = QuestionSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		quiz_id=self.kwargs['quiz_id']
		quiz=models.Quiz.objects.get(pk=quiz_id)
		if 'limit' in self.kwargs:
			return models.QuizQuestions.objects.filter(quiz=quiz).order_by('id')[:1]
		elif 'question_id' in self.kwargs:
			current_question=self.kwargs['question_id']
			return models.QuizQuestions.objects.filter(quiz=quiz, id__gt=current_question).order_by('id')[:1]
		else:
			return models.QuizQuestions.objects.filter(quiz=quiz)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.QuizQuestions.objects.all()
	serializer_class = QuestionSerializer


class QuizAssignedCourseList(generics.ListCreateAPIView):
	queryset=models.CourseQuiz.objects.all()
	serializer_class = QuizAssignCourseSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		if 'course_id' in self.kwargs:
			course_id=self.kwargs['course_id']
			course=models.Course.objects.get(pk=course_id)
			return models.CourseQuiz.objects.filter(course=course)



@csrf_exempt
def fetch_quiz_assign_status(request, quiz_id, course_id):
	quiz = models.Quiz.objects.filter(id=quiz_id).first()
	course = models.Course.objects.filter(id=course_id).first()
	assignStatus = models.CourseQuiz.objects.filter(course=course, quiz=quiz).count()

	if assignStatus:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})

class AttemptQuizList(generics.ListCreateAPIView):
	queryset=models.AttemptQuiz.objects.all()
	serializer_class = AttemptQuizSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		if 'quiz_id' in self.kwargs:
			quiz_id=self.kwargs['quiz_id']
			quiz=models.Quiz.objects.get(pk=quiz_id)
			return models.AttemptQuiz.objects.filter(quiz=quiz)

@csrf_exempt
def fetch_quiz_attempt(request, quiz_id, user_id):
	quiz = models.Quiz.objects.filter(id=quiz_id).first()
	user = models.Student.objects.filter(id=user_id).first()
	total_questions=models.QuizQuestions.objects.filter(quiz=quiz).count()
	total_attempted_questions=models.AttemptQuiz.objects.filter(quiz=quiz, user=user).values('user').count()
	attempted_questions=models.AttemptQuiz.objects.filter(quiz=quiz, user=user)

	total_correct_questions=0
	for attempt in attempted_questions:
		if attempt.right_ans==attempt.question.right_ans:
			total_correct_questions+=1
	return JsonResponse({'total_questions':total_questions, 'total_attempted_questions':total_attempted_questions, 'total_correct_questions':total_correct_questions})



@csrf_exempt
def fetch_quiz_attempt_status(request, quiz_id, user_id):
	quiz = models.Quiz.objects.filter(id=quiz_id).first()
	user = models.Student.objects.filter(id=user_id).first()
	attemptStatus = models.AttemptQuiz.objects.filter(user=user, question__quiz=quiz).count()

	if attemptStatus > 0:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})


class StudyMaterialList(generics.ListCreateAPIView):
	serializer_class = StudyMaterialSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		course_id=self.kwargs['course_id']
		course=models.Course.objects.get(pk=course_id)
		return models.StudyMaterial.objects.filter(course=course)


class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.StudyMaterial.objects.all()
	serializer_class = StudyMaterialSerializer
	#permission_classes=[permissions.IsAuthenticated]


@csrf_exempt
def teacher_forgot_password(request):
	email=request.POST.get('email')
	verify=models.Teacher.objects.filter(email=email).first()
	if verify:
		link=f"http://localhost:3000/teacher-change-forgot-password/{verify.id}"
		send_mail(
            'Құпиясөзді өзгеру!',
            'Құпиясөзді өзгеру',
            '190103021@stu.sdu.edu.kz',
            [email],
            fail_silently=False,
            html_message=f'<p>Төмендегі сілтеме бойынша құпиясөзді өзгерте аласыз. </p><p>{link}</p>'
        )
		return JsonResponse({'bool': True, 'msg':'Поштаңызды тексеруді өтінеміз!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})


@csrf_exempt
def teacher_change_forgot_password(request, teacher_id):
	password=request.POST.get('password')
	verify=models.Teacher.objects.filter(id=teacher_id).first()
	if verify:
		models.Teacher.objects.filter(id=teacher_id).update(password=password)
		return JsonResponse({'bool': True, 'msg':'Құпиясөз өзгертілді!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})



@csrf_exempt
def user_forgot_password(request):
	email=request.POST.get('email')
	verify=models.Student.objects.filter(email=email).first()
	if verify:
		link=f"http://localhost:3000/user-change-forgot-password/{verify.id}"
		send_mail(
            'Құпиясөзді өзгеру!',
            'Құпиясөзді өзгеру',
            '190103021@stu.sdu.edu.kz',
            [email],
            fail_silently=False,
            html_message=f'<p>Төмендегі сілтеме бойынша құпиясөзді өзгерте аласыз. </p><p>{link}</p>'
        )
		return JsonResponse({'bool': True, 'msg':'Поштаңызды тексеруді өтінеміз!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})


@csrf_exempt
def user_change_forgot_password(request, user_id):
	password=request.POST.get('password')
	verify=models.Student.objects.filter(id=user_id).first()
	if verify:
		models.Student.objects.filter(id=user_id).update(password=password)
		return JsonResponse({'bool': True, 'msg':'Құпиясөз өзгертілді!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})


@csrf_exempt
def save_teacher_student_msg(request, teacher_id, user_id):
	teacher=models.Teacher.objects.get(id=teacher_id)
	user=models.Student.objects.get(id=user_id)
	msg_text=request.POST.get('msg_text')
	msg_from=request.POST.get('msg_from')
	msgRes=models.TeacherUserChat.objects.create(
		teacher=teacher,
		user=user,
		msg_text=msg_text,
		msg_from=msg_from,
	)
	if msgRes:
		return JsonResponse({'bool': True, 'msg':'Хабарлама жіберілді!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})



class MessageList(generics.ListAPIView):
	queryset=models.TeacherUserChat.objects.all()
	serializer_class = TeacherUserChatSerializer
	
	def get_queryset(self):
		teacher_id=self.kwargs['teacher_id']
		user_id=self.kwargs['user_id']
		teacher=models.Teacher.objects.get(pk=teacher_id)
		user=models.Student.objects.get(pk=user_id)
		return models.TeacherUserChat.objects.filter(teacher=teacher, user=user).exclude(msg_text='')


@csrf_exempt
def save_teacher_group_msg(request, teacher_id):
	teacher=models.Teacher.objects.get(id=teacher_id)
	msg_text=request.POST.get('msg_text')
	msg_from=request.POST.get('msg_from')

	enrolledList=models.UserCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
	for enrolled in enrolledList:
		msgRes=models.TeacherUserChat.objects.create(
		teacher=teacher,
		user=enrolled.user,
		msg_text=msg_text,
		msg_from=msg_from,
	)
	if msgRes:
		return JsonResponse({'bool': True, 'msg':'Хабарлама жіберілді!'})
	else:
		return JsonResponse({'bool': False, 'msg':'Қате!'})


	
class MyTeacherList(generics.ListAPIView):
	queryset=models.Course.objects.all()
	serializer_class = CourseSerializer
	#permission_classes=[permissions.IsAuthenticated]

	def get_queryset(self):
		if 'user_id' in self.kwargs:
			user_id=self.kwargs['user_id']
			sql=f"SELECT * FROM main_course as c, main_usercourseenrollment as e, main_teacher as t WHERE c.teacher_id = t.id AND e.course_id=c.id AND e.user_id={user_id} GROUP BY c. teacher_id"
			qs=models.Course.objects.raw(sql)
			return qs	


class AssignmentList(generics.ListCreateAPIView):
	queryset=models.UserAssignment.objects.all()
	serializer_class = UserAssignmentSerializer

	def get_queryset(self):
		course_id=self.kwargs['course_id']
		course=models.Course.objects.get(pk=course_id)
		return models.UserAssignment.objects.filter(course=course)


class AssignmentListDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset=models.UserAssignment.objects.all()
	serializer_class = UserAssignmentSerializer



class ContactList(generics.ListCreateAPIView):
	queryset=models.Contact.objects.all()
	serializer_class = ContactSerializer
		
		
class FAQList(generics.ListAPIView):
	queryset=models.FAQ.objects.all()
	serializer_class = FAQSerializer


@csrf_exempt
def remove_enroll_course(request, course_id, user_id):
	user=models.Student.objects.filter(id=user_id).first()
	course=models.Course.objects.filter(id=course_id).first()
	enrollStatus=models.UserCourseEnrollment.objects.filter(course=course,user=user).delete()
	if enrollStatus:
		return JsonResponse({'bool': True})
	else:
		return JsonResponse({'bool': False})





