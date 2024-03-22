from django.urls import path, re_path
from .views import *
from . import views
from djmoney.models.fields import *

urlpatterns = [
    # listviews
    path(
        "update-preferences/",
        UserPreferencesUpdateView.as_view(),
        name="update_preferences",
    ),
    path("lecturerprofile/", lecturerDetailView.as_view(), name="lecturer-profile"),
    path(
        "submit-quiz/<int:test_id>/",
        TopicsQuizSubmissionView.as_view(),
        name="submit-quiz",
    ),
    path("search-results/", SearchResultsView.as_view(), name="search_results"),
    path(
        "quiz/<int:topicid>/",
        quizpageView.as_view(),
        name="quizpage",
    ),
    #    path(
    #        "generate/<int:topicid>/",
    #        generatesubtitle.as_view(),
    #        name="generate",
    #    ),
    path(
        "submit-answer/<int:obj_id>/",
        submitobj.as_view(),
        name="submit-answer",
    ),
    path(
        "submit-theory/<int:topicid>/",
        submitheory.as_view(),
        name="submit-theory",
    ),
    path(
        "updatetopic/<int:topicid>/",
        topicupdate.as_view(),
        name="topicupdate",
    ),
    path(
        "submit-options/<int:quiz_id>/",
        objSubmissionView.as_view(),
        name="submit-option",
    ),
    path("coursedashboard/", cousedashboard.as_view(), name="coursedashboard"),
    path("courses/", courseListView.as_view(), name="courses"),
    path("", PostListView.as_view(), name="studypal-home"),
    # template views
    path("welcomelecturer/", orientationView.as_view(), name="welcomelecturer"),
    path("welcometeacher/", teacherorientView.as_view(), name="welcometeacher"),
    # CreateView Urls
    path(
        "courses/new/",
        createcourse.as_view(template_name="studypal/course_form.html"),
        name="course-create",
    ),
    path("topicdesc/<int:pk>/", topicdescription.as_view(), name="topic-description"),
    path(
        "create-topic/<int:course_id>/",
        createtopic.as_view(template_name="studypal/topics_form.html"),
        name="topic-create",
    ),
    path(
        "create-section/<int:topic_id>/",
        createsection.as_view(template_name="studypal/section_form.html"),
        name="section-create",
    ),
    path("quizpg/<int:pk>/", questiondetailview.as_view(), name="quizpg"),
    path(
        "enrollstudent/<int:course_id>/",
        enrollmentview.as_view(),
        name="course-enroll",
    ),
    path("studyurl/selectcourse/", CourseSelectView.as_view(), name="select_course"),
    path("courses/<int:pk>/", courseDetailView.as_view(), name="course-detail"),
    path("topics/<int:pk>/", topicdetailview.as_view(), name="topic-detail"),
    path("topic/<int:pk>/", topicview.as_view(), name="topic-view"),
    path(
        "lecturer/new/",
        createlecturer.as_view(template_name="studypal/lectureform.html"),
        name="lecturer-create",
    ),
]
