from django.test.runner import DiscoverRunner as BaseRunner
from wagtail.models import Locale


class MyMixinRunner(object):
    def setup_databases(self, *args, **kwargs):
        temp_return = super(MyMixinRunner, self).setup_databases(*args, **kwargs)
        Locale.objects.create(language_code="fr")
        return temp_return

    def teardown_databases(self, *args, **kwargs):
        # do somthing
        return super(MyMixinRunner, self).teardown_databases(*args, **kwargs)


class MyTestRunner(MyMixinRunner, BaseRunner):
    pass
