import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import User


@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'}, status=400)

    full_name       = data.get('full_name', '').strip()
    phone           = data.get('phone', '').strip()
    email           = data.get('email', '').strip().lower()
    password        = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    # ── Validation ──
    if not all([full_name, phone, email, password, confirm_password]):
        return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

    if not re.match(r'^\d{10}$', phone):
        return JsonResponse({'success': False, 'message': 'Phone number must be exactly 10 digits.'}, status=400)

    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return JsonResponse({'success': False, 'message': 'Enter a valid email address.'}, status=400)

    if len(password) < 6:
        return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters.'}, status=400)

    if password != confirm_password:
        return JsonResponse({'success': False, 'message': 'Passwords do not match.'}, status=400)

    # ── Duplicate check ──
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'An account with this email already exists.'}, status=409)

    # ── Create user ──
    User.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        password=password   # plain text (no extra packages needed)
    )

    return JsonResponse({'success': True, 'message': 'Account created successfully! Please login.'})


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'}, status=400)

    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return JsonResponse({'success': False, 'message': 'Email and password are required.'}, status=400)

    try:
        user = User.objects.get(email=email, password=password)
        return JsonResponse({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'id':        user.id,
                'full_name': user.full_name,
                'email':     user.email,
                'phone':     user.phone,
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=401)
