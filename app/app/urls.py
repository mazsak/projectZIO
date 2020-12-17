"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from workflows import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('workflows', views.workflows_view, name='workflows'),
    path('workflows/<int:id>', views.workflow_view, name='workflow'),
    path('account', views.account_view, name='account'),
    path('create_workflow', views.update_create_workflow_view, name='create_workflow'),
    path('create_task', views.update_create_task_view, name='create_task'),
    path('logout', views.logout_view, name='logout'),
    path('workflows/start/<int:id>', views.workflow_start_view, name='workflow_start_view'),
    path('workflows/status', views.workflow_status_view, name='workflow_status_view'),
    path('workflows/update', views.workflow_update_view, name='workflow_update_view'),
    path('czarymary/hokus/pokus/json/mendoza/zrob/endpointa/<int:id>', views.workflow_stop_view, name='workflow_stop_view'),
    path('workflows/log/<str:file>', views.workflow_log_view, name='workflow_log_view'),
    path('admin/', admin.site.urls),
    path('admin/file', views.admin_file_view, name='admin_file_view'),
]
