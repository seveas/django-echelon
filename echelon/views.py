# Copyright (c) 2011 Dennis Kaarsemaker <dennis@kaarsemaker.net>
# Small piece of middleware to be able to access authentication data from
# everywhere in the django code.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Django nor the names of its contributors may be used
#        to endorse or promote products derived from this software without
#        specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.contrib.auth.decorators import user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext
from echelon.models import ChangelogEntry

class FakeChangeList(object):
    show_all = False
    can_show_all = False
    multi_page = True

    def __init__(self, paginator, page_num, model):
        self.paginator = paginator
        self.page_num = int(page_num)
        self.model = model

    def get_query_string(self, kwargs):
        if self.model:
            return './?content_type=%s&page=%s' % (self.model, kwargs['p'])
        return './?p=%s' % kwargs['p']


@user_passes_test(lambda user: user.is_superuser)
def changelog(request):
    log = ChangelogEntry.objects.all()
    selected = request.GET.get('content_type', None)
    if selected and selected.isdigit():
        selected = int(selected)
        log = log.filter(content_type__id=selected)
    else:
        selected = None
    paginator = Paginator(log, 50)
    page = request.GET.get('p','0')
    if not page.isdigit():
        page = '0'
    page = int(page) + 1
    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    ctx = RequestContext(request, {
        'models': ContentType.objects.order_by('app_label', 'model'),
        'selected': selected,
        'page': page,
        'paginator': paginator,
        'fake_cl': FakeChangeList(paginator, page.number-1, selected),
    })
    return render_to_response('echelon/changelog.html', ctx)
