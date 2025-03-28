from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from app_models.models import Review
from app_models.serializer import ReviewSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.




class UserView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)



class ReviewList(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request):
        permission_classes = [IsAuthenticated]
        request.data['user'] = request.user
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)


class ReviewDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
