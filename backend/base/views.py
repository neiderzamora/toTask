#Files
from base.serializers import ActivitySerializer, SubActivitySerializer, TaskSerializer
from base.models import Activities
from subActivities.models import SubActivities
from tasks.models import Task

# Rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from users.permissions import IsManager, IsStaff, IsSupervisor

""" API Activities """

class ActivityList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Activities.objects.all().order_by('name')
        serializer = ActivitySerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

class ActivityCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Activities.objects.get(pk=pk)
        except Activities.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        if activity is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        activity = self.get_object(pk)
        if activity is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        if activity is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

""" API SubActivities """

class SubActivityList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = SubActivities.objects.all().order_by('name')
        serializer = SubActivitySerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

class SubActivityCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SubActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubActivityDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return SubActivities.objects.get(pk=pk)
        except SubActivities.DoesNotExist:
            return None
    
    def get(self, request, pk, format=None):
        subactivities = self.get_object(pk)
        if subactivities is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubActivities(subactivity)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        subactivities = self.get_object(pk)
        if subactivities is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SubActivitySerializer(subactivities, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk, format=None):
        subactivities = self.get_object(pk)
        if subactivities is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subactivities.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" API Task """

class TaskList(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        queryset = Task.objects.all().order_by('name')
        serializer = TaskSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

class TaskCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserTasks(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, format=None):
        user = request.user
        tasks = Task.objects.filter(user=user).order_by('date_created')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserStaffTasks(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request, format=None):
        user_staff = request.user
        tasks = Task.objects.filter(user_staff=user_staff).order_by('date_created')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)