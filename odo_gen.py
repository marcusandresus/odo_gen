import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "assets" / "profiles" / "default" / "config.json"
INPUT_PATTERN = re.compile(r"^\d+(?:\.\d)?$")


def hex_to_rgb(hex_str):
    """Convierte color hexadecimal a tupla RGB para Pillow."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def cargar_configuracion(config_path):
    if not config_path.exists():
        print(f"Error: No se encuentra el archivo de configuración '{config_path}'")
        return
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generar_odometro(numero_str, config_path=DEFAULT_CONFIG_PATH):
    conf = cargar_configuracion(config_path)
    if conf is None:
        return

    # 1. Validar formato de entrada: enteros con decimal opcional de un solo digito.
    if not INPUT_PATTERN.fullmatch(numero_str):
        print("Error: El formato debe ser numerico, con decimal opcional de un digito (ejemplos: 1234567 o 1234567.8)")
        return

    if "." in numero_str:
        enteros, decimal = numero_str.split(".")
    else:
        enteros, decimal = numero_str, "0"

    celdas_enteros = sorted(
        key for key in conf["celdas"] if key.startswith("entero_")
    )
    if len(enteros) > len(celdas_enteros):
        print(
            f"Error: El perfil solo soporta {len(celdas_enteros)} digitos enteros y se recibieron {len(enteros)}."
        )
        return

    profile_dir = config_path.parent

    # 2. Cargar Imagen Template (Desde el JSON)
    template_name = conf.get("archivo_fondo", "template.jpg")
    template_path = (profile_dir / template_name).resolve()
    if not template_path.exists():
        print(f"Error: No se encuentra el archivo de fondo '{template_path}'")
        return

    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Configurar Fuente y Color
    try:
        color = hex_to_rgb(conf["fuente"]["color_hex"])
        font_path = (profile_dir / conf["fuente"]["archivo"]).resolve()
        font = ImageFont.truetype(str(font_path), conf["fuente"]["size"])
    except Exception as e:
        print(f"Error al cargar fuente o color: {e}")
        return

    dx = conf["ajuste_texto"]["dx"]
    dy = conf["ajuste_texto"]["dy"]

    # --- LÓGICA DE IMPRESIÓN ---

    # Imprimir Decimal (Celda fija)
    if "decimal" in conf["celdas"]:
        c = conf["celdas"]["decimal"]
        # El texto se posiciona sumando el offset a la esquina superior izquierda (x_min, y_min)
        draw.text((c[0] + dx, c[1] + dy), decimal, font=font, fill=color)

    # Imprimir Enteros de derecha a izquierda (Alineado a la derecha)
    # Invertimos la cadena: '123' -> '321' para mapear a entero_1, entero_2...
    enteros_rev = enteros[::-1]

    for i in range(1, 9):
        key = f"entero_{i}"
        # Si la celda existe en el JSON y tenemos un dígito disponible para ella
        if key in conf["celdas"] and (i - 1) < len(enteros_rev):
            c = conf["celdas"][key]
            digito = enteros_rev[i - 1]
            draw.text((c[0] + dx, c[1] + dy), digito, font=font, fill=color)

    # 4. Guardar el resultado
    output_name = f"o_{numero_str}.jpg"
    img.save(output_name, "JPEG", quality=95)
    print(f"Imagen generada con éxito: {output_name}")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Uso: python odo_gen.py 1234567.8 [ruta_config.json]")
    else:
        config_path = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else DEFAULT_CONFIG_PATH
        generar_odometro(sys.argv[1], config_path)
