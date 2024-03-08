from django.urls import path
from base.views import *
from evidence.views import *

urlpatterns = [
    path('activities', ActivityList.as_view(), name='list-activity'),
    path('activity', ActivityCreate.as_view(), name='create-activity'),
    path('activity/<uuid:pk>', ActivityDetail.as_view(), name='detail-activity'),

    path('subActivities', SubActivityList.as_view(), name='list-subActivity'),
    path('subActivity', SubActivityCreate.as_view(), name='create-subActivity'),
    path('subActivity/<uuid:pk>', SubActivityDetail.as_view(), name='detail-subactivity'),

    path('tasks', TaskList.as_view(), name='list-task'),
    path('task', TaskCreate.as_view(), name='create-task'),
    path('task/<uuid:pk>', TaskDetail.as_view(), name='detail-task'),
    path('taskuser', UserTasks.as_view(), name='list-taskuser'),
    path('taskuserstaff', UserStaffTasks.as_view(), name='list-taskuserstaff'),

    path('evidence', EvidenceList.as_view(), name='create-evidence'),
    path('file', FileCreate.as_view(), name='create-file'),

]