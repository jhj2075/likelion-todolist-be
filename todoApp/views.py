from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from .models import Todo, User
from .serializers import TodoSerializer, TodoDetailSerializer, TodoCheckSerializer, TodoReviewsSerializer
# Create your views here.

class Todos(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get(self, request, user_id):
        now = timezone.localtime(timezone.now())
        current_month = now.month
        current_day = now.day
        
        month = request.query_params.get("month", current_month)
        month = int(month)

        day = request.query_params.get("day", current_day)
        day = int(day)
        
        user = self.get_user(user_id)
        todos = Todo.objects.filter(
            date__month=month,
            date__day=day,
            user=user
        )
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request, user_id):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_user(user_id)
            serializer.save(
                user=user
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class TodoDetailView(APIView):
    def get_todo(self, user_id, todo_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        
        try:
            return user.todos.get(id=todo_id)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")
        
    def get(self, request, user_id, todo_id):
        todo = self.get_todo(user_id, todo_id)

        serializer = TodoSerializer(todo)
        return Response(serializer.data)
            
    def patch(self, request, user_id, todo_id):
        todo = self.get_todo(user_id, todo_id)
        user = User.objects.get(id=user_id)

        serializer = TodoSerializer(todo)
        detailserializer = TodoDetailSerializer(todo, data=request.data, partial=True)
        if detailserializer.is_valid():
            detailserializer.save(
                user=user
            )
            return Response(serializer.data)
        else:
            raise ParseError
    
    def delete(self, request, user_id, todo_id):
        todo = self.get_todo(user_id, todo_id)

        todo.delete()
        return Response({"detail": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
    
class TodoCheckView(APIView):
    def get_todo(self, user_id, todo_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        
        try:
            return user.todos.get(id=todo_id)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")
    
    def patch(self, request, user_id, todo_id):
        todo = self.get_todo(user_id, todo_id)
        user = User.objects.get(id=user_id)

        serializer = TodoSerializer(todo)
        checkserializer = TodoCheckSerializer(todo, data=request.data, partial=True)
        if checkserializer.is_valid():
            checkserializer.save(
                user=user
            )
            return Response(serializer.data)
        else:
            raise ParseError

class TodoReviewsView(APIView):
    def get_todo(self, user_id, todo_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        
        try:
            return user.todos.get(id=todo_id)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")
    
    def patch(self, request, user_id, todo_id):
        todo = self.get_todo(user_id, todo_id)
        user = User.objects.get(id=user_id)

        serializer = TodoSerializer(todo)
        reviewsserializer = TodoReviewsSerializer(todo, data=request.data, partial=True)
        if reviewsserializer.is_valid():
            reviewsserializer.save(
                user=user
            )
            return Response(serializer.data)
        else:
            raise ParseError
        
class TodoSortView(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get(self, request, user_id):
        now = timezone.localtime(timezone.now())
        current_month = now.month
        current_day = now.day
        
        month = request.query_params.get("month", current_month)
        month = int(month)

        day = request.query_params.get("day", current_day)
        day = int(day)
        
        user = self.get_user(user_id)
        todos = Todo.objects.filter(
            date__month=month,
            date__day=day,
            user=user
        ).order_by('content')
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
class TodoSearchView(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get(self, request, user_id):
        now = timezone.localtime(timezone.now())
        current_month = now.month
        
        month = request.query_params.get("month", current_month)
        month = int(month)
        
        user = self.get_user(user_id)
        todos = Todo.objects.filter(
            date__month=month,
            user=user
        )
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)