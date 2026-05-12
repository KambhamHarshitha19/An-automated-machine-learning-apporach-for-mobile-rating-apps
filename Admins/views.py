from django.shortcuts import render
from django.contrib import messages
from Users.models import UserRegisterModel

#============================================================================================
def AdminLogin(request):
    if request.method == 'POST':
        username =    request.POST.get('admin_username')
        password =    request.POST.get('admin_password')
        print(username , password)
        try:
            if username=='admin' and password=='admin':
                return render(request, 'admins/AdminHome.html')
            else:
                messages.warning(request  , 'Invalid credentials')
                return render(request, 'Adminlgoin.html')
        except Exception as e:
            messages.warning(request  , f'{e} ')
    return render(request, 'Adminlgoin.html')
#============================================================================================

def AdminHome(request):
    return render(request, 'admins/AdminHome.html')

#============================================================================================
def viewusers(request):
    data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html', {'data':data})

#============================================================================================
from django.shortcuts import render, get_object_or_404, redirect


def delete_user(request):
    if request.method == 'POST':  # Use POST for security
        uid = request.POST.get('id')
        user = get_object_or_404(UserRegisterModel, id=uid)
        user.delete()
        messages.success(request, f'User {uid} has been deleted successfully!')

    return redirect(viewusers)  # Redirect after deletion


def activate_user(request, uid):
    user = get_object_or_404(UserRegisterModel, id=uid)
    user.status = 'Activate'
    user.save()
    messages.success(request, f'User {uid} has been activated successfully!')

    return redirect(viewusers)  # Redirect after activation


#============================================================================================
def Deactivateusers(request):
    if request.method == 'GET':
        uid = request.GET.get('id')
        status ='waiting'
        UserRegisterModel.objects.filter(id=uid).update(status=status)
        data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html' , {'data':data})


#============================================================================================

# def Deleteusers(request):
#     if request.method == 'GET':
#         uid = request.GET.get('id')
#         UserRegisterModel.objects.get(id=uid).delete()
#         data= UserRegisterModel.objects.all()
#     return render(request, 'admins/Viewregisterusers.html' , {'data':data})