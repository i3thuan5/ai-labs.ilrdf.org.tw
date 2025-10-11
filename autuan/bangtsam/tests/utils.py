from django.contrib.auth.models import User
from django.core.files.base import ContentFile
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


def get_test_document_file(file_suffix):
    fake_file = ContentFile(b"A boring example document")
    fake_file.name = f"test.{file_suffix}"
    return fake_file
