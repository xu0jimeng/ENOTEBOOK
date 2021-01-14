from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic,Entry 
from .forms import TopicForm, EntryForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.



from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def logout_view(request):
	# 注销账户
	logout(request)
	return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
	if request.method != 'POST':
		form = UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()
			authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
			login(request,authenticated_user)
			return HttpResponseRedirect(reverse('learning_logs:index'))
	context = {'form':form}
	return render(request,'users/register.html',context)

	
def index(request):
	# request 是原始请求对象 ——我们知道当URLconf文件匹配到用户输入的路径后会调用对应的view函数
	# 并将HttpRequest对象作为第一个参数传入该函数（request存在不一定用到).
	return render(request,'learning_logs/index.html')


@login_required
def topics(request):
	"""显示所有主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	# topics = Topic.objects.order_by('date_added')--这样可以只允许用户访问自己的主题！
	context = {'topics':topics}
	return render(request,'learning_logs/topics.html',context)
	# render()结合一个给定的模板和一个给定的上下文字典，并返回一个渲染后的HttpResponse对象。
	# 通俗的讲就是把context的内容, 加载进templates中定义的文件, 并通过浏览器渲染呈现.

@login_required
def items(request):
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	# topics = Topic.objects.order_by('date_added')--这样可以只允许用户访问自己的主题！
	context = {'topics':topics}
	return render(request,'learning_logs/items.html',context)


@login_required
def topic(request,topic_id):
	"""显示单个主题及其所有的条目"""
	topic = get_object_or_404(Topic,id=topic_id)
	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic,'entries':entries}
	return render(request,'learning_logs/topic.html',context)


@login_required
def new_topic(request):
	if request.method != 'POST':
		# 如果请求不是POST,则返回一个空表单
		form = TopicForm()
	else:
		form = TopicForm(request.POST)

		if form.is_valid():
			# 函数is_valid()检测用户填写的字段和预指定的是否一致，如果一致则保存。
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
			# 保存过后页面会重新定向到topic页面

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html',context)	


@login_required
def new_entry(request,topic_id):
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
	context = {'form': form, 'topic': topic}
	return render(request, 'learning_logs/new_entry.html',context)		

@login_required
def edit_entry(request,entry_id):
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
	context = {'entry': entry,'topic': topic,'form': form}	
	return render(request, 'learning_logs/edit_entry.html',context)	