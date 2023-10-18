from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout , authenticate
from .forms import ToDoForm
from .models import ToDo
from django.utils import  timezone

def signup(request):
    if request.method == 'GET':
        return render(request ,'todo/signup.html')


    else:
        Password = request.POST["password"]
        Password2 = request.POST["password2"]
        UserName = request.POST["name"]

        if Password == Password2:
            if not User.objects.filter(username = UserName).exists() :
                Person = User.objects.create_user(username=UserName , password=Password)
                Person.save()
                login(request , Person)
                return redirect('home')
            else:
                return render(request, 'todo/signup.html', {'error': 'Пользователь с таким именем уже существует'})

        else :
            return render(request, 'todo/signup.html' ,{'error' : 'Пароли не совпадают'})

@login_required()
def create(request):
    if request.method == "GET":
        return  render(request,'todo/create.html', {'form': ToDoForm()})
    else:
        form = ToDoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('home')

@login_required
def home(request):
    todos = ToDo.objects.filter(user=request.user ,finishedDate__isnull=True).order_by('-createdDate')
    return render(request ,'todo/home.html', {'todos': todos})
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/login.html')
    else:
        Person = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if Person is None :
            return render(request, 'todo/login.html', {'error': 'Неверные данные для входа'})
        else:
            login(request,Person)
            return redirect('home')

@login_required
def showtodo(request ,todo_id):
    todo = get_object_or_404(ToDo ,pk=todo_id ,user = request.user)

    if request.method == "GET":
        todo_form = ToDoForm(instance=todo)
        return render(request, 'todo/todoview.html', {"form":todo_form , "todo":todo})
    else:
        form = ToDoForm(request.POST , instance=todo)
        form.save()
        return redirect('home')

@login_required
def complete(request ,todo_id):
    if request.method == "POST":
        todo = get_object_or_404(ToDo , pk =todo_id , user = request.user)
        todo.finishedDate = timezone.now()
        todo.save()
        return redirect('home')

@login_required
def completed(request):
    todos = ToDo.objects.filter(user = request.user , finishedDate__isnull=False).order_by('-finishedDate')
    return render(request ,'todo/completed.html' ,{'todos':todos})

@login_required
def deleteToDo(request ,todo_id):
    try:
        todos = get_object_or_404(ToDo ,pk = todo_id , user = request.user)
        todos.delete()
        return redirect('home')
    except:
        return redirect('home')