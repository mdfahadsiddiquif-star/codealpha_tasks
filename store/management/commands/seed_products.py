from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Category, Product


SAMPLE_DATA = {
    'Electronics': [
        ('Wireless Headphones', 59.99, 'Over-ear Bluetooth headphones with noise cancellation.'),
        ('Smartwatch', 89.99, 'Fitness tracking smartwatch with heart-rate monitor.'),
        ('Portable Speaker', 34.99, 'Compact waterproof Bluetooth speaker.'),
    ],
    'Clothing': [
        ('Classic T-Shirt', 14.99, '100% cotton crew-neck t-shirt.'),
        ('Denim Jacket', 49.99, 'Unisex denim jacket, regular fit.'),
        ('Running Shoes', 64.99, 'Lightweight running shoes with cushioned sole.'),
    ],
    'Home & Kitchen': [
        ('Ceramic Mug Set', 19.99, 'Set of 4 ceramic mugs, dishwasher safe.'),
        ('Non-Stick Pan', 27.99, '10-inch non-stick frying pan.'),
        ('LED Desk Lamp', 22.99, 'Adjustable LED desk lamp with 3 brightness levels.'),
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        created_products = 0
        for category_name, products in SAMPLE_DATA.items():
            category, _ = Category.objects.get_or_create(
                name=category_name, defaults={'slug': slugify(category_name)}
            )
            for name, price, description in products:
                _, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'slug': slugify(name),
                        'category': category,
                        'price': price,
                        'description': description,
                        'stock': 25,
                    },
                )
                if created:
                    created_products += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_products} products.'))
