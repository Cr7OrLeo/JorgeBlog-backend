import random
from urllib import request
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import LoginSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    # Pass the request to the serializer context so build_absolute_uri works
    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        print("FILES:", request.FILES)  # should show your uploaded file
        print("DATA:", request.data)     # form data
        return super().create(request, *args, **kwargs)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        code = str(random.randint(100000, 999999))

        user.profile.verification_code = code
        user.profile.save()

        send_mail(
            subject="Your Verification Code",
            message=f"Hello {username},\n\nYour verification code is: {code}\n\nThanks for signing up!",
            from_email="contact.jorgeblog@gmail.com",  # Replace with your Gmail
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "User registered successfully. Please check your email for the verification code."})

@api_view(['POST'])
def verify_email(request):
    username = request.data.get("username")
    code = request.data.get("code")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.profile.verification_code == code:
        user.profile.is_verified = True
        user.profile.verification_code = ""
        user.profile.save()
        return Response({"message": "Email verified successfully"})
    else:
        return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)







@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_login(request):
    return Response({"username": request.user.username})