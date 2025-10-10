from django.contrib.auth.models import User
from wagtail.models import Page, Site


def tshong_superuser():
    superuser = User.objects.create_superuser(
        'kuanliuan', 'kuan@ithuan.tw', 'ku#va0ti17@')
    return superuser


def tshong_wagtail_site():
    root = Page.get_first_root_node()
    Site.objects.create(
        hostname="testserver",
        root_page=root,
        is_default_site=True,
        site_name="testserver",
    )
    return root
