from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Loop, Like, Comment
from .forms import LoopForm, CommentForm

def loops_list(request):
    # Get all loops
    loops_list = Loop.objects.all()
    
    # Filtering
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Apply filters
    if category and category != 'all':
        loops_list = loops_list.filter(category=category)
    
    if difficulty and difficulty != 'all':
        loops_list = loops_list.filter(difficulty=difficulty)
    
    if search_query:
        loops_list = loops_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Apply sorting
    valid_sort_fields = ['-created_at', 'created_at', '-views', '-likes_count']
    if sort_by in valid_sort_fields:
        loops_list = loops_list.order_by(sort_by)
    
    # Add likes count annotation
    loops_list = loops_list.annotate(likes_count=Count('likes'))
    
    # Pagination
    paginator = Paginator(loops_list, 12)  # Show 12 loops per page
    page_number = request.GET.get('page')
    loops = paginator.get_page(page_number)
    
    context = {
        'loops': loops,
        'categories': Loop.CATEGORY_CHOICES,
        'difficulties': Loop.DIFFICULTY_CHOICES,
        'current_category': category,
        'current_difficulty': difficulty,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_loops': loops_list.count(),
    }
    return render(request, 'loops/loops_list.html', context)


def loop_detail(request, pk):
    loop = get_object_or_404(Loop, pk=pk)
    
    # Increment view count
    loop.increment_views()
    
    # Check if user has liked this loop
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, loop=loop).exists()
    
    # Get comments for this loop
    comments = loop.comments.all()
    
    # Handle comment submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to comment.')
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.loop = loop
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('loop_detail', pk=pk)
    else:
        form = CommentForm()
    
    # Get similar loops (same category)
    similar_loops = Loop.objects.filter(
        category=loop.category
    ).exclude(pk=pk)[:4]
    
    context = {
        'loop': loop,
        'is_liked': is_liked,
        'comments': comments,
        'form': form,
        'similar_loops': similar_loops,
        'likes_count': loop.likes.count(),
        'comments_count': comments.count(),
    }
    return render(request, 'loops/loop_detail.html', context)


@login_required
def create_loop(request):
    if request.method == 'POST':
        form = LoopForm(request.POST, request.FILES)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.creator = request.user
            
            # If it's not premium, ensure price is 0
            if not loop.is_premium:
                loop.price = 0
            
            loop.save()
            messages.success(request, 'Your loop has been created successfully!')
            return redirect('loop_detail', pk=loop.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoopForm()
    
    context = {'form': form}
    return render(request, 'loops/create_loop.html', context)


@login_required
def edit_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)
    
    # Check if user is the creator
    if loop.creator != request.user:
        messages.error(request, 'You can only edit loops you created.')
        return redirect('loop_detail', pk=pk)
    
    if request.method == 'POST':
        form = LoopForm(request.POST, request.FILES, instance=loop)
        if form.is_valid():
            loop = form.save(commit=False)
            
            # If it's not premium, ensure price is 0
            if not loop.is_premium:
                loop.price = 0
            
            loop.save()
            messages.success(request, 'Loop updated successfully!')
            return redirect('loop_detail', pk=pk)
    else:
        form = LoopForm(instance=loop)
    
    context = {'form': form, 'loop': loop}
    return render(request, 'loops/edit_loop.html', context)


@login_required
def delete_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)
    
    if loop.creator != request.user:
        messages.error(request, 'You can only delete loops you created.')
        return redirect('loop_detail', pk=pk)
    
    if request.method == 'POST':
        loop.delete()
        messages.success(request, 'Loop deleted successfully!')
        return redirect('loops_list')
    
    return render(request, 'loops/delete_loop.html', {'loop': loop})


@login_required
def like_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)
    
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(
            user=request.user,
            loop=loop
        )
        
        if not created:
            like.delete()
            action = 'unliked'
        else:
            action = 'liked'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'action': action,
                'likes_count': loop.likes.count()
            })
        
        messages.info(request, f'You {action} this loop.')
    
    return redirect('loop_detail', pk=pk)


@login_required
def my_loops(request):
    loops = Loop.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'loops/my_loops.html', {'loops': loops})


def category_view(request, category):
    loops = Loop.objects.filter(category=category).order_by('-created_at')
    context = {
        'loops': loops,
        'category': category,
        'category_name': dict(Loop.CATEGORY_CHOICES).get(category, category),
    }
    return render(request, 'loops/category.html', context)