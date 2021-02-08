from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import threading

request_cfg = threading.local()


class DatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_cfg.context_instance = "default"

    def process_response(self, request, response):
        if hasattr(request_cfg, "context_instance"):
            del request_cfg.context_instance
        return response


class SubdomainRouter:
    route_app_labels = set(
        ["core"] + [x.split('.')[-1] for x in settings.INSTALLED_APPS if x.startswith("django")]
    )
    db_list = list(settings.DATABASES.keys())

    def _default_db(self, model):
        if model._meta.app_label in self.route_app_labels:
            return settings.CORE_DB_NAME
        
        db_name = getattr(request_cfg, "context_instance", None)
        if db_name is None:
            return None
        return db_name

    def db_for_read(self, model, **hints):
        return self._default_db(model)

    def db_for_write(self, model, **hints):
        return self._default_db(model)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == settings.CORE_DB_NAME and app_label not in self.route_app_labels:
            return False

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db in self.db_list and obj2._state.db in self.db_list:
            return True
        return None

        