# -*- coding: utf-8 -*-
# @author: leesoar
# @email: secure@tom.com
# @email2: employ@aliyun.com


def version():
    """get version from version file"""
    from curl2 import __version__
    return __version__.version()
