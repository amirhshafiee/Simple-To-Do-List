from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, ShowTaskSerializer
from rest_framework.response import Response
from rest_framework import status
from Accounts.models import CustomUser


class ShowTasksView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = CustomUser.objects.filter(email= request.user.email).first()
        tasks = Task.objects.filter(author= user)
        ser_data = ShowTaskSerializer(instance=tasks, many=True)
        return Response(data= ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = CustomUser.objects.filter(email=request.user.email).first()
        ser_data = TaskSerializer(data= request.data)

        if ser_data.is_valid():
            ser_data.validated_data['user'] = user
            task = ser_data.create(ser_data.validated_data)

            return Response(data= {
                'Message': f'{task.title} Created .',
                'All Task': '/home/',
            }, status=status.HTTP_201_CREATED)
        return Response(data= ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowTaskView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        user = CustomUser.objects.filter(email=request.user.email).first()
        task = Task.objects.filter(author=user, pk= pk).first()
        if task:
            ser_data = ShowTaskSerializer(instance=task)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data={
            'Message': 'Task-id not valid !'
        }, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        user = CustomUser.objects.filter(email=request.user.email).first()
        task = Task.objects.filter(author=user, pk=pk).first()
        if task:
            ser_data = ShowTaskSerializer(data=request.data, instance=task, partial=True)

            if ser_data.is_valid():
                ser_data.save()

                return Response(data={
                    'Message': f'{task.title} Updated .',
                    'All Task': '/home/',
                }, status=status.HTTP_200_OK)
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            'Message': 'Task-id not valid !'
        }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        user = CustomUser.objects.filter(email=request.user.email).first()
        task = Task.objects.filter(author=user, pk=pk).first()
        if task:
            title = task.title
            task.delete()
            return Response(data={
                'Message': f'Task {title} Deleted .',
                'All Task': '/home/',
            }, status=status.HTTP_200_OK)
        return Response(data= {
            'Message': 'Task-id not valid !'
        }, status=status.HTTP_400_BAD_REQUEST)
