from django.contrib import admin
from util.models import StudentBase,SchemeMaster,CollegeTypeMaster
 
from django.urls import reverse
from django.utils.safestring import mark_safe
import river_admin

def create_river_button(obj, transition_approval):
    approve_ticket_url = reverse('approve_ticket', kwargs={'ticket_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return f"""
        <input
            type="button"
            style="margin:2px;2px;2px;2px;"
            value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
            onclick="location.href=\'{approve_ticket_url}\'"
        />
    """
 

class StudentBaseAdmin(admin.ModelAdmin):
    list_display = ('name','user', 'pin_number', 'fee_concession_status','created_by','created_on','updated_by','status', 'river_actions') #helps to show the fields

    def get_list_display(self, request):
        self.user = request.user
        return super(StudentBaseAdmin, self).get_list_display(request)

    def river_actions(self, obj):
        content = ""
        for transition_approval in obj.river.status.get_available_approvals(as_user=self.user):
            content += create_river_button(obj, transition_approval)

        return mark_safe(content)



admin.site.register(StudentBase,StudentBaseAdmin)
admin.site.register(SchemeMaster)
admin.site.register(CollegeTypeMaster)




class StudentBaseRiverAdmin(river_admin.RiverAdmin):
    name = "Student BAse"
    icon = "mdi-ticket-account"
    list_displays = ['pk', 'name', 'user', 'pin_number', 'fee_concession_status','status']


river_admin.site.register(StudentBase, "status", StudentBaseRiverAdmin)
