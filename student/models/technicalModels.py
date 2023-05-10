from django.db import models

from student.models.studentModels import Student


class TechnicalProfile(models.Model):

    student_id = models.OneToOneField(
        Student, null=True, on_delete=models.CASCADE)
    git_username = models.CharField(max_length=50)

    total_commits = models.IntegerField(default=0)
    total_prs = models.IntegerField(default=0)
    total_stars = models.IntegerField(default=0)
    total_issues = models.IntegerField(default=0)
    total_contribs = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)

    c = models.FloatField(default=0.0)
    cmake = models.FloatField(default=0.0)
    cPlusPlus = models.FloatField(default=0.0)
    java = models.FloatField(default=0.0)
    javascript = models.FloatField(default=0.0)
    python = models.FloatField(default=0.0)
    r = models.FloatField(default=0.0)
    jupyter = models.FloatField(default=0.0)
    dart = models.FloatField(default=0.0)
    kotlin = models.FloatField(default=0.0)
    go = models.FloatField(default=0.0)
    swift = models.FloatField(default=0.0)
    cSharp = models.FloatField(default=0.0)
    aspNet = models.FloatField(default=0.0)
    typescript = models.FloatField(default=0.0)
    php = models.FloatField(default=0.0)
    objective_c = models.FloatField(default=0.0)
    ruby = models.FloatField(default=0.0)
    html = models.FloatField(default=0.0)
    css = models.FloatField(default=0.0)
    scss = models.FloatField(default=0.0)
    sql = models.FloatField(default=0.0)
    rust = models.FloatField(default=0.0)

    def __str__(self):
        return self.git_username

    @property
    def gitName(self):
        return self.git_username

    @property
    def cLang(self):
        return self.c

    @property
    def cmakeLang(self):
        return self.cmake

    @property
    def javaLang(self):
        return self.java

    @property
    def cPlusPlusLang(self):
        return self.cPlusPlus

    @property
    def jsLang(self):
        return self.javascript

    @property
    def pythonLang(self):
        return self.python

    @property
    def rLang(self):
        return self.r

    @property
    def jupyterLang(self):
        return self.jupyter

    @property
    def dartLang(self):
        return self.dart

    @property
    def kotlinLang(self):
        return self.kotlin

    @property
    def goLang(self):
        return self.go

    @property
    def swiftLang(self):
        return self.swift

    @property
    def cSharpLang(self):
        return self.cSharp

    @property
    def aspNetLang(self):
        return self.aspNet

    @property
    def tsLang(self):
        return self.typescript

    @property
    def phpLang(self):
        return self.php

    @property
    def objCLang(self):
        return self.objective_c

    @property
    def rubyLang(self):
        return self.ruby

    @property
    def htmlLang(self):
        return self.html

    @property
    def cssLang(self):
        return self.css

    @property
    def scssLang(self):
        return self.scss

    @property
    def sqlLang(self):
        return self.sql

    @property
    def rustLang(self):
        return self.rust
