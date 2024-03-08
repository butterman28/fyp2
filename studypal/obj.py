class modules(models.Model):
    topic = models.ForeignKey(courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=False, null=False)
    video_file = models.FileField(upload_to="videos")


class modulequiz(models.Model):
    module = models.ForeignKey(modules, on_delete=models.CASCADE)
    question = models.CharField(max_length=5000, blank=False, null=False)
    questiontype = models.CharField(
        max_length=5000, choices=questiontype, blank=False, null=False
    )


class moduleobj(models.Model):
    mquiz = models.ForeignKey(modulequiz, on_delete=models.CASCADE)
    op1 = models.CharField(max_length=5000, blank=False, null=False)
    op2 = models.CharField(max_length=5000, blank=False, null=False)
    op3 = models.CharField(max_length=5000, blank=False, null=False)
    op4 = models.CharField(max_length=5000, blank=False, null=False)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


class objmoduleanswersheet(models.Model):
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(moduleobj, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


class modtheoryansheet(models.Model):
    mquiz = models.ForeignKey(modulequiz, on_delete=models.CASCADE)
    an


class topicstest(models.Model):
    topic = models.ForeignKey(topics, on_delete=models.CASCADE)
    question = models.CharField(max_length=5000, blank=False, null=False)
    questiontype = models.CharField(
        max_length=5000, choices=questiontype, blank=False, null=False
    )


class topicobj(models.Model):
    topict = models.ForeignKey(topicstest, on_delete=models.CASCADE)
    op1 = models.CharField(max_length=5000, blank=True, null=True)
    op2 = models.CharField(max_length=5000, blank=True, null=True)
    op3 = models.CharField(max_length=5000, blank=True, null=True)
    op4 = models.CharField(max_length=5000, blank=True, null=True)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


class objtestanswersheet:
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    objquestion = models.ForeignKey(topicobj, on_delete=models.CASCADE)
    theory = models.CharField(max_length=5000, blank=True, null=True)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


class courseexam(models.Model):
    course = models.ForeignKey(courses, on_delete=models.CASCADE)
    question = models.CharField(max_length=5000, blank=False, null=False)
    questiontype = models.CharField(
        max_length=5000, choices=questiontype, blank=False, null=False
    )


class examobj(models.Model):
    cexam = models.ForeignKey(courseexam, on_delete=models.CASCADE)
    op1 = models.CharField(max_length=5000, blank=True, null=True)
    op2 = models.CharField(max_length=5000, blank=True, null=True)
    op3 = models.CharField(max_length=5000, blank=True, null=True)
    op4 = models.CharField(max_length=5000, blank=True, null=True)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


if len(classr) == 0:
    firstteacher = teachers.first()
    classroom.objects.create(student=student, teacher=firstteacher)
if len(classr) == 1:
    if not istudenteninclass:
        for i in teachers:
            for j in classr:
                if i.handlesize < j.size and i == j.teacher:
                    for m in j:
                        sd = m.student.disabilityprofile.disabilities
                        for k in sd:
                            for l in studentdisability:
                                if k != l:
                                    theclass.append(n)
                
else:
    for m in classtojoin:
        for n in m:
            sd = n.student.disabilityprofile.disabilities
            for k in sd:
                for l in studentdisability:
                    if k != l:
                        theclass.append(n)


class objexamanswersheet:
    studentid = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(examobj, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5000, choices=optype, blank=False, null=False)


class enrollmentview(CreateView):
    model = courseenrollment

    form_class = EnrollmentForm

    def dispatch(self, request, *args, **kwargs):
        self.course_id = self.kwargs["course_id"]
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, form):
    #  form.instance.user = self.request.user
    # return super().form_valid(form)

    def form_valid(self, form):
        course = get_object_or_404(Courses, id=self.course_id)
        form.instance.course = course
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["another_form"] = AnotherForm()
        teacherprofile = Teachers.objects.filter(teacher=self.request.user).first()
        context["teacherprofile"] = teacherprofile
        return context
