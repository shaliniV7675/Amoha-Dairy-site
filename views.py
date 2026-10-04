import json
import re
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import User, Order


# ─────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'}, status=400)

    full_name        = data.get('full_name', '').strip()
    phone            = data.get('phone', '').strip()
    email            = data.get('email', '').strip().lower()
    password         = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

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

    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'An account with this email already exists.'}, status=409)

    User.objects.create(full_name=full_name, phone=phone, email=email, password=password)

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
            },
        })
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=401)


# ─────────────────────────────────────────────
#  ORDERS
# ─────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def place_order(request):
    """
    Called from payment.html after the user confirms payment.
    Body JSON: { user_id, cart, shipping, payment_method }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'}, status=400)

    user_id        = data.get('user_id')
    cart           = data.get('cart', [])
    shipping       = data.get('shipping', {})
    payment_method = data.get('payment_method', 'unknown')

    if not user_id:
        return JsonResponse({'success': False, 'message': 'User not logged in.'}, status=401)

    if not cart:
        return JsonResponse({'success': False, 'message': 'Cart is empty.'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)

    # Calculate totals (mirror the JS logic in payment.html)
    def price_int(p):
        try:
            return int(str(p).replace('₹', '').replace(',', '').strip())
        except (ValueError, TypeError):
            return 0

    items_total  = sum(price_int(item.get('price', 0)) * int(item.get('qty', 1)) for item in cart)
    delivery_fee = 30 if 0 < items_total < 200 else 0
    discount     = int(items_total * 0.05) if items_total > 500 else 0
    grand_total  = items_total + delivery_fee - discount

    # Generate unique order ID
    order_id = 'AM' + str(int(time.time() * 1000))[-8:].upper()

    order = Order.objects.create(
        user           = user,
        order_id       = order_id,
        items          = cart,
        shipping       = shipping,
        payment_method = payment_method,
        items_total    = items_total,
        delivery_fee   = delivery_fee,
        discount       = discount,
        grand_total    = grand_total,
        status         = 'pending',
    )

    return JsonResponse({
        'success':  True,
        'message':  'Order placed successfully!',
        'order_id': order.order_id,
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_orders(request):
    """
    Returns all orders for the logged-in user.
    Query param: ?user_id=<id>
    """
    user_id = request.GET.get('user_id')

    if not user_id:
        return JsonResponse({'success': False, 'message': 'user_id is required.'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)

    orders = Order.objects.filter(user=user).order_by('-placed_at')

    orders_data = []
    for o in orders:
        orders_data.append({
            'order_id':       o.order_id,
            'items':          o.items,
            'shipping':       o.shipping,
            'payment_method': o.payment_method,
            'items_total':    o.items_total,
            'delivery_fee':   o.delivery_fee,
            'discount':       o.discount,
            'grand_total':    o.grand_total,
            'status':         o.status,
            'placed_at':      o.placed_at.strftime('%d %b %Y, %I:%M %p'),
        })

    return JsonResponse({
        'success':     True,
        'orders':      orders_data,
        'order_count': len(orders_data),
        'user_name':   user.full_name,
    })
