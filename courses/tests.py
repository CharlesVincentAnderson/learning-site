# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step

# Create your tests here.
class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title = "Python Regex's",
            description = "Learn to write regular expressions in Python"
        )

        now = timezone.now()
        self.assertLess(course.created_at, now)

class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python testing",
            description="Learn to write tests in Python"
        )
        print ("self.course = " + str(self.course))
        self.course2 = Course.objects.create(
            title="New course",
            description="A new course"
        )
        print ("self.course2 = " + str(self.course2))
        self.step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail', kwargs={'pk':self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
    
    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step', kwargs={'course_pk':self.course.pk, 'step_pk': self.step.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
