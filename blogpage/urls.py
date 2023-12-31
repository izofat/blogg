from django.contrib import admin
from django.urls import path , include
from django.contrib.auth.views import LoginView

from users import views as usersView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('blog.urls')),
    path('login/' , LoginView.as_view(template_name= 'users/login.html') , name='login' ),
    path('logout_user/' , usersView.logout_user , name='logout_user'),
    path('logout_view/' , usersView.logout_view , name='logout_view') ,
    path('register/' , usersView.register_user , name='register'),
    path('profile/' , usersView.profile  , name='profile'),
    path('resetpassword/' , usersView.reset_password , name='reset-password')
]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)