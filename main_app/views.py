from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, Collection, Category, Vendor, Event, SavedEvents, Address, Posts, Follows
from .forms import ItemForm, EventForm
 
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def collections_index(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'collections/index.html', {'collections': collections})

def events_index(request):
    # events = Event.objects.filter(user=request.user) ; will user later
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

@login_required
def items(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items': items})

def category(request):
    categories = Collection.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})

@login_required
def collection_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    item_form = ItemForm()
    return render(request, 'collections/detail.html', {
        'collection': collection,
        'item_form': item_form
    })
    
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    event_form=EventForm()
    return render(request, 'events/detail.html', {
        'event': event,
        'event_form': event_form
    })
    
@login_required   
def add_item(request, collection_id):
    form = ItemForm(request.POST)
    
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.collection_id = collection_id
        new_item.save()
        
    return redirect('collection-detail', collection_id=collection_id)

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            
            new_event.vendor = request.user.vendor  
            
            new_event.save()
            return redirect('events-index')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form})

@login_required
def update_item(request, collection_id):
    form = ItemForm(request.UPDATE)
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('collections-index')
        else:
            error_message = 'Invalid sign up - try again'
    
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    
class Home(LoginView):
    template_name = 'home.html'

class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['name', 'description']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = ['description']
    
class CollectionDelete(LoginRequiredMixin, DeleteView):
    model = Collection
    success_url = '/collections/'
    
class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('collection-detail', args=[self.object.collection.id])

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    
    def get_success_url(self):
        return reverse('collection-detail', args=[self.object.collection.id])
    
class EventUpdate(UpdateView):
    model = Event
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('event-detail', args=[self.object.id])
    
class EventDelete(DeleteView):
    model = Event
    
    def get_success_url(self):
        return reverse('events-index')