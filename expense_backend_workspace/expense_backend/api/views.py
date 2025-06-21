from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Expense, Category
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ExpenseSerializer,
    CategorySerializer,
)
from datetime import datetime


# PUBLIC_INTERFACE
@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@api_view(['POST'])
def register(request):
    """
    User registration endpoint.

    Body: {username, password, email (optional)}
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(['POST'])
def login_view(request):
    """
    User authentication endpoint.

    Body: {username, password}
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logs out the authenticated user."""
    logout(request)
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)


# PUBLIC_INTERFACE
class ExpenseViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for expenses.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# PUBLIC_INTERFACE
class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for expense categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# PUBLIC_INTERFACE
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monthly_statistics(request):
    """
    Returns monthly statistics for expenses (grouped by category).
    Query params: year, month
    """
    year = int(request.query_params.get('year', datetime.now().year))
    month = int(request.query_params.get('month', datetime.now().month))

    expenses = Expense.objects.filter(
        user=request.user, date__year=year, date__month=month
    )
    stats = {}
    for expense in expenses:
        cat = expense.category.name if expense.category else "Uncategorized"
        stats.setdefault(cat, 0)
        stats[cat] += float(expense.amount)
    total = sum(stats.values())

    return Response({
        "month": month,
        "year": year,
        "total": total,
        "by_category": stats,
    })
