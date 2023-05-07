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
    typescript = models.FloatField(default=0.0)
    php = models.FloatField(default=0.0)
    objective_c = models.FloatField(default=0.0)
    ruby = models.FloatField(default=0.0)
    html = models.FloatField(default=0.0)
    css = models.FloatField(default=0.0)
    sql = models.FloatField(default=0.0)
    rust = models.FloatField(default=0.0)

    def __str__(self):
        return self.git_username
    
    @property
    def gitName(self):
        return self.git_username
    
    @property
    def c(self):
        return self.c
    
    @property
    def cPlusPlus(self):
        return self.cPlusPlus
    
    @property
    def javascript(self):
        return self.javascript
    
    @property
    def python(self):
        return self.python
    
    @property
    def r(self):
        return self.r
    
    @property
    def jupyter(self):
        return self.jupyter
    
    @property
    def dart(self):
        return self.dart
    
    @property
    def kotlin(self):
        return self.kotlin
    
    @property
    def go(self):
        return self.go
    
    @property
    def swift(self):
        return self.swift
    
    @property
    def cSharp(self):
        return self.cSharp
    
    @property
    def typescript(self):
        return self.typescript
    
    @property
    def php(self):
        return self.php
    
    @property
    def cPlusPlus(self):
        return self.cPlusPlus
    
    @property
    def objective_c(self):
        return self.objective_c
    
    @property
    def ruby(self):
        return self.ruby
    
    @property
    def html(self):
        return self.html
    
    @property
    def css(self):
        return self.css
    
    @property
    def sql(self):
        return self.sql
    
    @property
    def rust(self):
        return self.rust
    