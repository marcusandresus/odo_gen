# odo_gen

Generador simple de imagenes de odometro a partir de una plantilla y un perfil de configuracion.

## Estructura

- `assets/profiles/default/`: perfil versionado que mantiene juntos `config.json` y su `template.png`.
- `assets/fonts/`: fuentes compartidas entre perfiles.
- `odo_gen.py`: script principal. Por defecto usa `assets/profiles/default/config.json`.

La idea es que cada perfil viva en su propia carpeta para evitar que el `config.json` quede desacoplado del template al que pertenece.

## Uso

```bash
python3 odo_gen.py 1234567.8
python3 odo_gen.py 1234567.8 assets/profiles/default/config.json
```

El formato soportado es `enteros.decimal`, con exactamente un decimal y hasta la cantidad de digitos definida por el perfil.

Tambien se acepta el formato sin decimal, que se interpreta como decimal `0`:

```bash
python3 odo_gen.py 1234567
```

## Instalacion En Windows

La release publica actual esta en GitHub:

- `https://github.com/marcusandresus/odo_gen/releases/tag/v0.1.0`

El artefacto distribuible es `odo_gen-v0.1.0-win64.zip`. Como el build fue generado en modo `onedir`, no debes extraer solo `odo_gen.exe`; debes conservar la carpeta completa con `_internal`.

Instalacion sugerida:

1. Extraer el ZIP en `C:\tools\misc\odo_gen`.
2. Crear `C:\Users\marco\bin\odo_gen.cmd` con este contenido:

```bat
@echo off
"C:\tools\misc\odo_gen\odo_gen.exe" %*
```

Si `C:\Users\marco\bin` esta en tu `PATH`, luego puedes ejecutar:

```bat
odo_gen 1234567
odo_gen 1234567.8
```
