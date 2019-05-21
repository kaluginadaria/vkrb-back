import hashlib

import phonenumbers
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from webpack_loader.utils import _get_bundle

from vkrb.application import settings


def validate_phone_number(x):
    try:
        numobj = phonenumbers.parse(x)
    except phonenumbers.NumberParseException:
        return None

    return phonenumbers.format_number(
        numobj,
        phonenumbers.PhoneNumberFormat.E164
    )


def chunk_page(queryset, chunk_size):
    pk = None
    field = queryset.model._meta.pk
    order_by_field = field.attname
    queryset = queryset.order_by(order_by_field)

    while True:
        if pk:
            queryset = queryset.filter(pk__gt=pk)

        page = list(queryset[:chunk_size])
        num_items = len(page)

        if num_items == 0:
            return

        last_item = page[-1]

        pk = last_item.pk

        yield page

        if num_items < chunk_size:
            return


def queryset_by_chunks(queryset, chunk_size):
    for page in chunk_page(queryset, chunk_size):
        yield from page


def build_url(url):
    url = url.strip('/ ')
    return f'/{url}'


def build_url_with_domain(url):
    schema = settings.SCHEMA.strip('/ ')
    domain = settings.DOMAIN.strip('/ ')
    url = url.strip('/ ')
    return f'{schema}://{domain}/{url}'


def build_file_url(filename):
    return f'file:///media/vkrb/{filename}'


def build_bundle_url(bundle):
    return f'file:///opt/vkrb/src/assets/{bundle}'


def get_absolute_bundle_urls(bundle_name, extension, config='DEFAULT'):
    def mapper(url):
        if not url.startswith('http'):
            url = build_bundle_url(url)
        return url

    urls = [_.get('name') for _ in _get_bundle(bundle_name, extension, config)]
    return list(map(mapper, urls))


def generate_html(**kwargs):
    ctx = kwargs.get('ctx', None)
    template_path = kwargs.get('template_path')
    template_text = kwargs.get('template_text')

    if template_path is None and template_text is None:
        raise Exception('template_path or template_text must be not None')

    if isinstance(ctx, Context):
        ctx = ctx.flatten()
    elif ctx is None:
        ctx = {}

    if template_path is not None:
        template = get_template(template_path)

        html = template.render(ctx)

        return html


def generate_pdf(html, **kwargs):
    import pdfkit
    options = {
        'disable-javascript': None,
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '1cm',
        'margin-right': '1cm',
        'margin-bottom': '1cm',
        'margin-left': '2cm',
        'print-media-type': ''
    }
    extra_options = kwargs.get('extra_options')

    if extra_options is not None:
        options.update(extra_options)
    result = pdfkit.from_string(
        html, False, options,
        css=kwargs.get('css'),
        configuration=pdfkit.configuration(
            wkhtmltopdf=settings.WKHTMLTOPDF_PATH
        )
    )

    return result


def render_to_pdf(**kwargs):
    html = generate_html(**kwargs)
    if html:
        pdf_file = generate_pdf(html, **kwargs)

        if kwargs.get('return_pdf'):
            return pdf_file

        http_response = HttpResponse(
            pdf_file,
            content_type='application/pdf'
        )
        http_response['Content-Disposition'] = 'filename="{0}"' \
            .format(kwargs.get('filename', 'report.pdf'))

        return http_response
    else:
        return HttpResponse(status=404)


def to_int(val, default=None):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def calculate_image_hash(image):
    image_hashes = []
    for chunk in image.chunks():
        image_hashes.append(hashlib.sha256(chunk).hexdigest())
    image_hash = hashlib.sha256(','.join(image_hashes).encode()).hexdigest()
    return image_hash
