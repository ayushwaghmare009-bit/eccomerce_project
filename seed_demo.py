"""Create demo categories and products (safe to run repeatedly)."""
import shutil
from decimal import Decimal
 
from django.conf import settings
from django.core.management.base import BaseCommand
 
from store.models import Category, Product
 
PRODUCTS = [
    ("Electronics", "electronics", "Apple iPhone Pro", "apple-iphone-pro", "Latest iPhone Pro with an advanced camera system.", "119900.00", "Apple-iPhone-18-Pro-2up-Geo-260909_inline.jpg.large.jpg"),
    ("Electronics", "electronics", "Apple AirPods Pro", "apple-airpods-pro", "Wireless earbuds with active noise cancellation.", "24900.00", "Apple-AirPods-Pro-2nd-gen-hero-220907_big.jpg.large.jpg"),
    ("Electronics", "electronics", "Pro Laptop 16-inch", "pro-laptop-16", "High-performance laptop for work and creativity.", "199900.00", "D1_66a3bdc9-d540-4705-9689-f685a4e66d6f.webp"),
    ("Fashion", "fashion", "Nike Running Shoes", "nike-running-shoes", "Lightweight, comfortable everyday running shoes.", "8995.00", "ad22b92Nike-FD2596-201_1.avif"),
    ("Fashion", "fashion", "Classic Striped Polo", "classic-striped-polo", "Soft knit polo shirt with a classic striped design.", "2499.00", "images.jpg"),
    ("Accessories", "accessories", "Steel Automatic Watch", "steel-automatic-watch", "Stainless steel wristwatch with a colourful dial.", "45000.00", "images_1.jpg"),
]
 
 
class Command(BaseCommand):
    help = "Seed demo products so the shop is not empty after a fresh deploy"
 
    def handle(self, *args, **options):
        src_dir = settings.BASE_DIR / "products"
        dst_dir = settings.MEDIA_ROOT / "products"
        dst_dir.mkdir(parents=True, exist_ok=True)
        created = 0
        for cat, cat_slug, title, slug, desc, price, img in PRODUCTS:
            category, _ = Category.objects.get_or_create(slug=cat_slug, defaults={"name": cat})
            src = src_dir / img
            if src.exists():
                shutil.copy(src, dst_dir / img)
            _, was_created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "category": category, "title": title, "description": desc,
                    "price": Decimal(price), "stock": 25, "is_available": True,
                    "image": f"products/{img}",
                },
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"Seed complete ({created} new products)"))
