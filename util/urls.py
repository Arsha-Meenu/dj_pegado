from django.urls import path,include
from util import views
from django.conf.urls import url

urlpatterns = [
    path('',views.sample,name = 'sample'),

    # river action
    path('^approve_ticket/(?P<ticket_id>\d+)/(?P<next_state_id>\d+)/', views.approve_ticket, name='approve_ticket'),
    # path('', include("river_admin.urls")),
    url(r'^', include("river_admin.urls")),

 
    # token generated user
    path('login/',views.loginClass.as_view(),name="login_Api"),
    # user get all students details
    path('studentsdata/',views.GetUserAllData.as_view(),name = "get_all_students_data"),
    path('usermodeldetails/',views.UserModelDetails.as_view(),name= "user_has_permission"),
    path('availableTransitionApprovals/',views.availableTransitionApprovals.as_view(),name = "availableTransitionApprovals"),
    path('approveinstanceapi/<int:pk>/',views.ApproveInstanceApi.as_view(),name = "ApproveInstanceApi"),
    # serializer
    path('viewset/',views.ViewsetView.as_view({'get':'list'})),
    
 
]