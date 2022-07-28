from ast import Pass
from http.client import HTTPResponse
import numbers
from unittest.mock import patch
from django.shortcuts import render
from .models import Stageir,gestion
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import send_mail
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import random,os
from datetime import date

def form(request):
    context = {}
    if request.method=='POST':
        nom = request.POST['nom']
        prenoma = request.POST['prenom']
        debutstages = request.POST['debutstage']
        finstages = request.POST['finstage']
        emails = request.POST['email']
        domaine = request.POST['domaine']
        sexee = request.POST['sexe']
        CV = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(CV.name, CV)
        context['url'] = fs.url(name)
        a=Stageir(name=nom,prenom=prenoma,email=emails,service=domaine,debutstage=debutstages,fintage=finstages,sexe=sexee,cv=CV.name,statu="")
        a.save()
        response = redirect('/gestion/')
        return response
    return render(request,"index.html")



def logout(request):
    del request.session['admin']
    return redirect('/gestion/login')




def list(request):
    if  'admin' in request.session:
        context = {'stagier_list': Stageir.objects.filter(statu='').values(),"number":Stageir.objects.filter(statu='').count(),"numberA":Stageir.objects.filter(statu='accept').count(),"numberB":Stageir.objects.filter(statu='stage').count()}
        
        return render(request,"list.html",context)
    return render(request,"error.html")




def list_accept(request):
    if  'admin' in request.session:
        context = {'stagier_list': Stageir.objects.filter(statu='accept').values(),"number":Stageir.objects.filter(statu='accept').count()}
        
        return render(request,"accept.html",context)
    return render(request,"error.html")
 
  


def login(request):
    if  'admin' in request.session:
            return redirect('/gestion/list')


    if request.method=='POST':
        if request.POST['user'] == "root" and  request.POST['pass']=="123":
            request.session['admin']="kayn"

            response = redirect('/gestion/list/')
            return response
    return render(request,"login.html")

def ckeck(request,id):
    if  'admin' in request.session:
        context = {'x':Stageir.objects.filter(pk=id)[0]}
        return render(request,"check.html",context)
    return render(request,"error.html")

def stagier_delete(request,id):
    if  'admin' in request.session:
        stagier = Stageir.objects.get(pk=id)
        os.remove(f"C:\\Users\\hp\\Desktop\\tp\\media\\{stagier.cv}")
        stagier.delete()
        return redirect('/gestion/list')
    return render(request,"error.html")



def return_to_list(request,id):
    if  'admin' in request.session:
        context = Stageir.objects.filter(pk=id)[0]
        x=Stageir.objects.get(pk=id)
        x.statu=""
        x.save()        
        return redirect('/gestion/list/')
    return render(request,"error.html")



def return_to_listA(request,id):
    if  'admin' in request.session:
        context = Stageir.objects.filter(pk=id)[0]
        x=Stageir.objects.get(pk=id)
        x.statu=""
        x.save()        
        return redirect('/gestion/list/')
    return render(request,"error.html")



def evaluation(request,id):
    if  'admin' in request.session:
        context = {'stagier': gestion.objects.filter(number=id)[0],"date":date.today()}   
        return render(request,"evaluation.html",context)
    return render(request,"error.html")



def evaluation_update(request,id):
    if  'admin' in request.session:
        nameMaître =request.POST['Maître']
        Assiduité=request.POST['Assiduité']
        Adresse=request.POST['Adresse']
        Initiative=request.POST['Initiative']
        Communication=request.POST['Communication']
        Esprit =request.POST['Esprit']
        Connaissances =request.POST['Connaissances']
        Total =float(Assiduité)+float(Initiative)+float(Communication)+float(Esprit)+float(Connaissances)
        Observations=request.POST['Observations']
        print(Observations)
        P = gestion.objects.get(pk=id)
        P.nameMaître=nameMaître
        P.Assiduité=Assiduité
        P.Adresse=Adresse
        P.Initiative=Initiative
        P.Communication=Communication
        P.Esprit=Esprit
        P.Connaissances=Connaissances
        P.Total=Total
        P.Observations=Observations
        P.save()
        return redirect(f'/gestion/evaluation/{P.number}/')
     
    return render(request,"error.html")





def accept(request,id):
    if  'admin' in request.session:
        context = Stageir.objects.filter(pk=id)[0]
        x=Stageir.objects.get(pk=id)
        x.statu="accept"
        x.save()        
        return redirect('/gestion/list/')
    return render(request,"error.html")




def send(email,name,debutstage):
    subject = "Votre demande est acceptée"  
    msg     = f"cher {name} Votre demande est acceptée,Vous pouvez commencer avec nous dans {debutstage}"  
    to      = email
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        print("Mail Sent Successfully."  )
    else:  
        msg = "Mail Sending Failed." 





def send_all(request):
    if  'admin' in request.session:
        context ={"hello":Stageir.objects.filter(statu='accept').values()}
        for i in context['hello']:
            send(i["email"],i['name'],i['debutstage']) 
        return redirect('/gestion/listA/')
    return render(request,"error.html")







def debut(request):
    if  'admin' in request.session:
        context ={"hello":Stageir.objects.filter(statu='accept').values()}
        for i in context['hello']:
            P = Stageir.objects.get(pk=i['id'])
            nam=P.prenom+" "+P.name
            date=str(P.debutstage)+">"+str(P.fintage)
            w=gestion(name=nam,number=P.id,Option=P.service,Période=date)
            P.statu="stage" 
            w.save()
            P.save()
        return redirect('/gestion/tracker/')







def tracker(request):
    if  'admin' in request.session:
        context ={"stagier_list":Stageir.objects.filter(statu='stage').values()}
        return render(request,"tracker.html",context)
    return render(request,"error.html")




def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1","ignore")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None




context = {'stagier_list': Stageir.objects.filter(statu='accept').values()}
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('invoice.html', context)
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "listdeStagiaires_%s.pdf" %(random.randint(1000, 9999))
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

def get(request,idd):
	pdf = render_to_pdf('invoice1.html', {'stagier': gestion.objects.filter(pk=idd)[0],"date":date.today()}   )
	response = HttpResponse(pdf, content_type='application/pdf')
	filename = "listdeStagiaires_%s.pdf" %(random.randint(1000, 9999))
	content = "attachment; filename='%s'" %(filename)
	response['Content-Disposition'] = content
	return response
def get2(request,idd):
	pdf = render_to_pdf('attestation.html', {'stagier': gestion.objects.filter(number=idd)[0],"date":date.today()}   )
	response = HttpResponse(pdf, content_type='application/pdf')
	filename = "listdeStagiaires_%s.pdf" %(random.randint(1000, 9999))
	content = "attachment; filename='%s'" %(filename)
	response['Content-Disposition'] = content
	return response