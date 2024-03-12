from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import *
from django.db.models import Q
from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseForbidden

import math
import requests
import time
import uuid
import environ
from json import JSONDecodeError
from users.models import *

# import speech_recognition as sr
# from moviepy.editor import *
# import assemblyai as aai
import os

base_dir = settings.BASE_DIR

optype = (
    ("op1", "Op1"),
    ("op2", "Op2"),
    ("op3", "Op3"),
    ("op4", "Op4"),
)


class UserPreferencesForm(forms.Form):
    font_size = forms.IntegerField(
        initial=16,
        widget=forms.NumberInput(
            attrs={"min": 1, "max": 50, "type": "range", "class": "form-range"}
        ),
        label="Font Size",
    )
    word_spacing = forms.IntegerField(
        initial=5,
        widget=forms.NumberInput(
            attrs={"min": 1, "max": 50, "type": "range", "class": "form-range"}
        ),
        label="Word Spacing",
    )
    color_theme = forms.CharField(
        max_length=7,  # Assuming the color will be represented as a 7-character hex code
        initial="#ffffff",  # Set an initial color (white in this case)
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control"}),
        label="Color Theme",
    )
    font_color = forms.CharField(
        max_length=7,  # Assuming the color will be represented as a 7-character hex code
        initial="#000000",  # Set an initial color (white in this case)
        widget=forms.TextInput(attrs={"type": "color", "class": "form-control"}),
        label="Font Color",
    )
    brightness = forms.IntegerField(
        initial=100,
        widget=forms.NumberInput(
            attrs={"min": 1, "max": 100, "type": "range", "class": "form-range"}
        ),
        label="Brightness",
    )


class ansForm(forms.Form):
    answerfilled = forms.ChoiceField(
        label="Choose Only One of the below",
        choices=optype,
        widget=forms.RadioSelect,
    )


class theoryForm(forms.Form):
    ans = forms.CharField(
        label="Enter Your theory Answer answer is not Guaranteed like it obj counterpart ",
        max_length=30,
    )


class TopicsQuizForm(forms.ModelForm):
    class Meta:
        model = topicsquiz
        fields = ["question", "questiontype"]


class objForm(forms.ModelForm):
    class Meta:
        model = topicobj
        fields = ["op1", "op2", "op3", "op4", "answer"]


class topicupdateform(forms.ModelForm):
    class Meta:
        model = topics
        fields = ["name", "description", "content", "video_file"]


# class ansForm(forms.ModelForm):
#    class Meta:
#        model = objanssheet
#        fields = ["answer"]


class UserPreferencesUpdateView(View):
    template_name = (
        "studypal/user_preferences_form.html"  # Update with your actual template path
    )
    success_url = reverse_lazy("studypal-home")  # Update with your desired success URL

    def get(self, request, *args, **kwargs):
        # Get or create the UserPreferences object for the logged-in user
        user_preferences, created = UserPreferences.objects.get_or_create(
            user=request.user
        )
        form = UserPreferencesForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserPreferencesForm()
        font_size = request.POST.get("font_size")
        color_theme = request.POST.get("color_theme")
        brightness = request.POST.get("brightness")
        font_color = request.POST.get("font_color")
        word_spacing = request.POST.get("word_spacing")
        userexist = UserPreferences.objects.filter(user=self.request.user).first()
        if userexist:
            userp = get_object_or_404(UserPreferences, user=self.request.user)
            userp.color_theme = color_theme
            userp.font_size = font_size
            userp.font_color = font_color
            userp.brightness = brightness
            userp.word_spacing = word_spacing
            userp.save()
        else:
            userp = UserPreferences(
                user=self.request.user,
                color_theme=color_theme,
                font_size=font_size,
                brightness=brightness,
                font_color=font_color,
                word_spacing=word_spacing,
            )
        userp.save()

        messages.success(request, "Updated!")
        # Get or create the UserPreferences object for the logged-in user

        return render(request, self.template_name, {"form": form})


class orientationView(TemplateView):
    template_name = "studypal/lecturerorientation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class teacherorientView(TemplateView):
    template_name = "studypal/teacherorien.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = courseenrollment
        fields = ["course", "student"]


# class generatesubtitle(View):
#   def get(self, request, topicid):
#        topic = get_object_or_404(topics, id=topicid)
#        # Get the path to the video file
#        # video_path = topic.video_file.url
#        video_name = topic.video_file.name
#        video_path = os.path.join(settings.MEDIA_ROOT, video_name)
#        print(video_name)
#        complete_path = os.path.join(
#            "C:/Users/ithar/Desktop/finalyearproui/media", video_name
#        )
#        audio_clip = VideoFileClip(video_path).audio
#        audio_clip.write_audiofile(
#            "C:/Users/ithar/Desktop/finalyearproui/media/audio/sub.mp3"
#        )
#        aai.settings.api_key = "7e3a73239ae84d1583fa5625a66cfef5"
#        transcriber = aai.Transcriber()
#        transcript = transcriber.transcribe(
#            "C:/Users/ithar/Desktop/finalyearproui/media/audio/sub.mp3"
#        )
#        subs = transcript.export_subtitles_vtt()
#        # os.remove(audio_output_path)
#        subtittle = get_object_or_404(subtitles, topic=topic, subtitle=subs)
#        if not subtittle:
#            subtitles.objects.create(topic=topic, subtitle=subs)
#        if subtittle:
#            subtittle.subtitle = subs
#            subtittle.save()
#        return redirect("topic-view", pk=topicid)


class enrollmentview(View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, id=course_id)
        student = request.user
        if student.disabilityprofile:
            studentdisability = request.user.disabilityprofile.disabilities
        istudentenrolled = courseenrollment.objects.filter(
            course=course,
            student=student,
        ).first()
        if not istudentenrolled:
            courseenrollment.objects.create(
                course=course,
                student=student,
            )
        return redirect("course-detail", pk=course_id)


class yourclasses(ListView):
    template_name = "studypal/yourteachers.html"
    model = classroom
    context_object_name = "cl"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = classroom.objects.filter(student=self.request.user)
        context["classes"] = classes
        return context


class teacherdetail(View):
    template_name = "studypal/fellowstudent.html"

    def get(self, request, teacherid):
        teachers = get_object_or_404(Teachers, id=teacherid)
        teachername = teachers.teacher.username
        student = request.user
        classr = classroom.objects.filter(
            teacher=teachers,
        )
        context = {"classroom": classr, "teachername": teachername}
        return render(request, self.template_name, context)
        # return redirect("course-detail", pk=course_id)


class cousedashboard(ListView):
    template_name = "studypal/coursedashboard.html"
    model = Courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usercourses = courseenrollment.objects.filter(student=self.request.user)
        context["userc"] = usercourses
        return context


class courseListView(ListView):
    template_name = "studypal/courses.html"
    model = Courses
    context_object_name = "courses"

    # ordering = ["date_posted"]
    def get_context_data(self, *args, **kwargs):
        context = super(courseListView, self).get_context_data(**kwargs)
        # context["disabled"] = disabilityProfile.objects.all()
        context["lecturers"] = Lecturers.objects.all()
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        # context["artlikes"] = artlike.objects.all()
        # context["subform"] = SubscribeForm()
        for i in Courses.objects.all():
            print(i.lecturer.lecturer.username)
        user_in_lecutures = False
        if self.request.user.is_authenticated:
            user_in_lecturers = Lecturers.objects.filter(
                lecturer=self.request.user
            ).exists()
            print(user_in_lecturers)
            context["user_in_lecturers"] = user_in_lecturers
            context["teacherprofile"] = teacherprofile
        return context


class PostListView(ListView):
    template_name = "studypal/home.html"
    model = Courses
    context_object_name = "courses"
    # ordering = ["date_posted"]

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context["disabled"] = disabilityProfile.objects.all()
        context["samaritans"] = samaritanProfile.objects.all()
        context["Teachers"] = Teachers.objects.all()
        # context["artlikes"] = artlike.objects.all()
        # context["subform"] = SubscribeForm()
        user_in_samaritans = False
        user_in_disabled = False
        user_in_lecutures = False
        userinteachers = False

        if self.request.user.is_authenticated:
            user_in_samaritans = samaritanProfile.objects.filter(
                user=self.request.user
            ).exists()
            user_in_disabled = disabilityProfile.objects.filter(
                user=self.request.user
            ).exists()
            user_in_lecturers = Lecturers.objects.filter(
                lecturer=self.request.user
            ).exists()
            userinteachers = Teachers.objects.filter(teacher=self.request.user).exists()
            teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
            lecturerprofile = Lecturers.objects.filter(
                lecturer=self.request.user
            ).first()
            context["lecturerprofile"] = lecturerprofile
            context["user_in_lecturers"] = user_in_lecturers
            context["user_in_samaritans"] = user_in_samaritans
            context["user_in_disabled"] = user_in_disabled
            context["userinteachers"] = userinteachers
            context["teacherprofile"] = teacherprofile
        user = self.request.user
        return context


class createcourse(LoginRequiredMixin, CreateView):
    model = Courses
    fields = ["name", "description"]

    # def form_valid(self, form):
    #  form.instance.user = self.request.user
    # return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    def form_valid(self, form):
        lecturer = Lecturers.objects.get(lecturer=self.request.user)
        form.instance.lecturer = lecturer
        return super().form_valid(form)

    success_url = reverse_lazy("courses")


class createteacher(LoginRequiredMixin, CreateView):
    model = Teachers
    fields = ["handlesize"]

    # def form_valid(self, form):
    #  form.instance.user = self.request.user
    # return super().form_valid(form)
    def form_valid(self, form):
        teacherexist = Teachers.objects.filter(teacher=self.request.user).exists()
        if teacherexist:
            return HttpResponseForbidden("You are already registered as a teacher.")
        if teacherexist == False:
            form.instance.teacher = self.request.user
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class teacherDetailView(DetailView, UserPassesTestMixin):
    model = Teachers
    template_name = "studypal/teacher-profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_instance = self.object
        # Access the associated User instance
        user_instance = teacher_instance.teacher
        # Access the associated SamaritanProfile instance
        samaritan_profile = user_instance.samaritanprofile
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class lecturerDetailView(DetailView, UserPassesTestMixin):
    model = Lecturers
    template_name = "studypal/lecturerprofile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lecturer_instance = self.object
        # Access the associated User instance
        user_instance = lecturer_instance.lecturer
        # Access the associated SamaritanProfile instance
        samaritan_profile = user_instance.samaritanprofile
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class quiz_submitview(View):
    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data["address"]
            # Get the order associated with the logged-in user
            user_order = Order.objects.get(user=self.request.user)

            # Update the address column
            user_order.address = address
            user_order.save()
            ans = "Address:{}"
            success1 = ans.format(address)
            messages.success(request, f"Address Updated")
            response = HttpResponse(success1, content_type="text/plain")
            return response


# class topicreationcontinuation(View):


class createtopic(LoginRequiredMixin, CreateView):
    model = topics
    fields = ["name", "description", "content", "video_file"]

    def dispatch(self, request, *args, **kwargs):
        self.course_id = self.kwargs["course_id"]
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #  form.instance.user = self.request.user
    # return super().form_valid(form)

    def form_valid(self, form):
        course = get_object_or_404(Courses, id=self.course_id)
        form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    # success_url = reverse_lazy("topic-detail")


class createlecturer(LoginRequiredMixin, CreateView):
    model = Lecturers
    fields = ["qualifications", "proofofqualific"]

    # def form_valid(self, form):
    #  form.instance.user = self.request.user
    # return super().form_valid(form)

    def form_valid(self, form):
        lecturerexist = Lecturers.objects.filter(lecturer=self.request.user).exists()
        if lecturerexist:
            return HttpResponseForbidden("You are already registered as a lecturer.")
        if lecturerexist == False:
            form.instance.lecturer = self.request.user
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    success_url = reverse_lazy("courses")


class CourseSelectView(TemplateView):
    template_name = "studypal/courseselection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        courses = Courses.objects.all()
        context["courses"] = courses
        context["teacherprofile"] = teacherprofile
        return context


class pickstudents(View):
    template_name = "studypal/studentselection.html"

    def get(self, request, *args, **kwargs):
        # Retrieve course_id from URL parameters
        course_id = self.kwargs.get("course_id")
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        enrollments = courseenrollment.objects.filter(course__id=course_id)
        classr = classroom.objects.filter(teacher=teacherprofile).first()
        courses = Courses.objects.all()
        classes = classroom.objects.all()
        classsize = classroom.objects.filter(teacher=teacherprofile)
        if len(classsize) < teacherprofile.handlesize:
            accomodate = True
            context = {
                "accomodate": accomodate,
                "classes": classes,
                "classr": classr,
                "enrollments": enrollments,
                "courses": courses,  # Assuming you have a variable named 'courses' available
                "teacherprofile": teacherprofile,
            }
        if len(classsize) >= teacherprofile.handlesize:
            accomodate = False
            context = {
                "accomodate": accomodate,
                "classes": classes,
                "classr": classr,
                "enrollments": enrollments,
                "courses": courses,  # Assuming you have a variable named 'courses' available
                "teacherprofile": teacherprofile,
            }

        return render(request, self.template_name, context)


class addtoclass(View):
    def get(self, request, *args, **kwargs):
        studentid = self.kwargs.get("student_id")
        courseid = self.kwargs.get("course_id")
        course_id = courseid
        course = Courses.objects.filter(id=courseid)
        student = get_object_or_404(User, id=studentid)
        teacher = Teachers.objects.filter(teacher=self.request.user).first()
        enroll = courseenrollment.objects.filter(
            student=studentid, course=courseid
        ).first()
        classsize = classroom.objects.filter(teacher=teacher)
        print(enroll)
        if len(classsize) < teacher.handlesize:
            classroom.objects.create(student=student, teacher=teacher)
            enroll.tutored = True
            enroll.save()
            suc = "Added to class"
            return redirect("pickstudents", course_id=course_id)
        else:
            suc = "The Number of Students you can handle is exceeded"
            return redirect("pickstudents", course_id=course_id)


class yourclassviews(View):
    template_name = "studypal/classrooms.html"

    def get(self, request, *args, **kwargs):
        teacher = Teachers.objects.filter(teacher=self.request.user).first()
        classr = classroom.objects.filter(teacher=teacher)
        context = {"classroom": classr}
        return render(request, self.template_name, context)


class courseDetailView(DetailView, UserPassesTestMixin):
    model = Courses
    template_name = (
        "studypal/coursedetails.html"  # Replace with your actual template name
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_in_lecturers = Lecturers.objects.filter(
            lecturer=self.request.user
        ).exists()
        context["useriscreator"] = Courses.objects.filter(
            lecturer__lecturer=self.request.user
        ).exists()
        user_isenrolled = courseenrollment.objects.filter(
            student=self.request.user, course=self.object
        ).exists()
        context["user_isenrolled"] = user_isenrolled
        context["user_in_lecturers"] = user_in_lecturers
        context["topics"] = topics.objects.filter(course=self.object)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        # context["review_form"] = ArtReviewForm()
        # Include existing reviews for the clothing in the context
        return context


class topicview(DetailView):
    model = topics
    template_name = "studypal/topic.html"  # Replace with your actual template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subs"] = subtitles.objects.filter(topic=self.object)
        context["topicsquiz"] = topicsquiz.objects.filter(topic=self.object)
        context["topicinsub"] = subtitles.objects.filter(topic=self.object).exists()
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context


class quizpageView(View):
    template_name = "studypal/quizpage.html"

    def get(self, request, topicid):
        quizq = topicsquiz.objects.filter(topic__id=topicid)
        opform = ansForm()
        theory = theoryForm()
        objoptions = []
        objans = objanssheet.objects.filter(
            student=request.user,
        )
        for i in quizq:
            if i.questiontype == "objective":
                objoptions.append(
                    topicobj.objects.filter(
                        objquestion=i,
                    )
                )
        # for l in objoptions:
        # for m in l:
        # for j in objans:
        # if m == j:
        # if m.answer==j.answerfilled:

        context = {
            "topicsquiz": quizq,
            "objoptions": objoptions,
            "objans": objans,
            "opform": opform,
            "theoryForm": theory,
        }
        return render(request, self.template_name, context)


class submitobj(View):
    template_name = "studypal/quizpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    def post(self, request, obj_id):
        question = get_object_or_404(topicobj, id=obj_id)
        objans = objanssheet.objects.filter(
            question=question,
            student=request.user,
        ).first()
        questioncheck = topicobj.objects.filter(id=obj_id).first()
        form = ansForm(request.POST)

        if form.is_valid():
            ans = form.cleaned_data["answerfilled"]
            correctans = questioncheck.answer
            if not objans:
                # If the item doesn't exist, create a new cart item
                objans = objanssheet.objects.create(
                    question=question, student=request.user, answerfilled=ans
                )
                messages.success(request, "Objective options added successfully!")
            # Save the form data

        if objans and objans.answerfilled != None:
            objans.answerfilled = ans
            objans.save()
            messages.success(request, "submission Updated!")
            # redirect_url = reverse("quizpage", kwargs={"topicid": question.objquestion.topic.id})
            # redirect_url += f"?correct={correct}"

        # return redirect(redirect_url)

        return redirect("quizpage", topicid=question.objquestion.topic.id)


class submitheory(View):
    def post(self, request, topicid):
        question = get_object_or_404(topicsquiz, id=topicid)
        theoryans = theoryanssheet.objects.filter(
            question=question,
            student=request.user,
        ).first()
        form = theoryForm(request.POST)
        if form.is_valid():
            ans = form.cleaned_data["ans"]
            # correctans = questioncheck.answer
            if not theoryans:
                # If the item doesn't exist, create a new cart item
                theoryans = theoryanssheet.objects.create(
                    question=question, student=request.user, answer=ans
                )
                messages.success(request, " Submitted successfully!")
        if theoryans and theoryans.answer != None:
            theoryans.answer = ans
            theoryans.save()
            messages.success(request, "submission Updated!")

        return redirect("quizpage", topicid=question.topic.id)


class topicdetailview(DetailView, UserPassesTestMixin):
    model = topics
    template_name = (
        "studypal/topicsdetail.html"  # Replace with your actual template name
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topicsquiz"] = topicsquiz.objects.filter(topic=self.object)
        context["alreadyhasquiz"] = topicsquiz.objects.filter(
            topic=self.object
        ).exists()
        context["userislecturer"] = topics.objects.filter(
            course__lecturer__lecturer=self.request.user
        ).exists()
        hasnoobj = []
        topic_in_quiz = False
        context["obj"] = topicobj.objects.all()
        for i in context["topicsquiz"]:
            if i.questiontype == "objective":
                if topicobj.objects.filter(objquestion=i).exists():
                    print(topicobj.objects.filter(objquestion=i).exists())
                    # hasobj.append(i.id)
                else:
                    hasnoobj.append(i.id)

        topic_in_quiz = topicsquiz.objects.filter(topic=self.object).exists()
        print(
            topics.objects.filter(course__lecturer__lecturer=self.request.user).exists()
        )
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        context["topic_in_quiz"] = topic_in_quiz
        context["quiz_form"] = TopicsQuizForm()
        context["topicupdateform"] = topicupdateform()
        context["objform"] = objForm()
        context["hasnobj"] = hasnoobj
        # Include existing reviews for the clothing in the context
        return context


class topicupdate(View):
    form_class = topicupdateform

    def post(self, request, topicid):
        topicid = topicid
        topic = get_object_or_404(topics, id=topicid)
        updateform = self.form_class(request.POST, request.FILES, instance=topic)
        if updateform.is_valid():
            update_instance = updateform.save()
        return redirect("topic-view", pk=topicid)


class TopicsQuizSubmissionView(View):
    # template_name = 'your_template.html'
    form_class = TopicsQuizForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    def post(self, request, test_id):
        topic = topics.objects.get(id=test_id)
        quiz_form = self.form_class(request.POST)

        if quiz_form.is_valid():
            quiz_instance = quiz_form.save(commit=False)
            quiz_instance.topic = topic
            quiz_instance.save()

            messages.success(request, "Quiz submitted successfully!")
            return redirect("topic-detail", pk=test_id)


class objSubmissionView(View):
    # template_name = 'your_template.html'
    form_class = objForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context

    def post(self, request, quiz_id):
        obj = topicsquiz.objects.get(id=quiz_id)
        objform = self.form_class(request.POST)

        if objform.is_valid():
            obj_instance = objform.save(commit=False)
            obj_instance.objquestion = obj
            obj_instance.save()

            messages.success(request, "Objective options added successfully!")
        else:
            # Handle the case where the form is not valid
            messages.error(request, "Form submission failed!")

        # You should return an appropriate HttpResponse or redirect here

        return redirect("topic-detail", pk=obj.topic.id)


# Create your views here.
