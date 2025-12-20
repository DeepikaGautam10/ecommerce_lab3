
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import role_required, permission_required
from .models import Product, Category, Cart, CartItem
from .forms import ProductForm, CategoryForm

# Public Views
def home_view(request):
    featured_products = Product.objects.filter(featured=True)[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)

def shop_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'products/shop.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

# Cart Views
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'products/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('products:cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('products:cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('products:cart')

# Admin Views - Category CRUD
@login_required
@role_required(['admin'])
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
@role_required(['admin'])
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('products:category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Create'})

@login_required
@role_required(['admin'])
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'form': form, 'action': 'Update'})

@login_required
@role_required(['admin'])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {'category': category})

# Admin Views - Product CRUD
@login_required
@role_required(['admin'])
def product_list_admin(request):
    products = Product.objects.all()
    return render(request, 'products/product_list_admin.html', {'products': products})

@login_required
@role_required(['admin'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('products:product_list_admin')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})

@login_required
@role_required(['admin'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:product_list_admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})

@login_required
@role_required(['admin'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:product_list_admin')
    return render(request, 'products/product_confirm_delete.html', {'product': product})