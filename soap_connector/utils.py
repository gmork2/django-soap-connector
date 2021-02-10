from django.core.cache import cache


def dump_cache(depth, items):
    data = dict()
    for key, value in items:
        user_id = key.split(':')[0]
        data[key] = {}
        for cls, pk_list in value.items():
            data[key][cls] = {}
            for pk in pk_list:
                content = cache.get(':'.join([user_id, cls]), version=pk)
                data[key][cls][pk] = content
    return data


def obtain_ip(request):
    """
    Obtains ip client address.

    :return:
    """
    return (
        request.META.get('HTTP_X_FORWARDED_FOR') or
        request.META.get('REMOTE_ADDR', '?')
    ).split(',')[0]
