from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def send_overdue_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        if not loan.is_overdue:
            return "Loan is not overdue"
        
        member_email = loan.member.user.email
        book_title = loan.book.title
        days_overdue = loan.days_overdue

        send_mail(
            subject='Overdue Book Reminder',
            message=f'Dear {loan.member.user.username},\n\nYour book "{book_title}" is now {days_overdue} days overdue.\n Due date was {loan.due_date}, please return it as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )

        return f"Overdue notification sent for loan {loan_id}"

    except Loan.DoesNotExist:
        return f"Loan {loan_id} does not exist"




@shared_task
def check_overdue_loans():
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=date.today()).select_related('book', 'member__user')

    notifications_sent = 0

    for loan in overdue_loans:
        send_overdue_notification(loan.id)
        nonfictions_sent += 1

    return f"Checked Overdue loans. Sent {nonfictions_sent} notifications"





