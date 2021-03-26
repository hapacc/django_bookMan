from django.contrib import admin
from .models import book_info,student_info,borrow_info

class book_info_admin(admin.ModelAdmin):
    list_display=('book_name','book_publish_date','book_press','book_loc','book_sum','book_stock')
admin.site.register(book_info,book_info_admin)
class student_info_admin(admin.ModelAdmin):
    list_display=('student_name','student_major','student_borrow_limit','student_id')
admin.site.register(student_info,student_info_admin)
class borrow_info_admin(admin.ModelAdmin):
    list_display=('student_id','book_name','borrow_date','book_back','borrow_sum','borrow_overtime','borrow_fine')
admin.site.register(borrow_info,borrow_info_admin)