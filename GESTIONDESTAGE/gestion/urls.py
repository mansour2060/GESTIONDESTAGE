from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.form,name="FORMULAIRE"),
    path('login/', views.login),
    path('list/', views.list),
    path('listA/', views.list_accept),
    path('logout/', views.logout),
    path('sendall/', views.send_all,name="sendall"),
    path('debut/', views.debut,name="debut"),
    path('tracker/', views.tracker,name="tracker"),
    path('Check/<int:id>/', views.ckeck,name='checker'),
    path('<int:id>/', views.form,name='check'), 
    path('accept/<int:id>/', views.accept,name='accept'),
    path('<int:id>/', views.form,name='accept_stagier'), 
    path('return/<int:id>/', views.return_to_list,name='return'),
    path('<int:id>/', views.form,name='return_stagier'), 
    path('<int:id>/', views.form,name='stagier_update'), 
    path('delete/<int:id>/',views.stagier_delete,name='stagier_delete'),
    path('<int:id>/', views.form,name='Ev_update'), 
    path('evaluation/<int:id>/',views.evaluation,name='evaluation'),
    path('evaluation_update/<int:id>/',views.evaluation_update,name='evaluation_update'),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('pdf/<int:idd>/', views.get, name="pdf"),
    path('certificate/<int:idd>/', views.get2, name="certificate"),
    path('<int:idd>/', views.form,name='pdf_P'), 
    path('<int:idd>/', views.form,name='pdf_update'), 

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

