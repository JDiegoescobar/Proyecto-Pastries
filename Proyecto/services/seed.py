import sys
import os

# Esto le dice a Python dónde está la carpeta raíz de tu proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from models.evento import Local, Sala
from models.usuario import Usuario  # Ajusta según lo que necesites importar
# ... resto de tu código ...