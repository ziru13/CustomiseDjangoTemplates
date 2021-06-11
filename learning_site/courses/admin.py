from django.contrib import admin

# Register your models here.
# from .models import Course, Step
# from .models import Course, Text, Quiz
# 
# 
# # class StepInline(admin.StackedInline):
# #     model = Step
# 
# class TextInline(admin.StackedInline):
#     model = Text
# 
# 
# class CourseAdmin(admin.ModelAdmin):
#    # inlines = [StepInline,]
#     inlines = [TextInline,]
# 
# 
# admin.site.register(Course, CourseAdmin)
# # admin.site.register(Step)
# admin.site.register(Text)
# admin.site.register(Quiz)

# ----------------------------------------------------------------------------------
from . import models

# 2.5 我们不会再用这个
# class TextInline(admin.StackedInline):
#     model = Text

# 因此这个也不要了
# class CourseAdmin(admin.ModelAdmin):
#     inlines = [TextInline,]


admin.site.register(models.Course)
admin.site.register(models.Text)
admin.site.register(models.Quiz)
# admin.site.register(models.Question)
admin.site.register(models.MultipleChoiceQuestion)
admin.site.register(models.TrueFalseQuestion)
admin.site.register(models.Answer)
