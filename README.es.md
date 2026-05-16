# SplitFolder — Herramienta inteligente para dividir carpetas de fotos

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.de.md">Deutsch</a>
</p>

---

Divide archivos de fotos (RAW, HIF, XMP, etc.) dentro de una carpeta en subcarpetas distribuidas uniformemente según los IDs de las fotos. Compatible con recursos compartidos SMB, modo de vista previa (dry-run) y redistribución de particiones existentes. Ideal para distribuir grandes colecciones de fotos en múltiples discos o ubicaciones de red.

## Características

- **Agrupación por foto** — Archivos con el mismo ID de foto (ej. `DSC00001.ARW`, `DSC00001.HIF`, `DSC00001.XMP`) se mantienen juntos
- **Ordenación natural** — `DSC2` va antes de `DSC10`, no lexicográficamente
- **Distribución uniforme** — Los grupos de fotos se distribuyen lo más equitativamente posible
- **Modo de vista previa** — Usa `--dry-run` para previsualizar sin mover archivos
- **Redistribución** — Las carpetas `part_*` existentes se detectan y pueden redistribuirse
- **Escaneo recursivo** — Opcionalmente, escanea todo el árbol de directorios
- **Compatible con SMB** — Usa `os.rename` en el mismo sistema de archivos, con respaldo de copia+eliminación entre dispositivos
- **Filtro de archivos basura de macOS** — Omite automáticamente `.DS_Store` y archivos `._*`
- **Protección contra duplicados** — Si un archivo ya existe, lo renombra a `xxx__dupN.ext`
- **Limpieza de carpetas vacías** — Elimina las carpetas `part_*` viejas y vacías

## Requisitos

- Python 3.7+

Sin dependencias externas — solo usa la biblioteca estándar.

## Instalación

```bash
git clone https://github.com/LeonJian/SplitFolder.git
cd SplitFolder
```

## Uso

```bash
python3 main.py /ruta/a/carpeta/origen -n 10
```

Divide todos los archivos de fotos en 10 subcarpetas: `part_001_*`, `part_002_*`, ..., `part_010_*`.

### Ejemplos básicos

```bash
# Dividir en 5 partes con vista previa
python3 main.py /Volumes/Media/DCIM -n 5 --dry-run

# Dividir en 20 partes con prefijo personalizado
python3 main.py /Volumes/Media/DCIM -n 20 --prefix lote_

# Escanear recursivamente todos los subdirectorios
python3 main.py /Volumes/Media/DCIM -n 10 --recursive

# Redistribuir carpetas part existentes (detectado por defecto)
python3 main.py /Volumes/Media/DCIM -n 40

# Omitir limpieza de carpetas vacías
python3 main.py /Volumes/Media/DCIM -n 10 --no-clean-empty
```

### Opciones de línea de comandos

| Opción | Valor predeterminado | Descripción |
|--------|---------------------|-------------|
| `source` | *(obligatorio)* | Ruta a la carpeta de origen |
| `-n, --parts` | *(obligatorio)* | Número de subcarpetas de destino |
| `--prefix` | `part_` | Prefijo para los nombres de las carpetas |
| `--recursive` | desactivado | Escanea recursivamente todo el árbol de directorios |
| `--dry-run` | desactivado | Solo vista previa — no mueve archivos |
| `--no-clean-empty` | desactivado | Omite la limpieza de carpetas `part_*` vacías |

## Cómo funciona

1. **Escanear** — Recopila todos los archivos de la carpeta de origen (y subdirectorios opcionales)
2. **Agrupar** — Agrupa archivos por su ID de foto (ej. `DSC00001.ARW` + `DSC00001.XMP` → grupo `DSC00001`)
3. **Ordenar** — Ordena los grupos usando ordenación numérica natural
4. **Distribuir** — Distribuye uniformemente los grupos en N carpetas de destino
5. **Mover** — Mueve los archivos a sus carpetas de destino, conservando los nombres
6. **Limpiar** — Elimina las carpetas `part_*` vacías antiguas

### Convención de nombres de carpetas

```
part_001_DSC00001-DSC00500/
part_002_DSC00501-DSC01000/
part_003_DSC01001-DSC01500/
...
```

Cada nombre de carpeta muestra el rango de IDs de fotos que contiene.

## Licencia

MIT License.
