from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from users.models import Account
from .serializers import Register,ProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

def user(request):
    route=[{
        'register/':'register user',
        'forgotPassword/':'reset password',
        'addUser/':'To add users in various groups by super-admin',
        'addStudent/':'To add user in student group by user in teacher group',
        'getDetails/':'To get details of a user',
    },]

    return JsonResponse(route,safe=False)
@api_view(['POST'])
def users(request):
    if request.method=='POST':
        serializer=Register(data=request.data)
        data={}
        if serializer.is_valid():
            user=serializer.save()
            data['response']="Successfully registered a  new user."
            data['email']=user.email
            data['username']=user.username
        else:
            data=serializer.errors
        return Response(data)
    
@api_view(['GET'])
def forgot_password(request):
    userr=User.objects.all()
    serializer=ProfileSerializer(userr,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addUser(request):
    data=request.data
    current_user=request.user
    admin=Group.objects.get(name='Super-admin')
    auth=list(Group.objects.filter(user=current_user))
    if admin in auth:
        userr=User.objects.get(username=data['username'])
        grouped=list(Group.objects.filter(user=userr))
    #print(Student in grouped)
        if userr and (admin not in grouped):
            addGroup=Group.objects.get(name=data['group'])
            userr.groups.add(addGroup)
            userr.save()
            message={'message':'Group added successfully'}
            return Response(message)
        elif admin in grouped:
            message={'message':"You can't this user group"}
            return Response(message)
        else:
            message={'message':"user doesn't exists"}
            return Response(message)
    else:
        message={'message':"You are not authorized"}
        return Response(message)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addStudent(request):
    data=request.data
    current_user=request.user
    admin=Group.objects.get(name='Teacher')
    auth=list(Group.objects.filter(user=current_user))
    if admin in auth:
        userr=User.objects.get(username=data['username'])

        grouped=list(Group.objects.filter(user=userr))
        if userr and len(grouped)==0:
            addGroup=Group.objects.get(name='Student')
            userr.groups.add(addGroup)
            userr.save()
            message={'message':'Group added successfully'}
            return Response(message)
        elif len(grouped)>0:
            message={'message':"You can't user to this group"}
            return Response(message)
        else:
            message={'message':"user doesn't exists"}
            return Response(message)
    else:
        message={'message':"You are not authorized"}
        return Response(message)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDetails(request):
    data=request.data
    current_user=request.user
    admin=Group.objects.get(name='Student')
    auth=list(Group.objects.filter(user=current_user))
    if admin in auth:
        userr=User.objects.get(id=current_user.id)
        if userr:
            serializer=ProfileSerializer(userr,many=False)
            return Response(serializer.data)
        else:
            message={'message':"user doesn't exists"}
            return Response(message)
    else:
        message={'message':"You are not authorized"}
        return Response(message)
    



