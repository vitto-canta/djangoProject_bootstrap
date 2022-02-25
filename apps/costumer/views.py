from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.costumer.decorators import costumer_required
from apps.order.models import OrderItem
from apps.order.utilities import send_notification


@login_required
@costumer_required
def costumer_admin(request):
    costumer = request.user.costumer

    orders = costumer.buyers.all()
    products = costumer.costumers.filter(is_sold=False)

    return render(request, 'costumer/costumer_admin.html',
                  {'costumer': costumer, 'orders': orders, 'products': products})


@login_required
@costumer_required
def confirm_delivery(request, pk):
    item = OrderItem.objects.get(pk=pk)

    item.is_received = True
    item.save()
    send_notification(sender=request.user, recipient=item.vendor, action="confirm_delivery", product=item.product)
    return redirect("costumer_admin")


@login_required
@costumer_required
def edit_costumer(request):
    costumer = request.user.costumer

    if request.method == 'POST':
        name = request.POST.get('name', '')

        if name:
            costumer.name = name
            costumer.save()
            messages.success(request, 'Your costumer name has been changed')
            return redirect('costumer_admin')

    return render(request, 'costumer/edit_costumer.html', {'costumer': costumer})
