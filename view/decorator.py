# -*- coding: utf-8 -*-


def validate_required_parameters(required=None):
    """Validate the parameters of form which method is post."""
    def generator(func):
        def wrapper(self, *args, **kwargs):
            if not required:
                func(self)
            for parameter in required:
                if parameter not in self.request.arguments:
                    self.redirect("http://bing.com")
            func(self, message="Good")
        return wrapper
    return generator
