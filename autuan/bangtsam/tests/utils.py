from django.contrib.auth.models import User


def tshong_superuser():
    superuser = User.objects.create_superuser(
        'kuanliuan', 'kuan@ithuan.tw', 'ku#va0ti17@')
    return superuser
