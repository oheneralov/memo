# https://realpython.com/learning-paths/#python-core-language-advanced
class BaseView:
    def handle(self):
        return ["base"]

class AuthMixin(BaseView):
    def handle(self):
        return ["auth"] + super().handle()

class CacheMixin(BaseView):
    def handle(self):
        return ["cache"] + super().handle()

class ReportView(AuthMixin, CacheMixin):
    def handle(self):
        return ["report"] + super().handle()

print(ReportView().handle())

# ['report', 'auth', 'cache', 'base']

# report -> auth -> cache -> base

class BaseView:
    def handle(self):
        return ["base"]

class AuthMixin(BaseView):
    def handle(self):
        return ["auth"] + super().handle()

class CacheMixin(BaseView):
    def handle(self):
        return ["cache"] + super().handle()
    
class LoggingMixin(BaseView):
    def handle(self):
        return ["logging"] + super().handle()

class ReportView(AuthMixin, CacheMixin, LoggingMixin):
    def handle(self):
        return ["report"] + super().handle()

print(ReportView().handle())

# ['report', 'auth', 'cache', 'logging', 'base']