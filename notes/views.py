from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GroupForm, GroupPasswordForm, NoteUploadForm, SignUpForm, SubgroupForm
from .models import Group, Note, Subgroup


class NoteShareLoginView(LoginView):
    template_name = 'notes/login.html'


def signup(request):
    if request.user.is_authenticated:
        return redirect('group_list')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to NoteShare. Your account is ready.')
            return redirect('group_list')
    else:
        form = SignUpForm()

    return render(request, 'notes/signup.html', {'form': form})


@login_required
def group_list(request):
    groups = Group.objects.prefetch_related('members', 'subgroups').all()
    contributions = Note.objects.filter(uploader=request.user).select_related(
        'subgroup',
        'subgroup__group',
    ).order_by('-timestamp')[:5]

    return render(request, 'notes/group_list.html', {
        'groups': groups,
        'contributions': contributions,
    })


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group.objects.prefetch_related('members'), id=group_id)

    if request.user == group.creator or group.members.filter(id=request.user.id).exists():
        subgroups = group.subgroups.prefetch_related('notes__uploader').all()
        return render(request, 'notes/group_detail.html', {
            'group': group,
            'subgroups': subgroups,
        })

    if request.method == 'POST':
        form = GroupPasswordForm(request.POST)
        if form.is_valid() and group.check_password(form.cleaned_data['password']):
            group.members.add(request.user)
            messages.success(request, f'You joined {group.name}.')
            return redirect('group_detail', group_id=group.id)

        messages.error(request, 'Incorrect password. Please try again.')
    else:
        form = GroupPasswordForm()

    return render(request, 'notes/password_form.html', {
        'group': group,
        'form': form,
    })


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.creator = request.user
            new_group.set_password(form.cleaned_data['password'])
            new_group.save()
            new_group.members.add(request.user)
            messages.success(request, f'{new_group.name} is ready.')
            return redirect('group_detail', group_id=new_group.id)
    else:
        form = GroupForm()

    return render(request, 'notes/create_group.html', {'form': form})


@login_required
def create_subgroup(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.creator:
        messages.error(request, 'Only the group creator can add subjects.')
        return redirect('group_detail', group_id=group.id)

    if request.method == 'POST':
        form = SubgroupForm(request.POST)
        if form.is_valid():
            subgroup = form.save(commit=False)
            subgroup.group = group
            subgroup.save()
            messages.success(request, f'{subgroup.name} was added.')
            return redirect('group_detail', group_id=group.id)
    else:
        form = SubgroupForm()

    return render(request, 'notes/create_subgroup.html', {
        'group': group,
        'form': form,
    })


@login_required
def upload_note(request, subgroup_id):
    subgroup = get_object_or_404(Subgroup.objects.select_related('group'), id=subgroup_id)
    group = subgroup.group

    if request.user != group.creator and not group.members.filter(id=request.user.id).exists():
        messages.error(request, 'Join the group before uploading notes.')
        return redirect('group_detail', group_id=group.id)

    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.subgroup = subgroup
            note.uploader = request.user
            note.save()
            messages.success(request, f'{note.title} was uploaded.')
            return redirect('group_detail', group_id=group.id)
    else:
        form = NoteUploadForm()

    return render(request, 'notes/upload_note.html', {
        'subgroup': subgroup,
        'form': form,
    })
