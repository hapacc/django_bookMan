from django.db import models

# Create your models here.
class student_info(models.Model):
    student_name = models.CharField("姓名",max_length=4)
    student_major = models.CharField("专业",max_length=5)
    student_borrow_limit = models.IntegerField("借书上限")
    student_id = models.IntegerField("借书号",primary_key=True)
class book_info(models.Model):
    book_name = models.CharField("图书名称",max_length=10,primary_key=True)
    book_publish_date=models.DateField("发布日期")
    book_press=models.CharField("出版社",max_length=12)
    book_loc=models.CharField("存放位置",max_length=10)
    book_sum=models.IntegerField("图书总数量")
    book_stock=models.IntegerField("图书库存")
class borrow_info(models.Model):
    student_id = models.IntegerField("借书号")
    book_name = models.CharField("图书名称",max_length=10)
    borrow_date=models.DateField("借书日期",null=True,auto_now_add=True)
    book_back=models.DateField("还书日期",null=True)
    borrow_sum=models.IntegerField("借书量",null=True)
    borrow_overtime=models.TextField("超时",null=True,max_length=6)
    borrow_fine=models.CharField("罚金",max_length=10,null=True)
    
