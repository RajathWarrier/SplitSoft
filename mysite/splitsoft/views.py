from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.contrib.auth.models import User as djUser

from . import models
from . import forms

def registration_view(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            user = form_instance.save()
            login(request, user)
            return redirect("/dashboard")
    else:
        form_instance = forms.RegistrationForm(request.POST)
    
    context = {
        "title": "SplistSoft - Registration",
        "form": form_instance
    }

    return render(request, "registration/register.html", context=context)

def logoutView(request):
    logout(request)
    return redirect('/')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = models.User.objects.filter(fName__icontains=request.user.first_name).filter(lName__icontains=request.user.last_name)
    groups = user[0].groups.all()
    owe = models.Owe.objects.filter(who=user[0]).exclude(amount=0)
    owed = models.Owe.objects.filter(whom=user[0]).exclude(amount=0)
    context = {
        "title": "SplitSoft - Dashboard",
        "grouplist": groups,
        "owe": owe,
        "owed": owed
    }
    return render(request, 'dashboard.html', context=context)

def newgroupview(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form_instance = forms.AddGroupForm(request.POST)
        if form_instance.is_valid():
            groupName = form_instance.cleaned_data.get("groupName")
            # users = form_instance.cleaned_data.get("users")
            users = request.POST.getlist('users')
            userList = []
            for user_id in users:
                userList.append(models.User.objects.get(pk = user_id))
            newGroup = models.Group(name=groupName, total_expense=0)
            newGroup.save()
            for user in userList:
                user.groups.add(newGroup)
            return redirect("/dashboard")
    else:
        form_instance = forms.AddGroupForm(request.POST)
    
    context = {
        "title": "SplitSoft - New Group",
        "form": form_instance,
        "users": models.User.objects.all()
    }
    return render(request, "newgroup.html", context=context)

def groupview(request, id):
    if not request.user.is_authenticated:
        return redirect('/')
    group = models.Group.objects.get(pk=id)
    groupName = group.name.replace(" ", "")
    context = {
        "title": "SplitSoft - Group",
        "group": group,
        "groupName": groupName
    }
    return render(request, "group.html", context=context)

def adduserview(request, g_id):
    if not request.user.is_authenticated:
        return redirect('/')
    group = models.Group.objects.get(pk=g_id)
    querylist = []
    search = request.POST.get('search')
    if search != None:
        querylist = models.User.objects.filter(
            fName__icontains = search
        )
    context = {
        "title": "SplitSoft - Add Member",
        "group": group,
        "querylist": querylist
    }
    return render(request, "adduser.html", context=context)

def adduserconfirmation(request, g_id, u_id):
    if not request.user.is_authenticated:
        return redirect('/')
    user = models.User.objects.get(pk=u_id)
    group = models.Group.objects.get(pk=g_id)
    user.groups.add(group)
    return redirect('/group/' + str(g_id))

def removeuserview(request, g_id, u_id):
    if not request.user.is_authenticated:
        return redirect('/')
    user_del = models.User.objects.get(pk=u_id)
    user_grp = models.Group.objects.get(pk=g_id)
    if request.method == "POST":
        user_del.groups.remove(user_grp)
        currGroup = models.Group.objects.get(pk=g_id)
        if currGroup.user_set.all().count() == 0:
            currGroup.delete()
        return redirect('/group/' + str(g_id))
    context = {
        "title": "SplitSoft - Delete User",
        "user": user_del,
        "gid": g_id,
        "group": user_grp
    }
    return render(request, "remove.html", context=context)

def addexpenseview(request, g_id):
    if not request.user.is_authenticated:
        return redirect('/')
    group = models.Group.objects.get(pk=g_id)
    payer = request.POST.get('payers')
    amount = request.POST.get('amount')
    expensename = request.POST.get('expensename')
    n = group.user_set.count()
    if payer != None and amount != None:
        querylist = models.User.objects.filter(
            fName__icontains = payer
        )
        querylist2 = group.user_set.all()
        who = []
        for item in querylist2:
            if item != querylist[0]:
                who.append(item)
        newExpense = models.Expense(name=expensename, amount=amount, group=group, payer=querylist[0])
        newExpense.save()
        group.total_expense += float(amount)
        group.save()

        for user in who:
            querylist3 = models.Owe.objects.filter(who=user).filter(whom=querylist[0])
            querylist4 = models.Owe.objects.filter(who=querylist[0]).filter(whom=user)
            if len(querylist3) == 0 and len(querylist4) == 0:
                oweItem = models.Owe(who=user, whom=querylist[0], amount=float(amount) / n, group=group)
                oweItem.save()
            elif len(querylist3) != 0:
                querylist3[0].amount += float(amount) / n
                querylist3[0].save()
            else:
                if querylist4[0].amount < float(amount) / n:
                    newAmount = float(amount) / n - querylist4[0].amount
                    newRecord = models.Owe(who=querylist4[0].whom, whom=querylist4[0].who, amount=newAmount, group=group)
                    newRecord.save()
                    querylist4[0].delete()
                else:
                    querylist4[0].amount -= float(amount) / n
                    querylist4[0].save()
                    
            
        return redirect("/group/" + str(g_id))

    context = {
        "title": "SplitSoft - Add Expense",
        "group": group
    }
    return render(request, "addexpense.html", context=context)

def deleteexpenseview(request, e_id, g_id):
    if not request.user.is_authenticated:
        return redirect('/')
    expenseInstance = models.Expense.objects.get(pk=e_id)
    groupInstance = models.Group.objects.get(pk=g_id)
    groupInstance.total_expense -= expenseInstance.amount
    groupInstance.save()
    n = groupInstance.user_set.all().count()
    oweInstances1 = models.Owe.objects.filter(group=groupInstance).filter(whom=expenseInstance.payer)
    oweInstances2 = models.Owe.objects.filter(group=groupInstance).filter(who=expenseInstance.payer)
    if len(oweInstances1) != 0:
        for record in oweInstances1:
            if record.amount < expenseInstance.amount / n:
                newRevRecord = models.Owe(who=record.whom, whom=record.who, group=record.group, amount=(expenseInstance.amount / n - record.amount))
                newRevRecord.save()
                record.delete()
            else:
                record.amount -= expenseInstance.amount / n
                record.save()
    else:
        for record in oweInstances2:
            record.amount += expenseInstance.amount / n
            record.save()

    expenseInstance.delete()
    return redirect("/group/" + str(g_id))

def showsplitview(request, g_id):
    if not request.user.is_authenticated:
        return redirect('/')
    currGroup = models.Group.objects.get(pk=g_id)
    split = models.Owe.objects.filter(group=currGroup).exclude(amount=0.0)
    context = {
        "title": "SplitSoft - Split",
        "split": split,
        "group_id": g_id
    }
    return render(request, "split.html", context=context)
def settleview(request, g_id, s_id):
    oweInstance = models.Owe.objects.get(pk=s_id)
    oweInstance.delete()
    return redirect('/group/' + str(g_id) + '/split')
def expensesview(request, g_id):
    if not request.user.is_authenticated:
        return redirect('/')
    groupInstance = models.Group.objects.get(pk=g_id)
    expenses = models.Expense.objects.filter(group=groupInstance)
    context = {
        "title": "SplitSoft - Expenses",
        "expenses": expenses,
        "group_id": g_id
    }
    return render(request, "expenses.html", context=context)

def chatroom(request, room_name):
    if not request.user.is_authenticated:
        return redirect('/')
    user = models.User.objects.filter(fName__icontains=request.user.first_name).filter(lName__icontains=request.user.last_name)
    userGroups = user[0].groups.all()
    g_id = 0
    for grp in userGroups:
        if grp.name.replace(" ", "") == room_name:
            g_id = grp.id
    context = {
        "title": "SplitSoft - Chat",
        "room_name": room_name,
        "user": user[0],
        "gid": g_id
    }
    return render(request, "chatroom.html", context=context)