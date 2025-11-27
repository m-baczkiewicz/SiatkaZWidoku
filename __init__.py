# -*- coding: utf-8 -*-

def classFactory(iface):
    from .siatka_z_widoku import SiatkaZWidokuPlugin
    return SiatkaZWidokuPlugin(iface)
