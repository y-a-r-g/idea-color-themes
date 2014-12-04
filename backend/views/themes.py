import random

from django import http
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from backend.forms.UploadThemeForm import UploadThemeForm
from backend.logic.themes.themes import *
from backend.models import ShoppingToken
from backend.views import view
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful
from server import settings
from server.settings import ROOT_URL


__author__ = 'sdvoynikov'

_LANGUAGES = [
    ('Java', 'themes/code-java.html'),
    ('Python', 'themes/code-python.html'),
    ('HTML', 'themes/code-html.html')]


@view(path=r'^themes/?$')
def index(request):
    order = request.GET.get('order', '')
    if not order in ['downloads', 'date']:
        order = 'downloads'

    nameFilter = request.GET.get('filter', '')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    themes, page, pagesCount = get_page(order, nameFilter, page - 1)

    return render(request, 'themes/index.html', {
        'themes': themes,
        'order': order,
        'filter': nameFilter,
        'page': page + 1,
        'pages': range(1, pagesCount + 1),
        'nextPage': page + 2 if page < pagesCount - 1 else 0,
        'adPlace': themes[random.randint(0, len(themes) - 1)]['id'] if len(themes) > 0 else -1,
        'emptyList': len(themes) == 0
    })


@view(path=r'^themes/(\d{1,10})/download/(.{20})/(.{20})/?')
def download(_, themeId, tokenA, tokenB):
    token = gen_token(themeId)
    tokenA = ''.join(sorted(tokenA))
    tokenB = ''.join(sorted(tokenB))
    token = ''.join(sorted(token))
    if not token == tokenA or not token == tokenB:
        raise Http404

    name, data = get_theme_archive(themeId)
    if name and data:
        resp = http.HttpResponse(data, mimetype='application/x-zip-compressed')
        resp['Content-Disposition'] = 'attachment; filename=%s.jar' % name
        return resp
    else:
        raise Http404


def gen_token(id):
    id = int(id)
    token = ''
    x = 0
    for i in range(20):
        x += id
        token += str(x)
    return token[0:20]


@view(path=r'^themes/(\d{1,10})/?')
def theme(request, themeId):
    theme = get_theme(themeId)
    if not theme:
        raise Http404

    tokenA = gen_token(themeId)
    tokenA = ''.join(random.sample(tokenA, len(tokenA)))
    tokenB = ''.join(random.sample(tokenA, len(tokenA)))

    theme['languages'] = _LANGUAGES
    theme['tokenA'] = tokenA
    theme['tokenB'] = tokenB

    return render(request, 'themes/theme.html', theme)


@view(path=r'^themes/uploaded/(\d{1,10})/?')
def uploaded_theme(request, themeId):
    theme = get_theme(themeId)
    if not theme:
        raise Http404

    theme['languages'] = _LANGUAGES

    return render(request, 'themes/uploaded.html', theme)


@view(path=r'^themes/upload/?')
def upload(request):
    if request.method == 'POST':
        form = UploadThemeForm(request.POST, request.FILES)
        if form.is_valid():
            theme = form.save()
            fill_theme_elements(theme)
            theme.save()
            try:
                send_mail("New theme has been uploaded",
                          """Theme #%s has been uploaded\n
                            Preview: http://ideacolorthemes.org/themes/%s\n
                            Manage: http://www.ideacolorthemes.org/admin/backend/theme/%s
                            """ % (theme.id, theme.id, theme.id),
                          settings.NOTYFY_EMAIL,
                          [settings.NOTYFY_EMAIL],
                          fail_silently=True)
            except:
                pass
            return HttpResponseRedirect('/themes/uploaded/%d/' % theme.id)
    else:
        form = UploadThemeForm()

    return render(request, 'themes/upload.html', {
        'form': form
    })


@view(path=r'^themes/import/(\d{1,10})/?')
def import_from_eclipse(request, themeId):
    result = import_theme(themeId)
    if result < 0:
        return http.HttpResponseBadRequest()

    return redirect('/themes/%s' % result)


@view(path=r'^themes/download-all-archive/?')
def download_all_archive(request):
    token_value = request.session.get('shopping_token', None)
    if allow_download_all(token_value):
        archive = get_all_themes_archive()
        resp = http.HttpResponse(archive, mimetype='application/x-zip-compressed')
        resp['Content-Disposition'] = 'attachment; filename=all-idea-color-themes.zip'
        return resp

    return HttpResponseForbidden()


@view(path=r'^themes/download-all/?')
def download_all(request):
    token_value = request.session.get('shopping_token', None)
    if allow_download_all(token_value):
        return render(request, 'themes/download-all-payed.html')

    token = ShoppingToken()
    token.save()

    # ShoppingToken.objects.filter(payed=False).exclude(date__gte=(datetime.now() - timedelta(days=1)).date()).delete()

    form = PayPalPaymentsForm(initial={
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '2.00',
        'item_name': 'All themes for IDEA',
        'invoice': token.value,
        'notify_url': ROOT_URL + reverse('paypal-ipn'),
        'return_url': ROOT_URL + '/themes/download-all/',
        'cancel_return': ROOT_URL + '/themes/download-all/',
    })

    request.session['shopping_token'] = token.value
    return render(request, 'themes/download-all.html', {
        'form': form
    })


def payment_successful_handler(sender, **kwargs):
    if sender.payment_status == "Completed":
        try:
            token = ShoppingToken.objects.get(value=sender.invoice)
            token.payed = True
            token.save()
        except ObjectDoesNotExist:
            pass


payment_was_successful.connect(payment_successful_handler)
