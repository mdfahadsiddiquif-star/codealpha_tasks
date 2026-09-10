def cart_item_count(request):
    """Makes {{ cart_item_count }} available in every template for the navbar badge."""
    from .views import get_cart

    try:
        cart = get_cart(request)
        count = cart.total_items
    except Exception:
        count = 0
    return {'cart_item_count': count}
