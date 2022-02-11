from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from webpage import views as web_views

admin.site.site_header = "Event Management System"
admin.site.site_title = "Admin"
admin.site.index_title = "Fest Bengaluru"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-page/',web_views.admin_page,name='admin-page'),
    path('download/',web_views.download_file,name='download'),
    path('',web_views.home,name='webpage-home'),
    path('college/',web_views.college,name='college'),
    path('fest/<str:type>',web_views.fest,name='fest'),
    path('fest/<value>/',web_views.fest_clg,name='fest-clg'),
    path('event/',web_views.event,name='event'),
    path('event/<value>/',web_views.event_fest,name='event-fest'),
    path('my-events/',web_views.my_events,name='my-events'),
    path('update-event/<int:user_id>/<int:event_id>/',web_views.update_participation,name='update-participation'),
    path('register/',web_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='webpage/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='webpage/logout.html'),name='logout')
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)