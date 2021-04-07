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
from rest_framework import status,viewsets


# # token based authentication 
from util.models import StudentBase,CollegeTypeMaster,SchemeMaster
from django.contrib.auth.models import User,Group

## serializer
from .serializers import TransitionApprovalSerializer


# sample function
def sample(request):
    return HttpResponse('django river final')

################       ##########################

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

######################## #########################

# river action 
def approve_ticket(request, ticket_id, next_state_id=None):
    data = get_object_or_404(StudentBase, pk=ticket_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        data.river.status.approve(as_user=request.user, next_state=next_state)
        return redirect(reverse('admin:util_studentbase_changelist')) # (admin:appname_modelusedhere_changelist')
    except Exception as e:
        return HttpResponse(e.message)

######################### ###################

# token based authentication for the teacher get  all students data.

class GetUserAllData(APIView):
    permission_classes = (IsAuthenticated,)     

    def get(self,request,format = None):
        print(request.user) # showsthe user whose token is given.
        user = request.user.groups.all()
        print(user)
        if user.filter(name='Teacher').exists():
            data = StudentBase.objects.values('user').order_by('name')# "objects.values()" :give the specified values from the model
            print(data.values('name'))
            return Response(data.values())
        else:
            return Response("access denied")

    

######################## #########################


# get_on_approval_objects :output as list of available my model objects
class UserModelDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format = None):
        print(request.user) # showsthe user whose token is given.
        print('step 1')
        user = request.user.groups.all()
        print(user)
        if user.exists():
# here,the output is the model details of the requested user (where ,currently the user have the permission to change the status)
            my_model_objects = StudentBase.river.statusclass_workflow.get_on_approval_objects(as_user=request.user)# can find out what is the current status of action pf this user ()
            print(my_model_objects.values())
            print(request.user)
            print('step 2')
            if my_model_objects.exists():
                print(my_model_objects.values('name','user_id'))
                return Response(my_model_objects.values('name','user_id'))
            else:
                return Response('Permission completed.')
      
        else:
            return Response("Access Denied..")

##########################    #############################

# get_available_approvals : list of available transition approvals
#here,the output is the  details of transition approvals of  the requested user (where ,currently the user have the permission to change the status)
class availableTransitionApprovals(APIView):
    permission_classes = (IsAuthenticated,)
    # queryset = StudentBase.objects.all()
    # serializer_class = TransitionApprovalSerializer


    def get(self,request,format = None):
        user =  request.user.groups.all()
        print(user)
        print('123')
        data = request.user
        print(data) 
        my_model_objects = StudentBase.river.status.get_available_approvals(as_user=request.user)# can find out what is the current status of action pf this user ()
        destination_state =my_model_objects[0].transition.destination_state
        source_state=my_model_objects[0].transition.source_state
        # workflow = my_model_objects[0].workflow.field_name
        # print(workflow)
        print(source_state)
        
        print(my_model_objects.values('id','groups'))
        print(destination_state)
        # return HttpResponse(serializer_class)
        return Response(my_model_objects.values() )# shows current source and destination state of the studentbase of the requested user 
        


            
            # transition_approvals = StudentBase.river.status.get_available_approvals(
            #                 as_user= data
            #                 # source_state=State.objects.get(label='Applied'),
            #                 # destination_state=State.objects.get(label='Verified'),
            #         )
            # # print(transition_approvals)
            # if(transition_approvals.count()==1):
            #     destination_state=transition_approvals[0].destination_state_id
            #     source_state=transition_approvals[0].source_state_id
            #     print("ok")
            #     destination_state=transition_approvals[0].transition.destination_state
            #     print("nokay")
            #     source_state=transition_approvals[0].transition.source_state
            #     # return source_state,destination_state
            #     return HttpResponse('success')
            # else:
            #     return HttpResponse('haiii')


            # a= StudentBase.river.status.values('id','label')
            # print(a)
            # return HttpResponse('success')
        # else:
        #     return HttpResponse('failed')

###############
class ApproveInstanceApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,format = None):
        # return HttpResponse('hoi')
        # next_state = get_object_or_404(State, pk=next_state_id)
        # transition_approvals == StudentBase.river.staclass_workflowtus.next_approvals
        # transition_approval.transition.destination_state
        # my_model_objects = StudentBase.river.status.get_on_approval_objects(as_user=request.user)# can find out what is the current status of action pf this user (T_1)

        # print(my_model_objects.values())
        # print(my_model_objects.transition.destination_state)
        print(request.user)
        # next_state = State.objects.get(id =2)
        # a== StudentBase.river.status.approve(as_user=request.user, next_state= next_state)
        # destination_state_id=self.flow_type.start_stage.id		
		# self.river.stage.approve(as_user=user, next_state=destination_state_id, god_mod=True)
        # return HttpResponse(next_state[2])
        # a= StudentBase.river.status.approve(as_user=request.user, next_state=my_model_objects.transition.destination_state)
        # return HttpResponse(a)
        transition_approval = StudentBase.river.status.get_available_approvals(as_user=request.user)
        # print(transition_approval.values())
        next_state = State.objects.get(transition_as_destination= 3)
        print(next_state)
        a= StudentBase.river.status.approve(as_user=request.user, next_state=State.objects.get(transition_as_destination= 1))

        return HttpResponse("haii")
        

        # destination_state_id=self.flow_type.start_stage.id		
		# StudentBase.river.status.approve(as_user=request.user, next_state=destination_state_id, god_mod=True)
        


        # my_model_objects = StudentBase.river.status.get_available_approvals(as_user=request.user)# can find out what is the current status of action pf this user (T_1)
        # print(request.user)
        # a= StudentBase.river.status.approve(as_user=request.user, next_state=my_model_objects.transition.destination_state)
        # return HttpResponse('hai')
#########################

###### serializers #########
class ViewsetView(viewsets.ModelViewSet):
    queryset = StudentBase.objects.all()
    serializer_class = TransitionApprovalSerializer
    

# def Views(request):
#     queryset = StudentBase.objects.values()
#     # serializer_class = TransitionApprovalSerializer
#     return HttpResponse(queryset)
