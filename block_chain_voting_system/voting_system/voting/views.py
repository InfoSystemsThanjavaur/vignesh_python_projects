from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
# PDF Libraries
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Model Imports
from .models import Candidate, VoteBlock, ElectionSettings

def home(request):
    return render(request, 'voting/index.html')

def about(request):
    return render(request, 'voting/about.html')

@login_required(login_url='login')
def vote(request):
    settings = ElectionSettings.objects.first()
    now = timezone.now()

    # 1. Check Election Schedule
    if settings:
        if now < settings.start_time:
            messages.warning(request, "Election has not started yet!")
            return redirect('home')
        if now > settings.end_time:
            messages.error(request, "Election has ended!")
            return redirect('results')

    # 2. Prevent Duplicate Voting
    if VoteBlock.objects.filter(voter_id=request.user.id).exists():
        messages.error(request, "You have already cast your vote!")
        return redirect('results')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        if not candidate_id:
            messages.error(request, "Please select a candidate!")
            return redirect('vote')

        # 3. Blockchain Logic: Create Block
        last_block = VoteBlock.objects.all().order_by('-id').first()
        prev_hash = last_block.block_hash if last_block else "0" * 64

        new_vote = VoteBlock(
            prev_hash=prev_hash,
            voter_id=request.user.id,
            candidate_id=candidate_id
        )
        new_vote.save()

        # 4. Increment Candidate Count
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.votes_count += 1
        candidate.save()

        messages.success(request, "Vote recorded successfully on the Blockchain!")
        return redirect('results')

    candidates = Candidate.objects.all()
    return render(request, 'voting/vote.html', {'candidates': candidates})

def results(request):
    blockchain = VoteBlock.objects.all().order_by('id')
    candidates = Candidate.objects.all()
    
    chart_data = []
    for c in candidates:
        actual_votes = VoteBlock.objects.filter(candidate_id=c.id).count()
        chart_data.append({'name': c.name, 'count': actual_votes})

    # Tampering Detection
    is_valid = True
    tampered_id = None
    if blockchain.exists():
        for i in range(1, len(blockchain)):
            if blockchain[i].prev_hash != blockchain[i-1].block_hash:
                is_valid = False
                tampered_id = blockchain[i].id
                break
    
    return render(request, 'voting/results.html', {
        'chart_data': chart_data,
        'blockchain': blockchain,
        'is_valid': is_valid,
        'tampered_id': tampered_id
    })
def register_view(request):
    if request.method == 'POST':
        # 1. ஃபார்ம் டேட்டாவை வாங்குதல்
        un = request.POST.get('username')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        dob_str = request.POST.get('dob')

        # 2. வயது சரிபார்ப்பு (Server-side Check)
        if dob_str:
            birth_date = date.fromisoformat(dob_str)
            age = (date.today() - birth_date).days // 365
            if age < 18:
                messages.error(request, "Ineligible: You must be 18+ to register.")
                return redirect('register')

        # 3. யூசர் ஏற்கனவே இருக்கிறாரா என்று பார்த்தல்
        if User.objects.filter(username=un).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        # 4. முக்கியமானது: பாஸ்வர்டை ஹேஷ் செய்து சேமித்தல் (Hashing)
        user = User.objects.create_user(username=un, email=em, password=ps)
        user.save()
        
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'voting/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('vote')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'voting/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')

def download_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Election_Report.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Official Election Audit Report</b>", styles['Title']))
    
    data = [['Candidate', 'Party', 'Verified Votes']]
    for c in Candidate.objects.all():
        actual_count = VoteBlock.objects.filter(candidate_id=c.id).count()
        data.append([c.name, c.party, str(actual_count)])

    t = Table(data, colWidths=[200, 150, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t)
    doc.build(elements)
    return response