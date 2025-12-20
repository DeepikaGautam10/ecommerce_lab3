import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from products.models import Category, Product
from accounts.models import User

def create_sample_data():
    print("Starting data population...")
    
    # Create Categories for Watch House
    categories_data = [
        {
            'name': 'Luxury Watches',
            'slug': 'luxury-watches',
            'description': 'Premium luxury timepieces from top brands',
            'image_path': 'categories/luxury_watches.jpg'  # Edit this path
        },
        {
            'name': 'Smart Watches',
            'slug': 'smart-watches',
            'description': 'Modern smart watches with advanced features',
            'image_path': 'media/categories/smart_watches.jpg'  # Edit this path
        },
        {
            'name': 'Sports Watches',
            'slug': 'sports-watches',
            'description': 'Durable watches for athletes and outdoor enthusiasts',
            'image_path': 'media/categories/sports_watches.jpg'  # Edit this path
        },
        {
            'name': 'Fashion Watches',
            'slug': 'fashion-watches',
            'description': 'Stylish watches for everyday wear',
            'image_path': 'media/categories/fashion_watches.jpg'  # Edit this path
        },
        {
            'name': 'Classic Watches',
            'slug': 'classic-watches',
            'description': 'Timeless classic watch designs',
            'image_path': 'media/categories/classic_watches.jpg'  # Edit this path
        },
        {
            'name': 'Digital Watches',
            'slug': 'digital-watches',
            'description': 'Modern digital timepieces',
            'image_path': 'media/categories/digital_watches.jpg'  # Edit this path
        },
    ]
    
    print("\nCreating categories...")
    for cat_data in categories_data:
        image_path = cat_data.pop('image_path', None)
        
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        
        # Add image if path exists and file is found
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as img_file:
                    category.image.save(
                        os.path.basename(image_path),
                        File(img_file),
                        save=True
                    )
                print(f"✓ Created category: {category.name} (with image)")
            except Exception as e:
                print(f"✓ Created category: {category.name} (image error: {e})")
        else:
            if created:
                print(f"✓ Created category: {category.name} (no image)")
            else:
                print(f"- Category already exists: {category.name}")
    
    # Create Sample Products (Watches)
    print("\nCreating products...")
    
    luxury = Category.objects.get(slug='luxury-watches')
    smart = Category.objects.get(slug='smart-watches')
    sports = Category.objects.get(slug='sports-watches')
    fashion = Category.objects.get(slug='fashion-watches')
    classic = Category.objects.get(slug='classic-watches')
    digital = Category.objects.get(slug='digital-watches')
    
    products_data = [
        # Luxury Watches
        {
            'name': 'Rolex Submariner',
            'slug': 'rolex-submariner',
            'description': 'Iconic luxury diving watch with automatic movement. Water resistant up to 300m. Stainless steel case with black dial and ceramic bezel.',
            'price': 899999.00,
            'stock': 5,
            'category': luxury,
            'featured': True,
            'image_path': 'media/products/rolex_submariner.jpg'  # Edit this path
        },
        {
            'name': 'Omega Speedmaster',
            'slug': 'omega-speedmaster',
            'description': 'Professional chronograph, the first watch worn on the moon. Manual-wind movement with hesalite crystal.',
            'price': 650000.00,
            'stock': 8,
            'category': luxury,
            'featured': True,
            'image_path': 'media/products/omega_speedmaster.jpg'  # Edit this path
        },
        {
            'name': 'Tag Heuer Carrera',
            'slug': 'tag-heuer-carrera',
            'description': 'Racing-inspired chronograph with automatic calibre 16 movement. Sapphire crystal and steel bracelet.',
            'price': 425000.00,
            'stock': 12,
            'category': luxury,
            'featured': False,
            'image_path': 'media/products/tag_heuer_carrera.jpg'  # Edit this path
        },
        
        # Smart Watches
        {
            'name': 'Apple Watch Series 9',
            'slug': 'apple-watch-series-9',
            'description': 'Advanced health features including ECG, blood oxygen, and sleep tracking. Always-on Retina display. GPS + Cellular.',
            'price': 45999.00,
            'stock': 50,
            'category': smart,
            'featured': True,
            'image_path': 'media/products/apple_watch_series_9.jpg'  # Edit this path
        },
        {
            'name': 'Samsung Galaxy Watch 6',
            'slug': 'samsung-galaxy-watch-6',
            'description': 'Premium smartwatch with comprehensive health monitoring. Rotating bezel and Super AMOLED display.',
            'price': 38999.00,
            'stock': 40,
            'category': smart,
            'featured': True,
            'image_path': 'media/products/samsung_galaxy_watch_6.jpg'  # Edit this path
        },
        {
            'name': 'Garmin Forerunner 965',
            'slug': 'garmin-forerunner-965',
            'description': 'Advanced GPS running watch with AMOLED display. Training metrics and multi-band GPS.',
            'price': 52999.00,
            'stock': 25,
            'category': smart,
            'featured': False,
            'image_path': 'media/products/garmin_forerunner_965.jpg'  # Edit this path
        },
        
        # Sports Watches
        {
            'name': 'Casio G-Shock GA-2100',
            'slug': 'casio-g-shock-ga2100',
            'description': 'Shock resistant sports watch with 200m water resistance. Carbon core guard structure.',
            'price': 12999.00,
            'stock': 100,
            'category': sports,
            'featured': True,
            'image_path': 'media/products/casio_gshock_ga2100.jpg'  # Edit this path
        },
        {
            'name': 'Suunto 9 Peak Pro',
            'slug': 'suunto-9-peak-pro',
            'description': 'Ultra-durable GPS sports watch with long battery life. Titanium bezel and sapphire crystal.',
            'price': 64999.00,
            'stock': 20,
            'category': sports,
            'featured': False,
            'image_path': 'media/products/suunto_9_peak_pro.jpg'  # Edit this path
        },
        {
            'name': 'Timex Ironman Classic 30',
            'slug': 'timex-ironman-classic-30',
            'description': 'Digital sports watch with 30-lap memory and INDIGLO night-light. 100m water resistant.',
            'price': 4999.00,
            'stock': 75,
            'category': sports,
            'featured': False,
            'image_path': 'media/products/timex_ironman_classic_30.jpg'  # Edit this path
        },
        
        # Fashion Watches
        {
            'name': 'Daniel Wellington Classic',
            'slug': 'daniel-wellington-classic',
            'description': 'Minimalist watch with interchangeable NATO strap. Stainless steel case with white dial.',
            'price': 14999.00,
            'stock': 60,
            'category': fashion,
            'featured': True,
            'image_path': 'media/products/daniel_wellington_classic.jpg'  # Edit this path
        },
        {
            'name': 'Michael Kors Lexington',
            'slug': 'michael-kors-lexington',
            'description': 'Gold-tone chronograph watch with stylish design. Perfect for dressy occasions.',
            'price': 22999.00,
            'stock': 35,
            'category': fashion,
            'featured': False,
            'image_path': 'media/products/michael_kors_lexington.jpg'  # Edit this path
        },
        {
            'name': 'Fossil Grant Chronograph',
            'slug': 'fossil-grant-chronograph',
            'description': 'Vintage-inspired chronograph with leather strap. Roman numeral markers and blue hands.',
            'price': 16999.00,
            'stock': 45,
            'category': fashion,
            'featured': False,
            'image_path': 'media/products/fossil_grant_chronograph.jpg'  # Edit this path
        },
        
        # Classic Watches
        {
            'name': 'Seiko 5 Automatic',
            'slug': 'seiko-5-automatic',
            'description': 'Reliable automatic movement with day-date display. See-through case back and 100m water resistance.',
            'price': 18999.00,
            'stock': 70,
            'category': classic,
            'featured': True,
            'image_path': 'media/products/seiko_5_automatic.jpg'  # Edit this path
        },
        {
            'name': 'Orient Bambino',
            'slug': 'orient-bambino',
            'description': 'Classic dress watch with domed crystal. Automatic movement and leather strap.',
            'price': 15999.00,
            'stock': 50,
            'category': classic,
            'featured': False,
            'image_path': 'media/products/orient_bambino.jpg'  # Edit this path
        },
        {
            'name': 'Tissot PRX Powermatic 80',
            'slug': 'tissot-prx-powermatic-80',
            'description': 'Integrated bracelet sports watch with 80-hour power reserve. Swiss automatic movement.',
            'price': 67999.00,
            'stock': 30,
            'category': classic,
            'featured': True,
            'image_path': 'media/products/tissot_prx_powermatic_80.jpg'  # Edit this path
        },
        
        # Digital Watches
        {
            'name': 'Casio F-91W',
            'slug': 'casio-f91w',
            'description': 'Iconic digital watch with alarm, stopwatch, and LED light. Ultra-lightweight and water resistant.',
            'price': 1999.00,
            'stock': 200,
            'category': digital,
            'featured': False,
            'image_path': 'media/products/casio_f91w.jpg'  # Edit this path
        },
        {
            'name': 'Casio World Time AE-1200',
            'slug': 'casio-world-time-ae1200',
            'description': 'Digital watch with world time for 31 time zones. 5 alarms and 100m water resistance.',
            'price': 3999.00,
            'stock': 150,
            'category': digital,
            'featured': False,
            'image_path': 'media/products/casio_world_time_ae1200.jpg'  # Edit this path
        },
    ]
    
    for prod_data in products_data:
        image_path = prod_data.pop('image_path', None)
        
        product, created = Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults=prod_data
        )
        
        # Add image if path exists and file is found
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as img_file:
                    product.image.save(
                        os.path.basename(image_path),
                        File(img_file),
                        save=True
                    )
                print(f"✓ Created product: {product.name} - NPR {product.price} (with image)")
            except Exception as e:
                print(f"✓ Created product: {product.name} - NPR {product.price} (image error: {e})")
        else:
            if created:
                print(f"✓ Created product: {product.name} - NPR {product.price} (no image)")
            else:
                print(f"- Product already exists: {product.name}")
    
    print("\n" + "="*60)
    print("Database population completed successfully!")
    print("="*60)
    print(f"\nTotal Categories: {Category.objects.count()}")
    print(f"Total Products: {Product.objects.count()}")
    print(f"Featured Products: {Product.objects.filter(featured=True).count()}")
    print("\nNote: Images will only be added if the file paths are correct.")
    print("Update the 'image_path' values in the script with your actual image paths.")

if __name__ == '__main__':
    create_sample_data()