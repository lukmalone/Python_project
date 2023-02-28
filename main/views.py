from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Category, Product, Order, Favorite, ProductReview
from .forms import ProductReviewForm, UserUpdateForm, ProfileUpdateForm
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .serializers import ProductReviewSerializer

# def search(request):
#     query = request.GET.get('query')
#     search_results = Product.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query))
#     return render(request, 'search.html', {'products': search_results, 'query': query})

def search(request):
    query = request.GET.get('q')
    categories = Category.objects.filter(name__icontains=query)
    products = Product.objects.filter(title__icontains=query)
    context = {'categories': categories, 'products': products, 'query': query}
    return render(request, 'search_results.html', context)


def index(request):
    product_count = Product.objects.all().count()
    # available_instances_available = Instance.objects.filter(status='av').count()
    category_count = Category.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'product_count': product_count,
        'category_count': category_count,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        review = ProductReview()
        review.product = product
        review.user = request.user
        review.text = request.POST['text']
        review.save()
    return render(request, 'product_list.html', {'product': product})


def brands(request):
    paginator = Paginator(Category.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_brands = paginator.get_page(page_number)
    context = {
        'brands': paged_brands
    } 
    return render(request, 'brands.html', context=context)   


def brand(request, brand_id):
    brand = get_object_or_404(Category, pk=brand_id)
    context = {
        'brand': brand
    }
    return render(request, 'brand.html', context=context)


def products(request):
    products=Product.objects.all()
    data = {
        'products': products
    }
    return render(request, 'product_list.html', data)


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 2
    template_name = 'product_list.html'
    ordering = ['-created_by']
    # queryset = Product.objects.filter(title='Title 1')
 
    # def get_queryset(self):
    #     return Product.objects.filter(title='Title 1')    
    
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     context['data'] = 'random text'
    #     return context


class ProductDetailView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    paginate_by = 3
    form_class = ProductReviewForm
    ordering = ['-created_by']

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.product = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(ProductDetailView, self).form_valid(form)

def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite(user=request.user, product=product, image_url=product.image)
    favorite.save()
    return redirect('product_detail', product_id=product.id)

def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    context = {'favorites': favorites}
    return render(request, 'favorites.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    return render(request, 'favorites.html', {'product': product, 'is_favorite': is_favorite})

def product_detail_view(request, pk):
    product = Product.objects.get(pk=pk)
    category = product.category
    context = {'product': product, 'category': category}
    return render(request, 'product_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category_list.html', context)

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category_detail.html', context)

class ProductCreateView(CreateView):
    model = Product
    fields = ['title', 'description', 'price']
    success_url = reverse_lazy('product_list')


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with this email {email} is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')


class ReviewListApi(generics.ListAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


@login_required
def view_profile(request):
    try:
        profile = request.user.profile
    except profile.DoesNotExist:
        profile = None
    return render(request, 'profile.html', {'profile': profile})