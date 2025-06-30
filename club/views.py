from django.shortcuts import render
from .models import User, Task ,Event
from .serializers import UserSerializer, TaskSerializer, EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .permissions import IsAdmin, IsBoardMember, IsSimpleMember, IsFinanceLeader, IsMarketingLeader, IsTechnicalTeamLeader, IsVisualCreationLeader, IsERLeader, IsSelfOrBoard
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsBoardMember])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsSelfOrBoard])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdmin])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list(request):
    user = request.user

    if user.is_admin:
        tasks = Task.objects.all()
    elif user.is_board:
        tasks = Task.objects.filter(department=user.department)
    else:
        tasks = Task.objects.filter(assigned_to=user)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)

    user = request.user

    # Permission logic
    if not (
        task.assigned_to == user
        or user.is_admin
        or (user.is_board and user.department == task.department)
    ):
        return Response({'error': 'You do not have permission to view this task.'}, status=403)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsBoardMember])
def create_task(request):
    data = request.data.copy()
    data['department'] = request.user.department

    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        task = serializer.save(created_by=request.user)
        return Response(TaskSerializer(task).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsBoardMember])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check department match
    if request.user.department != task.department and not request.user.is_admin:
        return Response({'error': 'You do not have permission to update this task.'}, status=403)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        task = serializer.save()
        return Response(TaskSerializer(task).data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsBoardMember])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check department match
    if request.user.department != task.department and not request.user.is_admin:
        return Response({'error': 'You do not have permission to delete this task.'}, status=403)

    task.delete()
    return Response(status=204)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_events(request):
    user = request.user

    if user.is_admin:
        events = Event.objects.all()
    elif user.is_board:
        events = Event.objects.filter(department=user.department)
    else:
        events = Event.objects.filter(participants=user)

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

# 🟢 Create Event
@api_view(['POST'])
@permission_classes([IsBoardMember])
def create_event(request):
    user = request.user

    if not user.is_board and not user.is_admin:
        return Response({'detail': 'Permission denied'}, status=403)

    data = request.data.copy()
    data['created_by'] = user.id
    data['department'] = user.department

    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🟢 Retrieve Single Event
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user.is_admin :
        pass
    elif user.is_board and event.department == user.department:
        pass
    elif user in event.participants.all():
        pass
    else:
        return Response({'detail': 'Access denied'}, status=403)

    serializer = EventSerializer(event)
    return Response(serializer.data)

# 🟡 Update Event
@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if not (user.is_admin or (user.is_board and event.department == user.department)):
        return Response({'detail': 'Permission denied'}, status=403)

    serializer = EventSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔴 Delete Event
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if not (user.is_admin or (user.is_board and event.department == user.department)):
        return Response({'detail': 'Permission denied'}, status=403)

    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)