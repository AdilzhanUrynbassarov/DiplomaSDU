from django.urls import path
from . import views

urlpatterns = [
    #Teacher
    path('teacher/', views.TeacherList.as_view()),
    path('teacher/<int:pk>/', views.TeacherDetail.as_view()),
    path('teacher/change-password/<int:teacher_id>/', views.teacher_change_password),
    path('teacher-login', views.teacher_login),
    path('teacher-verify/<int:teacher_id>/', views.verify_teacher_via_otp),
    path('teacher-forgot-password/', views.teacher_forgot_password),
    path('teacher-change-forgot-password/<int:teacher_id>/', views.teacher_change_forgot_password),
    path('send-message/<int:teacher_id>/<int:user_id>', views.save_teacher_student_msg),
    path('get-messages/<int:teacher_id>/<int:user_id>', views.MessageList.as_view()),
    path('send-group-message/<int:teacher_id>/', views.save_teacher_group_msg),

    #Category
    path('category/', views.CategoryList.as_view()),

    #Course
    path('course/', views.CourseList.as_view()),
    path('course/<int:pk>/', views.CourseDetailView.as_view()),
    path('search-courses/<str:searchstring>', views.CourseList.as_view()),
    path('teacher-search-courses/<str:searchstring>', views.CourseList.as_view()),
    path('general-search-courses/<str:searchstring>', views.CourseList.as_view()),

    #Chapter
    path('chapter/', views.ChapterList.as_view()),
    path('chapter/<int:pk>/', views.ChapterDetailView.as_view()),
    path('chapters/<int:course_id>', views.ChapterList.as_view()),
    path('user/chapters/<int:course_id>', views.ChapterList.as_view()),

    #Specific course chapter
    path('course-chapters/<int:course_id>', views.ChapterCourseList.as_view()),

    #Specific chapter
    #path('chapter/<int:pk>', views.ChapterDetailView.as_view()),

    #Teacher Courses
    path('teacher-courses/<int:teacher_id>/', views.TeacherCourseList.as_view()),

    #Course Detail
    path('teacher-course-detail/<int:pk>/', views.TeacherCourseDetail.as_view()),

    #User
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('user-login', views.user_login),
    path('user-enroll-course/', views.UserEnrollCourseList.as_view()),
    path('fetch_enroll_status/<int:user_id>/<int:course_id>', views.fetch_enroll_status),
    path('fetch_enrolled_users/<int:course_id>', views.EnrolledUserList.as_view()),
    path('fetch-all-enrolled-users/<int:teacher_id>', views.EnrolledUserList.as_view()),
    path('fetch_enrolled_courses/<int:user_id>', views.EnrolledUserList.as_view()),
    path('user-add-favorite-course/', views.UserFavoriteCourseList.as_view()),
    path('user-remove-favorite-course/<int:course_id>/<int:user_id>', views.remove_fav_course),
    path('fetch-fav-status/<int:user_id>/<int:course_id>', views.fetch_fav_status),
    path('fetch-fav-courses/<int:user_id>', views.UserFavoriteCourseList.as_view()),
    path('user/change-password/<int:user_id>/', views.user_change_password),
    path('user-verify/<int:user_id>/', views.verify_user_via_otp),
    path('user-forgot-password/', views.user_forgot_password),
    path('user-change-forgot-password/<int:user_id>/', views.user_change_forgot_password),
    path('fetch-my-teachers/<int:user_id>/', views.MyTeacherList.as_view()),
     path('user-remove-enroll-course/<int:course_id>/<int:user_id>', views.remove_enroll_course),
   
    

    
    #Quiz
    path('quiz/', views.QuizList.as_view()),
    path('teacher-quizzes/<int:teacher_id>/', views.TeacherQuizList.as_view()),
    path('teacher-quiz-detail/<int:pk>/', views.TeacherQuizDetail.as_view()),
    path('quiz/<int:pk>/', views.QuizDetailView.as_view()),
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('quiz-questions/<int:quiz_id>', views.QuestionQuizList.as_view()),
    path('quiz-questions/<int:quiz_id>/<int:limit>', views.QuestionQuizList.as_view()),
    path('quiz-assign-course/', views.QuizAssignedCourseList.as_view()),
    path('fetch-quiz-assign-status/<int:quiz_id>/<int:course_id>', views.fetch_quiz_assign_status),
    path('fetch-assigned-quiz/<int:course_id>', views.QuizAssignedCourseList.as_view()),
    path('attempt-quiz/', views.AttemptQuizList.as_view()),
    path('quiz-questions/<int:quiz_id>/next-question/<int:question_id>', views.QuestionQuizList.as_view()),
    path('fetch-quiz-attempt-status/<int:quiz_id>/<int:user_id>', views.fetch_quiz_attempt_status),
    path('attempted-quiz/<int:quiz_id>', views.AttemptQuizList.as_view()),
    path('fetch-quiz-result/<int:quiz_id>/<int:user_id>/', views.fetch_quiz_attempt),
    
    #Study materials
    path('study-materials/<int:course_id>', views.StudyMaterialList.as_view()),
    path('study-material/<int:pk>/', views.StudyMaterialDetailView.as_view()),
    path('user/study-materials/<int:course_id>', views.StudyMaterialList.as_view()),

    #Assignment
    #path('assignment/<int:teacher_id>/<int:user_id>', views.AssignmentList.as_view()),
    path('assignment/<int:course_id>', views.AssignmentList.as_view()),
    path('assignmentd/<int:pk>/', views.AssignmentListDetailView.as_view()),
    path('user/assignments/<int:course_id>', views.AssignmentList.as_view()),

    #Contact
     path('contact/', views.ContactList.as_view()),

    #FAQ
     path('faq/', views.FAQList.as_view()),

    
]