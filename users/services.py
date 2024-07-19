import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """Создаем продукт в страйпев страйпе"""

    title_product = (
        f"{instance.paid_course}" if instance.paid_course else instance.paid_lesson
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_stripe_price(amount, product_id):
    """Создаст цену в страйпе"""

    return stripe.Price.create(
        currency="rub", unit_amount=amount * 100, product_data={"name": product_id}
    )


def create_stripe_session(price):
    """Создаст сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
