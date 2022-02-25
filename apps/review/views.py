from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.costumer.decorators import costumer_required
from apps.order.models import OrderItem
from apps.order.utilities import send_notification
from apps.review.forms import ReviewForm


@login_required
@costumer_required
def leave_review(request, pk):
    item = OrderItem.objects.get(pk=pk)
    vendor = item.vendor

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)

            review.addressed_to = vendor
            review.made_by = item.costumer
            review.save()
            item.is_reviewed = True
            item.save()
            send_notification(sender=request.user, recipient=vendor, action="leave_review")
            messages.success(request, 'Your review has been left successfully')
            return redirect('costumer_admin')
    else:
        form = ReviewForm()

    return render(request, 'review/leave_review.html', {'form': form, 'pk': pk, 'vendor': vendor.name})
