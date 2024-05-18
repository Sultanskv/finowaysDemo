from django.shortcuts import render,redirect , HttpResponse
from .forms import ClientLogin
from .forms import *
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from myapp.models import ClientDetail , ClientSignal
from django.utils import timezone
import datetime
from django.contrib import messages
from algosms import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime, timedelta
# Create your views here.
my_global_variable = None
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def logoutUser(request):
    if 'cadmin_id' in request.session:
        del request.session['cadmin_id']
    logout(request)
    return redirect('client_login')

from django.contrib.auth.decorators import login_required

@login_required
def client_dashboard(request):
    # Your view logic here
    return render(request, 'client_dashboard.html')

from django.utils import timezone

def client_login(request):

    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                user_id = ClientDetail.objects.get(email=user.email)
                # Check if last login date is today or later
                if user.last_login.date() >= timezone.now().date():
                    request.session['user_id'] = user_id.user_id

                    alls = SYMBOL.objects.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.user_id , SYMBOL = s.SYMBOL)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.user_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.user_id,
                                SYMBOL = s.SYMBOL,
                                QUANTITY = q
                            )
                            

                    return redirect('/dashboard/')
                else:
                    return redirect('/?msg=your plane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
         #   return HttpResponse('email no register')
            return redirect('/?msg=Email no register') 
     
    return render(request,'client_login.html', {'msg':msg})

# def admin_dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('admin_login')
    # if Account.objects.filter(user_id= request.user.user_id, is_client=True):
    #     client = Client.objects.all()
    #     LeaveRequests = TLeave.objects.filter(is_approved=0)
    #     return render(request,'admin_dashboard.html', context={'allEmp':allEmp, 'LeaveR':LeaveRequests})
    # else:
    #     messages.info(request, 'You Are Not Authorized To Access That Page')
        # return redirect('index')
    # return render(request,'admin_dashboard.html')  
@login_required(login_url='adminlogin')
def admin_dashboard(request):
    # For cards on dashboard
    clientcount = ClientDetail.objects.all().count()
    # Signal count
    # signalcount = models.ClientSignal.objects.all().count()  # Uncomment if needed
   
    # For recent order tables
    clientdetail = ClientDetail.objects.all()
    total_live_account = [10]
    total_demo_account = []
    total_licence = []
    total_2days_service = []
    
    active_live_account = []
    active_demo_account = []
    remaining_licence = []
    active_2days_service = []
    
    expired_total_account = []
    expired_demo_account = []
    used_licence = []
    total_converted_accounts = []
    
    for client in clientdetail:
        # Assuming you have a related field in ClientDetail model to get ordered products
        #  ordered_product=ClientDetail.objects.all().filter(id=client)
        # Do something with ordered_products
        
        # Appending dummy values for demonstration
        # Appending dummy values for demonstration
        total_live_account = ClientDetail.objects.filter(user_id=client.user_id)
        total_demo_account = ClientDetail.objects.filter(user_id=client.user_id)
        total_licence = ClientDetail.objects.filter(user_id=client.user_id)
        total_2days_service = ClientDetail.objects.filter(user_id=client.user_id)

        active_live_account = ClientDetail.objects.filter(user_id=client.user_id)
        active_demo_account = ClientDetail.objects.filter(user_id=client.user_id)
        remaining_licence = ClientDetail.objects.filter(user_id=client.user_id)
        active_2days_service = ClientDetail.objects.filter(user_id=client.user_id)

        expired_total_account = ClientDetail.objects.filter(user_id=client.user_id)
        expired_demo_account = ClientDetail.objects.filter(user_id=client.user_id)
        used_licence = ClientDetail.objects.filter(user_id=client.user_id)
        total_converted_accounts = ClientDetail.objects.filter(user_id=client.user_id)
        
    mydict = {
        'clientcount': clientcount,
        # 'signalcount': signalcount,  # If needed    
        'data': zip(total_live_account, total_demo_account, total_licence, total_2days_service,
                    active_live_account, active_demo_account, remaining_licence, active_2days_service,
                    expired_total_account, expired_demo_account, used_licence, total_converted_accounts),
    }
    return render(request, 'admin_dashboard.html', context=mydict)


       

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils import timezone
scheduler = BackgroundScheduler()

# Function to create attendance records for employees
@transaction.atomic
def symbol_inactive():
    timezone.activate('Asia/Kolkata')
    ss = Client_SYMBOL_QTY.objects.all()
    for s in ss:
        s.trade = None
        s.save()       
# Set the job to run every day at 12:00 AM
# scheduler.add_job(symbol_inactive, 'cron', hour=0, minute=1)
# scheduler.start()


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"  
        except:
            error = "yes"          
    return render(request,'admin_login.html', locals()) 


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def create_superuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                User.objects.create_superuser(username=username, email=email, password=password1)
                return redirect('admin_login')
                # return HttpResponse('Superuser created successfully!')
            except:
                return HttpResponse('Error creating superuser. Please try again.')
        else:
            return HttpResponse('Passwords do not match. Please try again.')
    else:
        return render(request, 'admin_register.html')
    
    
def admin_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return render(request, 'change_password.html', {'msg': 'Password updated successfully', 'error': 'no'})
            else:
                return render(request, 'change_password.html', {'msg': 'New Password and Confirm Password fields do not match', 'error': 'yes'})
        else:
            return render(request, 'change_password.html', {'msg': 'Your current password is wrong', 'error': 'not'})
    else:
        return render(request, 'change_password.html', {})    


# =====================================================================================

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['fname']
        ln = request.POST['lname']
        mo = request.POST['mobile']
        em = request.POST['email']
        fromd = request.POST['fromdate']
        tod = request.POST['todate']
        pwd = request.POST['pwd']
        print(fromd, ' to ', tod)
        try:
            try:
                u = ClientDetail.objects.get(email=em)
                return render(request,'register.html',{'msg': 'email all ready registration '}) 
            except:    
         #   user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
                ClientDetail.objects.create(
                                        name_first = fn,
                                        name_last = ln,
                                        email = em,
                                        password = pwd,
                                        phone_number = mo,
                                        date_joined	= fromd,
                                        last_login	= tod
                                                    )
                # Construct the email message
                # subject = 'your email paswword'
                # message = f'Name: {fn,ln}\nEmail: {em}\nPassword: {pwd}\n\nphone:\n{mo}'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [em]  # Add recipient email addresses here
                
             
                # try:
                #     # Send email
                #     send_mail(subject, message, email_from, recipient_list)
                # #    send_mail(subject, body, from_email, to_email, fail_silently=False)
                #     return redirect('/')
                # except Exception as e:
                #     # Handle any errors
                # #  return HttpResponse('error.html', {'error': str(e)})
                #    # return render(request, 'contact.html',{'msg':f'{e}'})
                #     return render(request,'register.html',{'msg': f'{e}'}) 
                
        except Exception as e:
            return render(request,'register.html',{'msg': f'error {e}'}) 
    return render(request,'register.html',)    




# Function to handle admin messages
import random
import string


def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id
#ids = None
def admin_message(request):
    error = ""
    symbols = SYMBOL.objects.all()  # Fetch all SYMBOL objects
    user = request.user
    current_date = timezone.now().date()
    d = request.session.get('message_id')
    if request.method == "POST":
        if request.user.is_authenticated:
            client_signals = ClientSignal.objects.filter( message_id = d , ids = 'No')
            
            user = request.user
            symbol_name = request.POST['symbol']  # Get the symbol name from the form
            sy = get_object_or_404(SYMBOL, SYMBOL=symbol_name)  # Fetch the corresponding SYMBOL instance
            # sy = request.POST['symbol']
            ty = request.POST['type']
         
            qty_str = request.POST['quantity']
         
            if ty == 'BUY_EXIT' or ty == 'SELL_EXIT':
                    for client_signal in client_signals:
                        print('test for ')
                        if qty_str.strip():  # Check if quantity string is not empty or only whitespace
                            qty = float(qty_str)
                        elif ty == 'BUY_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = float(request.POST['exit_price'])

                        elif ty == 'SELL_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = float(request.POST['exit_price'])    

                        else:
                            qty = 0 # Set qty to a default value or handle it according to your logic
                            enp = float(request.POST['entry_price'])
                            exp =  None
                    
                    
                        if ty == 'BUY_EXIT':
                        #    print('BUY_EXIT')
                            prloss = (float(exp) - float(enp)) * qty*100
                            t = ClientSignal.objects.filter( TYPE = 'BUY_EXIT' , client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = float(total) + float(prloss)
                            print(total_pl)

                        elif ty == 'SELL_EXIT':
                            print('SELL_EXIT')
                            prloss = (float(enp) - float(exp)) * qty*100
                            t = ClientSignal.objects.filter( TYPE = 'SELL_EXIT' ,client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                            #    print(total)
                            
                        
                            total_pl = float(total) + float(prloss)
                        #    print(total_pl)
                            
                    
                            
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                    ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss, 
                                                    cumulative_pl=total_pl, created_at=timezone.now(),
                                                    message_id = client_signal.message_id ,client_id  = client_signal.client_id )
                

            else:
                    qty = 0 # Set qty to a default value or handle it according to your logic
                    enp = float(request.POST['entry_price'])
                    exp =  None
                    prloss = None
                    total_pl = None                                    
                    if ty == 'BUY_ENTRY' or ty == 'SELL_ENTRY':
                        
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, admin = 'admin',TYPE=ty, QUANTITY=qty, 
                                                ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=prloss, 
                                                cumulative_pl=total_pl, created_at=timezone.now())
                        i = generate_unique_id()
                        creat.message_id = creat.id
                        creat.ids = i 
                        creat.save()      
                        request.session['message_id'] = creat.id
                    #    request.session['ids'] = i
                        global my_global_variable
                        my_global_variable = i
                        
                        error = "no"
                        result = add_singnal_qty(request)
    return render(request, 'admin_messages.html',{'symbols': symbols, 'error': error})
########################

''' 
def admin_message(request):
    error = ""
    user = request.user
    current_date = timezone.now().date()
    d = request.session.get('message_id')
    if request.method == "POST":
        if request.user.is_authenticated:
            client_signals = ClientSignal.objects.filter( message_id = d , ids = 'No')
            
            user = request.user
            sy = request.POST['symbol']
            ty = request.POST['type']
         
            qty_str = request.POST['quantity']
         
            if ty == 'BUY_EXIT' or ty == 'SELL_EXIT':
                    for client_signal in client_signals:
                        if qty_str.strip():  # Check if quantity string is not empty or only whitespace
                            qty = int(qty_str)
                        elif ty == 'BUY_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = int(request.POST['exit_price'])

                        elif ty == 'SELL_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = int(request.POST['exit_price'])    

                        else:
                            qty = 0 # Set qty to a default value or handle it according to your logic
                            enp = int(request.POST['entry_price'])
                            exp =  None
                    
                    
                    
                        if ty == 'BUY_EXIT':
                            print('BUY_EXIT')
                            prloss = (float(exp) - float(enp)) * qty
                            t = ClientSignal.objects.filter( TYPE = 'BUY_EXIT' , client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = int(total) + int(prloss)
                            print(total_pl)

                        elif ty == 'SELL_EXIT':
                            print('SELL_EXIT')
                            prloss = (float(exp) - float(enp)) * qty
                            t = ClientSignal.objects.filter( TYPE = 'SELL_EXIT' ,client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = int(total) + int(prloss)
                            print(total_pl)
                            
                    
                            
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                    ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss, 
                                                    cumulative_pl=total_pl, created_at=timezone.now(),
                                                    message_id = client_signal.message_id ,client_id  = client_signal.client_id )
                

            else:
                    qty = 0 # Set qty to a default value or handle it according to your logic
                    enp = int(request.POST['entry_price'])
                    exp =  None
                    prloss = None
                    total_pl = None                                    
                    if ty == 'BUY_ENTRY' or ty == 'SELL_ENTRY':
                        
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=prloss, 
                                                cumulative_pl=total_pl, created_at=timezone.now())
                        i = generate_unique_id()
                        creat.message_id = creat.id
                        creat.ids = i
                        creat.save()      
                        request.session['message_id'] = creat.id
                    #    request.session['ids'] = i
                        global my_global_variable
                        my_global_variable = i
                       
                        error = "no"
         
    return render(request, 'admin_messages.html', )
'''
 
def admin_signals(request):
    buy_entry_signals = ClientSignal.objects.filter(TYPE='BUY_ENTRY')
    buy_exit_signals = ClientSignal.objects.filter(TYPE='BUY_EXIT')
    return render(request, 'admin_signals.html', {'buy_entry_signals': buy_entry_signals, 'buy_exit_signals': buy_exit_signals})

def admin_thistory(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    clientsignal = ClientSignal.objects.all()
    return render(request,'admin_thistory.html',locals())

def admin_tstatus(request):
    return render(request,'admin_tstatus.html')

def admin_client(request):
    return render(request,'admin_client.html')


def client_dashboard(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)
        
        
        current_date = timezone.now().date()
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id = user_id)
        
        if request.method == 'POST':
            print('pst')
            # XAUUSD
            q1 = request.POST.get('QUANTITY1')
            o1 = request.POST.get('ORDER_TYPE1')
            t1 = request.POST.get('TRADING1')
            print(q1,o1,t1)
            # USOIL
            q2 = request.POST.get('QUANTITY2')
            o2 = request.POST.get('ORDER_TYPE2')
            t2 = request.POST.get('TRADING2')
            print(q2,o2,t2)
            # EURUSD
            q3 = request.POST.get('QUANTITY3')
            o3 = request.POST.get('ORDER_TYPE3')
            t3 = request.POST.get('TRADING3')
            print(q3,o3,t3)
            # USDJPY
            q4 = request.POST.get('QUANTITY4')
            o4 = request.POST.get('ORDER_TYPE4')
            t4 = request.POST.get('TRADING4')
            print(q4,o4,t4)
            # GBPUSD
            q5 = request.POST.get('QUANTITY5')
            o5 = request.POST.get('ORDER_TYPE5')
            t5 = request.POST.get('TRADING5')
            print(q5,o5,t5)
            value = my_global_variable
            try:
                
                
                Client_symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id = user_id)
                
                for q in Client_symbol_qty:
                    if q.SYMBOL == 'XAUUSD':
                        if t1 == 'on':
                            q.QUANTITY = float(q1)
                            q.trade = t1
                            q.save() 
                        else:
                            q.trade = t1 
                            q.save()    

                    elif q.SYMBOL == 'USOIL':
                        if t2 == 'on':
                            q.QUANTITY = float(q2)
                            q.trade = t2 
                            q.save()  
                        else:
                            q.trade = t2 
                            q.save()        

                    elif q.SYMBOL == 'EURUSD':
                        if t3 == 'on':
                            q.QUANTITY = float(q3)
                            q.trade = t3  
                            q.save() 
                        else:
                            q.trade = t3 
                            q.save()      

                    elif q.SYMBOL == 'USDJPY':
                        if t4 == 'on':
                            q.QUANTITY = float(q4)
                            q.trade = t4  
                            q.save() 
                        else:
                            q.trade = t4 
                            q.save()      
                        
                    elif q.SYMBOL == 'GBPUSD':
                        if t5 == 'on':
                            q.QUANTITY = float(q5)
                            q.trade = t5 
                            q.save()    
                        else:
                            q.trade = t5 
                            q.save()       

                  
                return redirect('client_dashboard')
            except Exception as e:
                error = str(e)
                print(error)


        return render(request,'client_dashboard.html',{'signals':filtered_signals})
    except:
        return redirect('login')

def add_singnal_qty(request):
    Client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    value = my_global_variable
    try:
        client_signal = ClientSignal.objects.get(ids= value) 
        for q in Client_symbol_qty:
            print('for tes qq', q.SYMBOL)
            print('for tes cc',client_signal.SYMBOL)
            print('for')
            if q.trade == 'on':
                print('on')    
                if str(q.SYMBOL) == str(client_signal.SYMBOL):
                    print('symbol')
                    print(q.SYMBOL)
                    print(client_signal.SYMBOL)
                    print('creat singnal')
                    creat = ClientSignal.objects.create(
                        user=client_signal.user,
                        SYMBOL=client_signal.SYMBOL,
                        TYPE=client_signal.TYPE,
                        ENTRY_PRICE=client_signal.ENTRY_PRICE,
                        ids = 'No',
                        QUANTITY=q.QUANTITY,
                        message_id = client_signal.message_id,
                        client_id = q.client_id,
                        created_at = timezone.now()
                    )

                    
        return HttpResponse('pass function')    
    except Exception as e:
        error = str(e)
        print(error)   
        return HttpResponse(f'error = {e}') 

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ClientSignal
from django.contrib import messages
from datetime import datetime, date
from django.http import HttpResponseNotFound

# client_signals client get method          
def client_signals(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        dt = {
            "s": signals_today,
        
        }
        return render(request, 'client_signals.html', dt)
    except:
        return redirect('client_login')
        
    
   
    
from django.db.models import Sum

def client_trade_history(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        # Calculate total profit and loss for today
        total_cumulative_pl = signals_today.aggregate(total_pl=Sum('cumulative_pl'))['total_pl']

        dt = {
            "s": signals_today,
            "total_cumulative_pl": total_cumulative_pl
        }
        return render(request, 'client_thistory.html', dt)
    except:
        return redirect('client_login')




def change_password(request):
    try:
        #    print('test form' ) 
        user_id = request.session.get('user_id')
    
        client_user = ClientDetail.objects.get(user_id=user_id)
        if request.method == "POST":
            c = request.POST['currentpassword']
            n = request.POST['newpassword']
            f = request.POST['confirmpassword']

            if c == client_user.password and n == f:
                client_user.password = n
                client_user.save()
                return redirect('/?msg=chenge password')  
            else:
                return render(request,'client_change_password.html',{'msg':'samthing wrong'})    
        return render(request,'client_change_password.html',locals(),)       
    except:
        return redirect('client_login')        


def admin_change_password(request):
    if not request.user.is_authenticated:
        return redirect('client_login')
    error = ""
    user = request.user
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"  
            else:
                error = "not"    
        except:
            error = "yes"
    return render(request,'admin_change_password.html',locals(),{'error': error}) 


def Settings(request):
    return render(request,'settings.html')

# ===============================Symbolic qty =============================
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client_SYMBOL_QTY
from .forms import Client_SYMBOL_QTYForm

def create_client_symbol_qty(request):
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')  # Redirect to the list view
    else:
        form = Client_SYMBOL_QTYForm()
    return render(request, 'create_client_symbol_qty.html', {'form': form})

def client_symbol_qty_list(request):
    client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    return render(request, 'client_symbol_qty_list.html', {'client_symbol_qty': client_symbol_qty})

def edit_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST, instance=client_symbol_qty)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')
    else:
        form = Client_SYMBOL_QTYForm(instance=client_symbol_qty)
    return render(request, 'edit_client_symbol_qty.html', {'form': form})

def delete_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        client_symbol_qty.delete()
        return redirect('client_symbol_qty_list')
    return render(request, 'delete_client_symbol_qty.html', {'client_symbol_qty': client_symbol_qty})


# ========================== SYMBOL ====================================================

# =======================================================================================
from .forms import SymbolForm

def symbol_list(request):
    symbols = SYMBOL.objects.all()
    return render(request, 'symbol_list.html', {'symbols': symbols})

def create_symbol(request):
    if request.method == 'POST':
        form = SymbolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('symbol_list')
    else:
        form = SymbolForm()
    return render(request, 'create_symbol.html', {'form': form})

def update_symbol(request, symbol_id):
    # Retrieve the symbol object from the database
    symbol = get_object_or_404(SYMBOL, id=symbol_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = SymbolForm(request.POST, instance=symbol)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('symbol_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = SymbolForm(instance=symbol)
    
    return render(request, 'update_symbol.html', {'form': form, 'symbol': symbol})



def delete_symbol(request, symbol_id):
    symbol = SYMBOL.objects.get(id=symbol_id)
    if request.method == 'POST':
        symbol.delete()
        return redirect('symbol_list')  # Redirect to the symbol list page after deletion
    return render(request, 'delete_symbol.html', {'symbol': symbol})


from django.shortcuts import render, redirect
from .models import HelpMessage
from .forms import HelpMessageForm

def client_help_center(request):
    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_help_center')  # Redirect to the same page or a thank you page
    else:
        form = HelpMessageForm()
    return render(request, 'client_help_center.html', {'form': form})

def admin_help_center(request):
    messages = HelpMessage.objects.all().order_by('-timestamp')
    return render(request, 'admin_help_center.html', {'messages': messages})

def client_tstatus(request):
    return render(request,'client_tstatus.html')

def multibank(request):
    return render(request,'multibank.html')

