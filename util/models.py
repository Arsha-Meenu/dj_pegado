from django.db import models

from base_util.models import Base
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentBase(Base): #Student Base(60)
    name = models.CharField(max_length = 100,null = True)
 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pin_number = models.CharField(max_length=20)
    fee_concession_status = models.BooleanField()


  
class CollegeTypeMaster(Base): #College Type Master(41)
    college_title = models.CharField(max_length=20)
    college_type_code = models.CharField(max_length=20)


class SchemeMaster(Base): #Scheme_master(10)

    scheme_name = models.CharField(max_length=20)
    scheme_title = models.CharField(max_length=20)
    scheme_description = models.CharField(max_length=100)