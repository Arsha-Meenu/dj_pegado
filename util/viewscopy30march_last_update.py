from django.shortcuts import render
from django.http import HttpResponse
# django river section
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from river.models import State
# token generated section
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


# # token based authentication 
from util.models import StudentBase,CollegeTypeMaster,SchemeMaster
from django.contrib.auth.models import User,Group


# sample function
def sample(request):
    return HttpResponse('django river final')

############################

# token genertaed in user login
 
class loginClass(APIView):
    permission_classes = (AllowAny,)

    def post(self,request,format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error':'Please provide username and password'},status=status.HTTP_400_BAD_REQUEST)
        userData = authenticate(username = username, password= password)
        if not userData :
            return Response({'error':'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)
        token,_ = Token.objects.get_or_create (user = userData) #create token for user
        return Response({'id':userData.id,'username':userData.username,'token':token.key},status=status.HTTP_200_OK)

########################

# river action 
def approve_ticket(request, ticket_id, next_state_id=None):
    data = get_object_or_404(StudentBase, pk=ticket_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        data.river.status.approve(as_user=request.user, next_state=next_state)
        return redirect(reverse('admin:util_studentbase_changelist')) # (admin:appname_modelusedhere_changelist')
    except Exception as e:
        return HttpResponse(e.message)

################################

# token based authentication for getting the teacher get the all students data.

class GetUserAllData(APIView):
    permission_classes = (IsAuthenticated,)     

    def get(self,request,format = None):
        print(request.user) # showsthe user whose token is given.
        user = request.user.groups.all()
        print(user)
        if user.filter(name='Teacher').exists():
            data = StudentBase.objects.values('user').order_by('name')# "objects.values()" :give the specified values from the model
            print(data.values('name'))
            return HttpResponse(data.values())
        else:
            return HttpResponse("access denied")

    

######################## #########################



class TeacherStatusPermission(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format = None):
        print(request.user) # showsthe user whose token is given.
        print('123')
        user = request.user.groups.all()
        print(user)
        if user.filter(name='Teacher').exists():
            my_model_objects = StudentBase.river.status.get_on_approval_objects(as_user=request.user)# can find out what is the current status of action pf this user ()
            print(my_model_objects.values())
            print(request.user)
            print('456')
            if my_model_objects.exists():
                print(my_model_objects.values('name','user_id'))
                return HttpResponse(my_model_objects.values('name','user_id'))
            else:
                return HttpResponse('Permission completed.')
      
        else:
            return HttpResponse("Access Denied..")

#########################
from django.shortcuts import get_object_or_404, redirect

class TeacherApproval(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,fromat = None):
        user =  request.user.groups.all()
        print(user)
        print('123')
        data = request.user
        print(data)
        
        if user.filter(name='Teacher').exists():
            transition_approvals = StudentBase.river.status.get_available_approvals(
                            as_user= data,
                            # source_state=State.objects.get(label='Applied'),
                            # destination_state=State.objects.get(label='Verified'),
                    )
            # print(transition_approval)
        # a= StudentBase.river.status.values('id','label')
        # print(a)
            return HttpResponse('success')
        else:
            return HttpResponse('failed')

    def post(self,request,format = None):
        # return HttpResponse('hoi')
        # next_state = get_object_or_404(State, pk=next_state_id)
        # transition_approvals == StudentBase.river.status.next_approvals
        # transition_approval.transition.destination_state
        # my_model_objects = StudentBase.river.status.get_on_approval_objects(as_user=request.user)# can find out what is the current status of action pf this user (T_1)

        # print(my_model_objects.values())
        # print(my_model_objects.transition.destination_state)
        print(request.user)
        # a= StudentBase.river.status.approve(as_user=request.user, next_state=my_model_objects.transition.destination_state)
        return HttpResponse('hai')
#########################
