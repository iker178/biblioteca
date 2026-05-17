"""
Wiki Multiverso Minecraft - Servidor Principal (Edición Definitiva)
Este script gestiona las rutas, la lógica de la enciclopedia, un sistema de
búsqueda interno y la configuración avanzada del servidor Flask.
Cumple estrictamente con los estándares PEP 8 (Flake8).
"""

import logging
from datetime import datetime
from flask import Flask, render_template, abort, request, jsonify

# --- CONFIGURACIÓN DEL SERVIDOR ---

class Config:
    """Clase base para la configuración de Flask."""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'super_llave_secreta_minecraft_wiki'
    JSON_AS_ASCII = False

# Configuración del sistema de registro (Logs)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# --- BASE DE DATOS INTERNA (Diccionario Masivo) ---

WIKI_DATA = {
    "minecraft": {
        "titulo": "Minecraft: Edición Estándar",
        "descripcion": (
            "El sandbox original de construcción y supervivencia. "
            "Infinitas posibilidades en un mundo generado por bloques."
        ),
        "lanzamiento": "2011",
        "controles": {
            "PC": [
                {"accion": "Moverse", "tecla": "W, A, S, D"},
                {"accion": "Saltar", "tecla": "Espacio"},
                {"accion": "Inventario", "tecla": "E"},
                {"accion": "Agacharse", "tecla": "Shift Izq."},
                {"accion": "Correr", "tecla": "Control Izq."},
                {"accion": "Soltar Objeto", "tecla": "Q"}
            ],
            "Xbox": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Saltar", "tecla": "A"},
                {"accion": "Inventario", "tecla": "Y"},
                {"accion": "Agacharse", "tecla": "Presionar Stick Der."},
                {"accion": "Pegar/Minar", "tecla": "RT"},
                {"accion": "Colocar/Usar", "tecla": "LT"}
            ],
            "Nintendo": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Saltar", "tecla": "B"},
                {"accion": "Inventario", "tecla": "X"},
                {"accion": "Agacharse", "tecla": "Presionar Stick Der."},
                {"accion": "Pegar/Minar", "tecla": "ZR"},
                {"accion": "Colocar/Usar", "tecla": "ZL"}
            ],
            "Telefono": [
                {"accion": "Moverse", "tecla": "D-pad Virtual Izquierdo"},
                {"accion": "Saltar", "tecla": "Botón de Salto Virtual"},
                {"accion": "Inventario", "tecla": "Botón de 3 Puntos (...)"},
                {"accion": "Agacharse", "tecla": "Doble toque al centro"},
                {"accion": "Pegar/Minar", "tecla": "Mantener la pantalla"},
                {"accion": "Colocar/Usar", "tecla": "Toque rápido"}
            ]
        },
        "herramientas": [
            "Arco", "Azada de Diamante", "Azada de Hierro", "Azada de Madera", 
            "Azada de Netherite", "Azada de Oro", "Azada de Piedra", "Ballesta", 
            "Brújula", "Brújula de recuperación", "Caña con hongo distorsionado", 
            "Caña con zanahoria", "Caña de pescar", "Carga ígnea", "Catalejo", 
            "Cizallas", "Cubo de agua", "Cubo de lava", "Cubo de nieve polvo", 
            "Cubo vacío", "Encendedor (Pedernal y hierro)", "Escudo", 
            "Espada de Diamante", "Espada de Hierro", "Espada de Madera", 
            "Espada de Netherite", "Espada de Oro", "Espada de Piedra", 
            "Etiqueta", "Hacha de Diamante", "Hacha de Hierro", "Hacha de Madera", 
            "Hacha de Netherite", "Hacha de Oro", "Hacha de Piedra", "Maza (Mace)", 
            "Pala de Diamante", "Pala de Hierro", "Pala de Madera", "Pala de Netherite", 
            "Pala de Oro", "Pala de Piedra", "Pico de Diamante", "Pico de Hierro", 
            "Pico de Madera", "Pico de Netherite", "Pico de Oro", "Pico de Piedra", 
            "Pincel", "Reloj", "Rienda", "Tridente"
        ],
        "secretos": [
            "El bioma de Tierras Baldías (Badlands) tiene más oro.",
            "Los Piglins aman el oro pero odian el fuego de almas.",
            "Poner un bloque de notas sobre calabazas cambia el sonido.",
            "Nombrar a una oveja 'jeb_' la hará cambiar de color.",
            "Nombrar a un mob 'Dinnerbone' lo pondrá de cabeza.",
            "Los Creepers tienen miedo de los gatos y ocelotes."
        ],
        "mobs_destacados": [
            {"nombre": "Warden", "tipo": "Hostil ciego", "hp": 500},
            {"nombre": "Dragón del Ender", "tipo": "Jefe Final", "hp": 200},
            {"nombre": "Wither", "tipo": "Jefe de Invocación", "hp": 300},
            {"nombre": "Ajolote", "tipo": "Aliado acuático", "hp": 14}
        ],
        "biomas": [
            "Llanuras", "Desierto", "Bosque Oscuro", "Taiga Nevada",
            "Bioma de Setas", "Picos Helados", "Pantano de Manglares"
        ]
    },
    "dungeons": {
        "titulo": "Minecraft Dungeons",
        "descripcion": (
            "Explora mazmorras, lucha contra monstruos y mejora tu "
            "equipo en este título de rol de acción (Dungeon Crawler)."
        ),
        "lanzamiento": "2020",
        "controles": {
            "PC": [
                {"accion": "Mover y Atacar", "tecla": "Clic Izquierdo"},
                {"accion": "Disparar", "tecla": "Clic Derecho"},
                {"accion": "Esquivar", "tecla": "Espacio"},
                {"accion": "Artefactos", "tecla": "1, 2, 3"},
                {"accion": "Poción", "tecla": "E"}
            ],
            "Xbox": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Atacar", "tecla": "A"},
                {"accion": "Disparar", "tecla": "RT"},
                {"accion": "Esquivar", "tecla": "RB"},
                {"accion": "Artefactos", "tecla": "X, Y, B"},
                {"accion": "Poción", "tecla": "LB"}
            ],
            "Nintendo": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Atacar", "tecla": "A"},
                {"accion": "Disparar", "tecla": "ZR"},
                {"accion": "Esquivar", "tecla": "R"},
                {"accion": "Artefactos", "tecla": "Y, X, B"},
                {"accion": "Poción", "tecla": "L"}
            ],
            "Telefono": [
                {"accion": "Moverse", "tecla": "Tocar punto en pantalla"},
                {"accion": "Atacar", "tecla": "Tocar al enemigo"},
                {"accion": "Esquivar", "tecla": "Botón Virtual Rodar"},
                {"accion": "Artefactos", "tecla": "Botones en la Interfaz"},
                {"accion": "Poción", "tecla": "Icono de Corazón"}
            ]
        },
        "herramientas": [
            "Arco de tormenta", "Ballesta pesada", "Capa de invisibilidad",
            "Cuchillo de alma", "Gólem de hierro portátil", 
            "Hongo de la muerte", "Martillo de gravedad"
        ],
        "secretos": [
            "Las runas ocultas están en todos los niveles base.",
            "El Archimaldeano fue corrompido por el Orbe del Dominio.",
            "Existen cofres ocultos detrás de cascadas de agua.",
            "El level de las vacas se desbloquea en la iglesia del inicio."
        ],
        "mobs_destacados": [
            {"nombre": "Archimaldeano", "tipo": "Jefe Principal", "hp": 800},
            {"nombre": "Monstruo de Redstone", "tipo": "Jefe", "hp": 1500},
            {"nombre": "Enredadera base", "tipo": "Hostil común", "hp": 50}
        ],
        "biomas": [
            "Bosque de Creepers", "Cañón Cactus", "Pastizales de Calabazas",
            "Minas de Redstone", "Templo del Desierto"
        ]
    },
    "legends": {
        "titulo": "Minecraft Legends",
        "descripcion": (
            "Lidera a tus aliados en batallas estratégicas en tiempo real "
            "contra la invasión de los Piglins desde el Nether."
        ),
        "lanzamiento": "2023",
        "controles": {
            "PC": [
                {"accion": "Moverse", "tecla": "W, A, S, D"},
                {"accion": "Atacar", "tecla": "E"},
                {"accion": "Invocar", "tecla": "Q"},
                {"accion": "Comandar", "tecla": "R"},
                {"accion": "Mapa", "tecla": "M"}
            ],
            "Xbox": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Atacar", "tecla": "X"},
                {"accion": "Invocar", "tecla": "Y"},
                {"accion": "Comandar", "tecla": "RT"},
                {"accion": "Mapa", "tecla": "Botón Vista"}
            ],
            "Nintendo": [
                {"accion": "Moverse", "tecla": "Stick Izquierdo"},
                {"accion": "Atacar", "tecla": "Y"},
                {"accion": "Invocar", "tecla": "X"},
                {"accion": "Comandar", "tecla": "ZR"},
                {"accion": "Mapa", "tecla": "Menos (-)"}
            ],
            "Telefono": [
                {"accion": "Juego en la nube", "tecla": "Controles virtuales"},
                {"accion": "Moverse", "tecla": "Joystick Táctil"},
                {"accion": "Acciones", "tecla": "Botones de Acción Virtuales"}
            ]
        },
        "herramientas": [
            "Caja de música de ayudantes", "Estandarte de Valentía",
            "Llamas de Creación", "Montura de Caballo", "Montura de Escarabajo"
        ],
        "secretos": [
            "Los Primeros son inmunes al daño de los Piglins pequeños.",
            "Las torres de flechas se pueden mejorar con piedra roja.",
            "El bioma de selva es ideal para ocultar tus estructuras.",
            "Los Creepers aliados son la mejor arma contra murallas."
        ],
        "mobs_destacados": [
            {"nombre": "El Devorador", "tipo": "Jefe Piglin", "hp": 2000},
            {"nombre": "Gólem de Piedra", "tipo": "Aliado asedio", "hp": 100},
            {"nombre": "Gólem de Madera", "tipo": "Aliado distancia", "hp": 40}
        ],
        "biomas": [
            "Picos dentados", "Prados verdes", "Tierras baldías corruptas",
            "Tumbas de Piglins"
        ]
    },
    "biomas_superficie": {
        "titulo": "Biomas: Llanuras y Entornos Verdes",
        "descripcion": (
            "Catálogo exhaustivo de los ecosistemas templados, "
            "prados y bosques fértiles de la superficie del Overworld."
        ),
        "lanzamiento": "Ecosistema I",
        "controles": {
            "PC": [
                {"accion": "Explorar Praderas", "tecla": "Caminar libremente"},
                {"accion": "Ubicar Aldeas", "tecla": "Seguir caminos de tierra"}
            ],
            "Telefono": [
                {"accion": "Navegar Terreno", "tecla": "Deslizar joystick"}
            ]
        },
        "herramientas": [
            "Cizallas para hojas", "Hacha de talado", "Polvo de hueso"
        ],
        "biomas": [
            "Arboledas de Cerezos", "Bosque de Robles", "Bosque Oscuro", 
            "Llanuras", "Praderas de Flores", "Taiga"
        ],
        "secretos": [
            "Las llanuras son las zonas con mayor tasa de aparición de caballos.",
            "En el bosque oscuro pueden generarse mansiones de manera oculta."
        ],
        "mobs_destacados": [
            {"nombre": "Caballo", "tipo": "Pacífico / Montura", "hp": 30},
            {"nombre": "Oveja", "tipo": "Pasivo común", "hp": 8},
            {"nombre": "Zorro de Taiga", "tipo": "Neutral", "hp": 10}
        ]
    },
    "biomas_aridosextremos": {
        "titulo": "Biomas: Áridos y Climas Extremos",
        "descripcion": (
            "Enciclopedia de entornos hostiles marcados por la escasez "
            "de agua, altas temperaturas o terrenos montañosos escarpados."
        ),
        "lanzamiento": "Ecosistema II",
        "controles": {
            "PC": [
                {"accion": "Evitar Caídas", "tecla": "Usar Shift en precipicios"},
                {"accion": "Cruzar Desiertos", "tecla": "Llevar reservas de agua"}
            ],
            "Telefono": [
                {"accion": "Escalar Picos", "tecla": "Botón de salto continuo"}
            ]
        },
        "herramientas": [
            "Botas de cuero para nieve", "Cubo de agua", "Pico de minería"
        ],
        "biomas": [
            "Cañón Cactus", "Desierto", "Pendientes Nevadas",
            "Picos Dentados", "Sabana", "Tierras Baldías (Badlands)"
        ],
        "secretos": [
            "El bioma de Badlands genera pozos de mina expuestos en la superficie.",
            "La nieve blanda en los picos helados puede hundir y congelar al jugador."
        ],
        "mobs_destacados": [
            {"nombre": "Camello", "tipo": "Montura doble", "hp": 32},
            {"nombre": "Conejito de arena", "tipo": "Pasivo", "hp": 3},
            {"nombre": "Esqueleto Errante", "tipo": "Hostil frío", "hp": 20}
        ]
    },
    "biomas_dimensiones": {
        "titulo": "Biomas: Inframundos y Dimensiones",
        "descripcion": (
            "Estudio avanzado de las realidades alternativas: "
            "Los peligros del Nether, el vacío del End y las profundidades."
        ),
        "lanzamiento": "Ecosistema III",
        "controles": {
            "PC": [
                {"accion": "Navegar en Lava", "tecla": "Montar un Lavagante"},
                {"accion": "Combate de Cerca", "tecla": "Bloquear con Escudo"}
            ],
            "Telefono": [
                {"accion": "Esquivar Proyectiles", "tecla": "Movimiento lateral"}
            ]
        },
        "herramientas": [
            "Ancla de respawn", "Piedra de imán", "Poción de resistencia"
        ],
        "biomas": [
            "Bosque Carmesí", "Ciudades del End", "Cuevas de Sculk",
            "Delta de Basalto", "Islas del Fin", "Valle de Arena de Almas"
        ],
        "secretos": [
            "Intentar dormir en el Nether o en el End provocará una explosión.",
            "El fuego azul de almas inflige el doble de daño que el fuego común."
        ],
        "mobs_destacados": [
            {"nombre": "Ghast", "tipo": "Hostil flotante", "hp": 10},
            {"nombre": "Piglin Bruto", "tipo": "Hostil implacable", "hp": 50},
            {"nombre": "Shulker", "tipo": "Defensor de fortaleza", "hp": 30}
        ]
    },
    "apartado_herramientas": {
        "titulo": "Catálogo de Arsenal y Herramientas",
        "descripcion": (
            "Sección dedicada exclusivamente al análisis de todas las herramientas, "
            "armas e instrumentos de ingeniería del multiverso."
        ),
        "lanzamiento": "Global",
        "controles": {
            "PC": [
                {"accion": "Usar Herramienta (Romper)", "tecla": "Clic Izquierdo"},
                {"accion": "Acción Especial (Bloquear)", "tecla": "Clic Derecho"}
            ],
            "Telefono": [
                {"accion": "Accionar Arsenal", "tecla": "Mantener pulsado"}
            ]
        },
        "herramientas": [
            "Arco", "Azada de Diamante", "Azada de Hierro", "Azada de Madera", 
            "Azada de Netherite", "Azada de Oro", "Azada de Piedra", "Ballesta", 
            "Brújula", "Brújula de recuperación", "Caña con hongo distorsionado", 
            "Caña con zanahoria", "Caña de pescar", "Carga ígnea", "Catalejo", 
            "Cizallas", "Cubo de agua", "Cubo de lava", "Cubo de nieve polvo", 
            "Cubo vacío", "Encendedor (Pedernal y hierro)", "Escudo", 
            "Espada de Diamante", "Espada de Hierro", "Espada de Madera", 
            "Espada de Netherite", "Espada de Oro", "Espada de Piedra", 
            "Etiqueta", "Hacha de Diamante", "Hacha de Hierro", "Hacha de Madera", 
            "Hacha de Netherite", "Hacha de Oro", "Hacha de Piedra", "Maza (Mace)", 
            "Pala de Diamante", "Pala de Hierro", "Pala de Madera", "Pala de Netherite", 
            "Pala de Oro", "Pala de Piedra", "Pico de Diamante", "Pico de Hierro", 
            "Pico de Madera", "Pico de Netherite", "Pico de Oro", "Pico de Piedra", 
            "Pincel", "Reloj", "Rienda", "Tridente"
        ],
        "biomas": [
            "Zonas de Crafteo", "Vetas de Hierro", "Yacimientos de Diamante"
        ],
        "secretos": [
            "El hacha inflige más daño por golpe crítico que la espada en PC.",
            "La durabilidad de una herramienta de netherite es un 30% superior."
        ],
        "mobs_destacados": [
            {"nombre": "Esmaltador", "tipo": "Mejora de armas", "hp": 20},
            {"nombre": "Gólem de Cobre", "tipo": "Ayudante mecánico", "hp": 20}
        ]
    }
}

COMPENDIO_MOBS = {
    "Jefes / Entidades Mayores": [
        {"nombre": "Dragón del Ender", "origen": "Minecraft", "hp": 200, "drop": "Huevo de Dragón"},
        {"nombre": "Guardián Anciano", "origen": "Minecraft", "hp": 80, "drop": "Esponja húmeda"},
        {"nombre": "Warden", "origen": "Minecraft", "hp": 500, "drop": "Catalizador de Sculk"},
        {"nombre": "Wither", "origen": "Minecraft", "hp": 300, "drop": "Estrella del Nether"}
    ],
    "Criaturas Hostiles": [
        {"nombre": "Ahogado (Drowned)", "origen": "Minecraft", "hp": 20, "drop": "Tridente / Cobre"},
        {"nombre": "Aldeano Zombi", "origen": "Minecraft", "hp": 20, "drop": "Carne Podrida"},
        {"nombre": "Ánima (Breeze)", "origen": "Minecraft", "hp": 30, "drop": "Vara de brisa"},
        {"nombre": "Araña de Cueva", "origen": "Minecraft", "hp": 12, "drop": "Ojo de araña"},
        {"nombre": "Bogged (Empantanado)", "origen": "Minecraft", "hp": 16, "drop": "Flechas venenosas"},
        {"nombre": "Bruja", "origen": "Minecraft", "hp": 26, "drop": "Pociones / Polvo de piedra luminosa"},
        {"nombre": "Creeper", "origen": "Minecraft", "hp": 20, "drop": "Pólvora"},
        {"nombre": "Cubo de Magma", "origen": "Minecraft", "hp": 16, "drop": "Crema de magma"},
        {"nombre": "Devastador (Ravager)", "origen": "Minecraft", "hp": 100, "drop": "Silla de montar"},
        {"nombre": "Endermite", "origen": "Minecraft", "hp": 8, "drop": "Ninguno"},
        {"nombre": "Esqueleto", "origen": "Minecraft", "hp": 20, "drop": "Hueso / Flecha"},
        {"nombre": "Esqueleto Glacial (Stray)", "origen": "Minecraft", "hp": 20, "drop": "Flechas de lentitud"},
        {"nombre": "Esqueleto Wither", "origen": "Minecraft", "hp": 20, "drop": "Cráneo de esqueleto Wither"},
        {"nombre": "Evocador", "origen": "Minecraft", "hp": 24, "drop": "Tótem de inmortalidad"},
        {"nombre": "Fantasma (Phantom)", "origen": "Minecraft", "hp": 20, "drop": "Membrana de fantasma"},
        {"nombre": "Ghast", "origen": "Minecraft", "hp": 10, "drop": "Lágrima de Ghast / Pólvora"},
        {"nombre": "Guardián", "origen": "Minecraft", "hp": 30, "drop": "Cristal / Fragmento de prismarina"},
        {"nombre": "Hoglin", "origen": "Minecraft", "hp": 40, "drop": "Carne de cerdo / Cuero"},
        {"nombre": "Ilusionista", "origen": "Minecraft", "hp": 32, "drop": "Ninguno (Comando)"},
        {"nombre": "Lepisma (Silverfish)", "origen": "Minecraft", "hp": 8, "drop": "Ninguno"},
        {"nombre": "Piglin Bruto", "origen": "Minecraft", "hp": 50, "drop": "Hacha de oro"},
        {"nombre": "Saqueador (Pillager)", "origen": "Minecraft", "hp": 24, "drop": "Ballesta / Esmeralda"},
        {"nombre": "Shulker", "origen": "Minecraft", "hp": 30, "drop": "Caparazón de Shulker"},
        {"nombre": "Slime", "origen": "Minecraft", "hp": 16, "drop": "Bola de Slime"},
        {"nombre": "Vengador (Vindicator)", "origen": "Minecraft", "hp": 24, "drop": "Hacha de hierro / Esmeralda"},
        {"nombre": "Vex", "origen": "Minecraft", "hp": 14, "drop": "Ninguno"},
        {"nombre": "Zoglin", "origen": "Minecraft", "hp": 40, "drop": "Carne podrida"},
        {"nombre": "Zombi", "origen": "Minecraft", "hp": 20, "drop": "Carne Podrida"},
        {"nombre": "Zombi Momificado (Husk)", "origen": "Minecraft", "hp": 20, "drop": "Carne podrida"}
    ],
    "Criaturas Neutrales": [
        {"nombre": "Abeja", "origen": "Minecraft", "hp": 10, "drop": "Ninguno"},
        {"nombre": "Araña", "origen": "Minecraft", "hp": 16, "drop": "Hilo / Ojo de araña"},
        {"nombre": "Delfín", "origen": "Minecraft", "hp": 10, "drop": "Bacalao crudo"},
        {"nombre": "Enderman", "origen": "Minecraft", "hp": 40, "drop": "Perla de Ender"},
        {"nombre": "Gólem de Hierro", "origen": "Minecraft", "hp": 100, "drop": "Lingote de hierro / Amapola"},
        {"nombre": "Llama", "origen": "Minecraft", "hp": 15, "drop": "Cuero"},
        {"nombre": "Llama de Comerciante", "origen": "Minecraft", "hp": 15, "drop": "Cuero / Rienda"},
        {"nombre": "Lobo", "origen": "Minecraft", "hp": 8, "drop": "Ninguno"},
        {"nombre": "Oso Polar", "origen": "Minecraft", "hp": 30, "drop": "Bacalao / Salmón crudo"},
        {"nombre": "Panda", "origen": "Minecraft", "hp": 20, "drop": "Bambú"},
        {"nombre": "Piglin", "origen": "Minecraft", "hp": 16, "drop": "Objetos de trueque"},
        {"nombre": "Piglin Zombificado", "origen": "Minecraft", "hp": 20, "drop": "Pepita de oro / Carne podrida"}
    ],
    "Criaturas Pasivas": [
        {"nombre": "Ajolote", "origen": "Minecraft", "hp": 14, "drop": "Ninguno"},
        {"nombre": "Aldeano", "origen": "Minecraft", "hp": 20, "drop": "Ninguno"},
        {"nombre": "Allay", "origen": "Minecraft", "hp": 20, "drop": "Ninguno"},
        {"nombre": "Armadillo", "origen": "Minecraft", "hp": 12, "drop": "Escama de armadillo"},
        {"nombre": "Burro", "origen": "Minecraft", "hp": 15, "drop": "Cuero"},
        {"nombre": "Caballo", "origen": "Minecraft", "hp": 15, "drop": "Cuero"},
        {"nombre": "Caballo Esqueleto", "origen": "Minecraft", "hp": 15, "drop": "Hueso"},
        {"nombre": "Caballo Zombi", "origen": "Minecraft", "hp": 15, "drop": "Carne podrida"},
        {"nombre": "Calamar", "origen": "Minecraft", "hp": 10, "drop": "Saco de tinta"},
        {"nombre": "Calamar Brillante", "origen": "Minecraft", "hp": 10, "drop": "Saco de tinta brillante"},
        {"nombre": "Camello", "origen": "Minecraft", "hp": 32, "drop": "Silla de montar (Si la tiene)"},
        {"nombre": "Cerdo", "origen": "Minecraft", "hp": 10, "drop": "Chuleta de cerdo"},
        {"nombre": "Champiñaca", "origen": "Minecraft", "hp": 10, "drop": "Ternera cruda / Champiñón"},
        {"nombre": "Conejo", "origen": "Minecraft", "hp": 3, "drop": "Piel de conejo / Carne"},
        {"nombre": "Gato", "origen": "Minecraft", "hp": 10, "drop": "Hilo"},
        {"nombre": "Gólem de Nieve", "origen": "Minecraft", "hp": 4, "drop": "Bolas de nieve"},
        {"nombre": "Loro", "origen": "Minecraft", "hp": 6, "drop": "Pluma"},
        {"nombre": "Mula", "origen": "Minecraft", "hp": 15, "drop": "Cuero"},
        {"nombre": "Murciélago", "origen": "Minecraft", "hp": 6, "drop": "Ninguno"},
        {"nombre": "Ocelote", "origen": "Minecraft", "hp": 10, "drop": "Ninguno"},
        {"nombre": "Oveja", "origen": "Minecraft", "hp": 8, "drop": "Lana / Cordero"},
        {"nombre": "Pez Globo", "origen": "Minecraft", "hp": 3, "drop": "Pez globo"},
        {"nombre": "Pez Tropical", "origen": "Minecraft", "hp": 3, "drop": "Pez tropical"},
        {"nombre": "Rana", "origen": "Minecraft", "hp": 10, "drop": "Ninguno"},
        {"nombre": "Renacuajo", "origen": "Minecraft", "hp": 6, "drop": "Ninguno"},
        {"nombre": "Salmón", "origen": "Minecraft", "hp": 3, "drop": "Salmón crudo"},
        {"nombre": "Sniffer", "origen": "Minecraft", "hp": 14, "drop": "Semillas de flor antorcha"},
        {"nombre": "Tortuga", "origen": "Minecraft", "hp": 30, "drop": "Hierba marina / Escama (Al crecer)"},
        {"nombre": "Vaca", "origen": "Minecraft", "hp": 10, "drop": "Ternera cruda / Cuero"},
        {"nombre": "Zorro", "origen": "Minecraft", "hp": 10, "drop": "Objeto que sostenga en la boca"}
    ]
}

COMPENDIO_BIOMAS = {
    "General": [
        {"nombre": "Llanuras", "juegos": "Minecraft", "detalles": "Zonas pacíficas con vegetación y aldeas."}
    ]
}

# --- RUTAS PRINCIPALES DEL SERVIDOR (Views) ---

@app.route('/')
def index():
    """Renderiza la página principal con todos los datos."""
    return render_template(
        'index.html',
        data=WIKI_DATA,
        mobs=COMPENDIO_MOBS,
        compendio_biomas=COMPENDIO_BIOMAS
    )

@app.route('/buscar', methods=['GET'])
def ruta_busqueda():
    """Ruta para manejar el formulario de búsqueda."""
    query = request.args.get('q', '')
    if not query:
        return "<h1>Por favor, ingresa un término de búsqueda.</h1>"

    # Buscador simple lineal
    resultados = []
    for juego_id, datos in WIKI_DATA.items():
        if query.lower() in datos["titulo"].lower():
            resultados.append((datos["titulo"], "Apartado"))

    html_respuesta = f"<h1>Resultados para: '{query}'</h1><ul>"
    for hallazgo, contexto in resultados:
        html_respuesta += f"<li><strong>{contexto}:</strong> {hallazgo}</li>"
    html_respuesta += "</ul><br><a href='/'>Volver al inicio</a>"

    return html_respuesta

# --- AÑADIDOS: SISTEMA MULTILINGÜE Y CRONOLOGÍA ---

SISTEMA_IDIOMAS = {
    "es": {
        "codigo": "es",
        "nombre": "Español",
        "mensaje": "Idioma del sistema configurado en Español."
    },
    "en": {
        "codigo": "en",
        "nombre": "English",
        "mensaje": "System language set to English."
    },
    "pt": {
        "codigo": "pt",
        "nombre": "Português",
        "mensaje": "Idioma do sistema configurado em Português."
    }
}

CRONOLOGIA_ACTUALIZACIONES = {
    "Pre-Clásico / Alpha": ["Cerdo", "Oveja", "Zombi", "Creeper", "Esqueleto", "Araña", "Espada de Madera", "Espada de Piedra", "Arco"],
    "1.0 (Adventure Update)": ["Dragón del Ender", "Gato", "Ocelote", "Aldeano", "Poción"],
    "1.4 (Pretty Scary Update)": ["Wither", "Murciélago", "Bruja", "Esqueleto Wither"],
    "1.8 (Bountiful Update)": ["Guardián", "Guardián Anciano", "Conejo", "Endermite"],
    "1.9 (Combat Update)": ["Shulker", "Escudo", "Flechas espectrales", "Flechas con efecto"],
    "1.11 (Exploration Update)": ["Evocador", "Vengador", "Vex", "Llama"],
    "1.13 (Update Aquatic)": ["Ahogado", "Delfín", "Tortuga", "Fantasma", "Tridente"],
    "1.14 (Village & Pillage)": ["Saqueador", "Devastador", "Zorro", "Panda", "Ballesta"],
    "1.15 (Buzzy Bees)": ["Abeja"],
    "1.16 (Nether Update)": ["Piglin", "Hoglin", "Piglin Bruto", "Strider", "Espada de Netherite", "Pico de Netherite"],
    "1.17 / 1.18 (Caves & Cliffs)": ["Ajolote", "Calamar Brillante", "Cabra", "Catalejo"],
    "1.19 (The Wild Update)": ["Warden", "Rana", "Renacuajo", "Allay", "Brújula de recuperación"],
    "1.20 (Trails & Tales)": ["Sniffer", "Camello", "Pincel"],
    "1.21 (Tricky Trials)": ["Ánima (Breeze)", "Bogged", "Armadillo", "Maza (Mace)"]
}

@app.route('/idioma', methods=['GET'])
def seleccionar_idioma():
    """Ruta prompt-based para seleccionar entre English, Español y Português."""
    lang = request.args.get('lang', 'es').lower()
    if lang in SISTEMA_IDIOMAS:
        return jsonify(SISTEMA_IDIOMAS[lang])
    return jsonify({"error": "Idioma no soportado. Por favor usa lang=en, lang=es, o lang=pt"}), 400

@app.route('/cronologia', methods=['GET'])
def ruta_cronologia():
    """Ruta para visualizar el orden cronológico de entidades y arsenal según actualización."""
    html_respuesta = "<h1>Cronología de Actualizaciones (Mobs y Arsenal)</h1><ul>"
    for version, elementos in CRONOLOGIA_ACTUALIZACIONES.items():
        html_respuesta += f"<li><strong>{version}:</strong> {', '.join(elementos)}</li>"
    html_respuesta += "</ul><br><a href='/'>Volver al inicio</a>"
    return html_respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
