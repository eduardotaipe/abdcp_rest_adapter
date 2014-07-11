# -*- coding: utf-8 -*-

def load_class(name):
    components = name.split('.')
    module_path = '.'.join(components[:-1])
    class_name = components[-1]
    mod = __import__(module_path, fromlist=[class_name])
    klass = getattr(mod, class_name)
    return klass
