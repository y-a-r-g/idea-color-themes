from StringIO import StringIO
from datetime import datetime, timedelta
from random import sample
import urllib2
from zipfile import ZipFile
from django.core.exceptions import ObjectDoesNotExist
from backend.models import Theme, ShoppingToken
from backend.logic.themes.serializer import *

__author__ = 'yarg'

THEMES_PER_PAGE = 20
AD_PER_PAGE = 1
PROMO_THEMES_LIMIT = 4


def get_page(order, nameFilter, page, count=THEMES_PER_PAGE, adCount=AD_PER_PAGE, promoCount=PROMO_THEMES_LIMIT):
    themesPerPage = count - adCount

    filteredThemes = list(Theme.objects.filter(name__icontains=nameFilter, moderating=False).order_by('-' + order))
    themesCount = len(filteredThemes)
    pagesCount = themesCount / themesPerPage
    if not (themesCount % themesPerPage) == 0:
        pagesCount += 1

    page = max(0, min(pagesCount - 1, page))

    start = page * themesPerPage
    end = start + themesPerPage

    themes = list(filteredThemes[start:end])

    if page == 0 and order == 'downloads':
        themes = list(_find_promo_themes(promoCount) + themes)

    themes = [
        {
            'id': t.id,
            'name': t.name,
            'downloads': t.downloads,
            'elements': dict([(e[0], gen_style(e[1])) for e in deserialize_from_lines(t.elements.split('\n'))]),
            'promote': t.promote
        }
        for t in themes]

    return themes, page, pagesCount


def get_theme(themeId):
    try:
        theme = Theme.objects.get(id=themeId)
    except ObjectDoesNotExist:
        return None

    return {
        'id': theme.id,
        'name': theme.name,
        'downloads': theme.downloads,
        'author': theme.author,
        'website': theme.website,
        'comment': theme.comment,
        'elements': dict([(e[0], gen_style(e[1])) for e in deserialize_from_lines(theme.elements.split('\n'))])
    }


def get_theme_archive(themeId):
    try:
        theme = Theme.objects.get(id=themeId)
    except ObjectDoesNotExist:
        return None, None

    theme.downloads = int(theme.downloads) + 1
    theme.save()

    if theme.archive:
        data = theme.archive.read()
    else:
        data = serialize_to_idea_lines(deserialize_from_lines(theme.elements.split(u'\n')), theme.name)
        data = u'\n'.join(data).encode('utf_8')

    options = u"""<?xml version="1.0" encoding="UTF-8"?>
    <application>
      <component name="EditorColorsManagerImpl">
        <option name="USE_ONLY_MONOSPACED_FONTS" value="true" />
        <global_color_scheme name="%s" />
      </component>
    </application>
    """ % theme.name

    resultStream = StringIO()
    archive = ZipFile(resultStream, 'w')

    archive.writestr('IntelliJ IDEA Global Settings', '')
    archive.writestr('options/colors.scheme.xml', options.encode('utf_8'))

    archive.writestr('colors/%s.xml' % theme.name, data)

    archive.close()
    return theme.name.encode('utf_8'), resultStream.getvalue()


def fill_theme_elements(theme):
    theme.elements = '\n'.join(serialize_to_lines(deserialize_from_idea(theme.archive.readlines())))


def _find_promo_themes(count):
    promoThemeLifeTime = 30 * 24 * 60 * 60

    now = datetime.now().date()

    def filterPromo(t):
        dt = t.date
        if isinstance(dt, unicode) or isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%d-%m').date()
        if (now - dt).total_seconds() > promoThemeLifeTime:
            t.promote = False
            t.save()
        return t.promote

    themes = filter(filterPromo, Theme.objects.filter(promote=True, moderating=False))
    if len(themes) > count:
        themes = sample(set(themes), count)

    return themes


def allow_download_all(token_value):
    dateLimit = (datetime.now() + timedelta(days=1)).date()
    if token_value:
        try:
            ShoppingToken.objects.get(value=token_value, date__lte=dateLimit, payed=True)
            return True
        except ObjectDoesNotExist:
            pass
    return False


def get_all_themes_archive():
    themes = Theme.objects.filter(moderating=False)
    resultStream = StringIO()
    archive = ZipFile(resultStream, 'w')
    archive.writestr('readme.txt', 'Thank you!\r\n Your ideacolorthemes.org!')
    for theme in themes:
        name, data = get_theme_archive(theme.id)
        archive.writestr('%s.jar' % name, data)
    archive.close()
    return resultStream.getvalue()


def import_theme(themeId):
    try:
        url = 'http://eclipsecolorthemes.org/?view=empty&action=download&theme=%s&type=xml'
        response = urllib2.urlopen(url % themeId)
        xml = response.read()
        descr, elements = deserialize_from_eclipse_color_theme_xml(
            xml.replace('\r', '').split('\n'))
        name, author, website = descr
        elements = '\n'.join(serialize_to_lines(elements))

        if len(name) == 0:
            return -1

        try:
            theme = Theme.objects.get(name=name)
            theme.elements = elements
        except ObjectDoesNotExist:
            theme = Theme(name=name,
                          author=author or 'Idea Color Themes',
                          website=website or 'http://www.ideacolorthemes.org',
                          elements=elements,
                          ect=themeId,
                          promote=False,
                          moderating=False,
                          comment="")
        theme.save()
        return theme.id
    except:
        return -1
