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
