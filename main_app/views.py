from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor, Event, Image
from .forms import EventForm, CustomSignUpForm
import uuid
import boto3
import os

def about(request):
    return render(request, "about.html")


def events_index(request):
    # events = Event.objects.filter(user=request.user) ; will user later
    events = Event.objects.all()
    return render(request, "events/index.html", {"events": events})


@login_required
def user_events(request):
    # Check if the user is a vendor
    try:
        vendor = Vendor.objects.get(user=request.user)
        # If the user is a vendor, redirect to the vendor's events page
        return redirect("vendor_events")  # Assuming 'vendor_events' is the URL for vendor events view
    except Vendor.DoesNotExist:
        # If the user is not a vendor, show events for non-vendors
        events = Event.objects.filter(vendor=None)  # Filter events for users who are not vendors
        saved_events = request.user.saved_events.all()  # Assuming 'saved_events' is a related field on User model
        return render(request, "user-events.html", {
            "events": events,
            "saved_events": saved_events
        })

@login_required
def save_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event in request.user.saved_events.all():
        # Unsave the event
        request.user.saved_events.remove(event)
    else:
        # Save the event
        request.user.saved_events.add(event)

    return redirect('user-events')  # Redirect to the user-events page

# View for vendors
@login_required
def vendor_events(request):
    try:
        # Get the vendor profile of the logged-in user
        vendor = Vendor.objects.get(user=request.user)
        # Fetch events related to the vendor
        events = Event.objects.filter(vendor=vendor)
        return render(
            request, "vendor-events.html", {"events": events, "vendor": vendor}
        )
    except Vendor.DoesNotExist:
        # In case the user is not a vendor, redirect to the general user events page or show an error
        return redirect("user_events")


@login_required
def items(request):
    items = Item.objects.all()
    return render(request, "items/index.html", {"items": items})


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    event_form = EventForm()
    vendor = None
    if request.user.is_authenticated:
        vendor = Vendor.objects.filter(user=request.user).first()
    return render(
        request,
        "events/detail.html",
        {
            "event": event,
            "event_form": event_form,
            "vendor": vendor
        },
    )
    
@login_required
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)

            try:
                vendor = Vendor.objects.get(user=request.user)
                new_event.vendor = vendor
                new_event.save()
                return redirect("vendor-events")
            except Vendor.DoesNotExist:
                return render(
                    request,
                    "events/event_form.html",
                    {"form": form, "error": "Only vendors can create events."},
                )
    else:
        form = EventForm()
        vendor = Vendor.objects.filter(user=request.user).first()

    return render(request, "events/event_form.html", {"form": form, "vendor": vendor})


def signup(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # or wherever you'd like to redirect after signup
        else:
            # Optional: Print form errors for debugging
            print(form.errors)
    else:
        form = CustomSignUpForm()

    return render(request, "signup.html", {"form": form})


@login_required
def post_login_redirect(request):
    try:
        # If the user is a vendor, send them to the vendor dashboard
        vendor = Vendor.objects.get(user=request.user)
        return redirect("vendor-events")
    except Vendor.DoesNotExist:
        # Otherwise, send them to the regular user view
        return redirect("user-events")


def add_image(request, event_id):
    image_file = request.FILES.get('image-file', None)
    if image_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
        
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            
            Image.objects.create(url=url, event_id=event_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect("event-detail", event_id=event_id)

class Home(LoginView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()

        if self.request.user.is_authenticated:
            try:
                context['vendor'] = Vendor.objects.get(user=self.request.user)
            except Vendor.DoesNotExist:
                context['vendor'] = None
        else:
            context['vendor'] = None

        return context


class Login(LoginView):
    template_name = "login.html"

class EventUpdate(UpdateView):
    model = Event
    fields = "__all__"

    def get_success_url(self):
        return reverse("vendor-events")


class EventDelete(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse("vendor-events")
