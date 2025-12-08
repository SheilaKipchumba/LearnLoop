from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Loop, Like, Comment
from payments.models import Payment     
from .forms import LoopForm, CommentForm


def loops_list(request):
    loops_list = Loop.objects.all()

    # Filtering
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')

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

    valid_sort_fields = ['-created_at', 'created_at', '-views', '-likes_count']
    if sort_by in valid_sort_fields:
        loops_list = loops_list.order_by(sort_by)

    loops_list = loops_list.annotate(likes_count=Count('likes'))

    paginator = Paginator(loops_list, 12)
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


def _user_has_access(user, loop):
    """Check if user purchased a premium loop."""
    if not loop.is_premium:
        return True
    if not user.is_authenticated:
        return False
    return Payment.objects.filter(user=user, loop=loop, status="COMPLETED").exists()


def loop_detail(request, pk):
    loop = get_object_or_404(Loop, pk=pk)

    # views
    loop.increment_views()

    # like status
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, loop=loop).exists()

    # USER ACCESS
    has_access = _user_has_access(request.user, loop)

    # Comments
    comments = loop.comments.all()

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
            messages.success(request, 'Comment added.')
            return redirect('loop_detail', pk=pk)
    else:
        form = CommentForm()

    similar_loops = Loop.objects.filter(category=loop.category).exclude(pk=pk)[:4]

    context = {
        'loop': loop,
        'has_access': has_access,
        'is_liked': is_liked,
        'comments': comments,
        'form': form,
        'similar_loops': similar_loops,
        'likes_count': loop.likes.count(),
        'comments_count': comments.count(),
    }
    return render(request, 'loops/loop_detail.html', context)


@login_required
def purchase_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)

    if not loop.is_premium:
        messages.info(request, "This loop is free.")
        return redirect('loop_detail', pk=pk)

    # check if already purchased
    if Payment.objects.filter(user=request.user, loop=loop, status="COMPLETED").exists():
        messages.success(request, "You already bought this loop.")
        return redirect('loop_detail', pk=pk)

    # Create a pending payment record
    payment = Payment.objects.create(
        user=request.user,
        loop=loop,
        amount=loop.price,
        status="PENDING",
    )

    return redirect('initiate_payment', payment_id=payment.id)


@login_required
def create_loop(request):
    if request.method == 'POST':
        form = LoopForm(request.POST, request.FILES)
        if form.is_valid():
            loop = form.save(commit=False)
            loop.creator = request.user

            if not loop.is_premium:
                loop.price = 0

            loop.save()
            messages.success(request, 'Loop created!')
            return redirect('loop_detail', pk=loop.pk)
        else:
            messages.error(request, 'Fix the errors.')
    else:
        form = LoopForm()

    return render(request, 'loops/create_loop.html', {'form': form})


@login_required
def edit_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)

    if loop.creator != request.user:
        messages.error(request, 'You can only edit your own loops.')
        return redirect('loop_detail', pk=pk)

    if request.method == 'POST':
        form = LoopForm(request.POST, request.FILES, instance=loop)
        if form.is_valid():
            loop = form.save(commit=False)
            if not loop.is_premium:
                loop.price = 0
            loop.save()
            messages.success(request, 'Updated.')
            return redirect('loop_detail', pk=pk)
    else:
        form = LoopForm(instance=loop)

    return render(request, 'loops/edit_loop.html', {'form': form, 'loop': loop})


@login_required
def delete_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)

    if loop.creator != request.user:
        messages.error(request, 'Not allowed.')
        return redirect('loop_detail', pk=pk)

    if request.method == 'POST':
        loop.delete()
        messages.success(request, 'Deleted.')
        return redirect('loops_list')

    return render(request, 'loops/delete_loop.html', {'loop': loop})


@login_required
def like_loop(request, pk):
    loop = get_object_or_404(Loop, pk=pk)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, loop=loop)

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

        messages.info(request, f"You {action} this loop.")

    return redirect('loop_detail', pk=pk)


@login_required
def my_loops(request):
    loops = Loop.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'loops/my_loops.html', {'loops': loops})


def category_view(request, category):
    loops = Loop.objects.filter(category=category).order_by('-created_at')
    return render(request, 'loops/category.html', {
        'loops': loops,
        'category': category,
        'category_name': dict(Loop.CATEGORY_CHOICES).get(category, category),
    })
