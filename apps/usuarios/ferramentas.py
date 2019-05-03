# coding: utf-8

import os

# Models' functions

def nomear_imagem(instance, filename):
    nome = instance.user.username
    extensao = os.path.splitext(filename)[-1]
    return 'usuarios/%s/%s%s' % (nome, nome, extensao)