from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Customer, Comment, User
from .forms import CustomerForm, CommentForm, LoginForm
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'crm/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    search = request.GET.get('search', '')
    customers = Customer.objects.all()
    
    if search:
        customers = customers.filter(
            Q(business_name__icontains=search) |
            Q(contact_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    
    context = {
        'customers': customers,
        'search': search,
        'user_type': request.user.user_type,
    }
    return render(request, 'crm/dashboard.html', context)

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    comments = customer.comments.all()[:20]  # Latest 20 comments
    
    if request.method == 'POST' and request.user.user_type in ['admin', 'user']:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.customer = customer
            comment.user = request.user
            comment.save()
            return redirect('customer_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'customer': customer,
        'comments': comments,
        'comment_form': comment_form,
        'user_type': request.user.user_type,
    }
    return render(request, 'crm/customer_detail.html', context)

@login_required
def customer_create(request):
    if request.user.user_type not in ['admin', 'user']:
        return HttpResponseForbidden("You don't have permission to create customers.")
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Add Customer'})

@login_required
def customer_edit(request, pk):
    if request.user.user_type not in ['admin', 'user']:
        return HttpResponseForbidden("You don't have permission to edit customers.")
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Edit Customer'})

@login_required
def customer_delete(request, pk):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can delete customers.")
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'crm/customer_delete.html', {'customer': customer})