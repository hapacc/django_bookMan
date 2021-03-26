#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from bookMain.models import book_info,student_info,borrow_info
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime,re

def login(request):
    return render(request,'./registration/login.html')

@login_required
def index(request):
    bookinfo=book_info.objects.all()
    page_no = int(request.GET.get("page_no", "1"))
    object_list, pagination_data = paginate_queryset(bookinfo, page_no, count_per_page=10)
    return render(request,'index.html',{'bookinfo':object_list,"pagination_data": pagination_data})

@login_required
def stu(request):
    studentinfo=student_info.objects.all()
    page_no = int(request.GET.get("page_no", "1"))
    object_list, pagination_data = paginate_queryset(
       studentinfo, page_no, count_per_page=10)
    return render(request,'student.html',{'studentinfo':object_list,"pagination_data": pagination_data})

@login_required
def borrow(request):
    borrowinfo=borrow_info.objects.all()
    page_no = int(request.GET.get("page_no", "1"))
    object_list, pagination_data = paginate_queryset(borrowinfo, page_no, count_per_page=10)
    return render(request,'borrow.html',{'borrowinfo':object_list,"pagination_data": pagination_data})

@login_required
def borrow_books(request):
    if request.method == "GET":
        return render(request,'borrow-books.html')
    elif request.method == "POST":
        a=0
        student_id = request.POST["id"].strip()
        book_name = request.POST["name"].strip()
        borrow_sum = int(request.POST["sum"].strip())
        new_book = book_info.objects.filter(book_name=book_name)
        new_id=borrow_info.objects.filter(student_id=student_id,borrow_fine__gt=0)
        try:
            for i in new_id:
                if i.borrow_fine>0:
                    messages.add_message(request, messages.INFO, u'借书失败')
                    a=1
            for i in new_book:
                book_sum=i.book_sum
                if borrow_sum>i.book_stock:
                    messages.add_message(request, messages.INFO, u'借书失败')
                    a=1
            if a==0:
                new_borrow = borrow_info(student_id=student_id,book_name= book_name,borrow_sum= borrow_sum)
                new_borrow.save()
                new_book.update(book_stock=book_sum-borrow_sum)
                messages.add_message(request, messages.INFO, u'借书成功')
            return render(request,'borrow-books.html',{"text": messages})
        except:
            messages.add_message(request, messages.INFO, u'不存在的借书证或书籍')
            return render(request,'borrow-books.html',{"text": messages})

@login_required       
def back_books(request):
    if request.method == "GET":
        return render(request,'back-books.html')
    elif request.method == "POST":
        student_id = request.POST["id"].strip()
        book_name = request.POST["name"].strip()
        back_sum=int(request.POST["sum"].strip())
        new_borrow = borrow_info.objects.filter(student_id=student_id,book_name=book_name,borrow_date__isnull=False)
        new_book=book_info.objects.filter(book_name=book_name)
        for i in new_book:book_stock=i.book_stock
        for i in new_borrow:
            i.book_back=datetime.date.today()
            i.borrow_overtime=str(i.book_back-i.borrow_date)
            if re.search(r"days",i.borrow_overtime):
                i.borrow_overtime=int(i.borrow_overtime.split('days,')[0])
                if i.borrow_overtime>=30:
                    new_borrow.update(borrow_overtime=i.borrow_overtime,book_back=i.book_back,borrow_fine=i.borrow_overtime*1.5)
                    new_book.update(book_stock=book_stock+back_sum)
                else:
                    new_borrow.update(book_back=i.book_back)
                    new_book.update(book_stock=book_stock+back_sum)
            else:
                new_borrow.update(book_back=i.book_back)
                new_book.update(book_stock=book_stock+back_sum)
        return redirect(r'/borrow')

def paginate_queryset(objs, page_no, count_per_page=10, half_show_length=5):
    p = Paginator(objs, count_per_page)
    if page_no > p.num_pages:
        page_no = p.num_pages
    if page_no <= 0:
        page_no = 1
    page_links = [i for i in range(page_no - half_show_length, page_no + half_show_length + 1)
                  if i > 0 and i <= p.num_pages]
    page = p.page(page_no)
    previous_link = page_links[0]-1
    next_link = page_links[-1]+1
    pagination_data = {"has_previous": previous_link > 0,
                       "has_next": next_link <= p.num_pages,
                       "previous_link": previous_link,
                       "next_link": next_link,
                       "page_cnt": p.num_pages,
                       "current_no": page_no,
                       "page_links": page_links}
    return(page.object_list, pagination_data)

@login_required
def register(request):
    errors=''
    if request.method=='GET':
        return render(request,'register.html')
    else:
        username=request.POST['username'].strip()
        email=request.POST['email'].strip()
        password=request.POST['password'].strip()
        re_password=request.POST['re_password'].strip()
        if not username or not password or not email:
            errors='任何字段不能为空'
        if password != re_password:
            errors='两次密码不一致'
        if User.objects.filter(username=username).exists():
            errors='用户已存在'
        if not errors:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return render(request,'./registration/login.html')
        else:
            return render(request,'register.html',{'errors':errors})

