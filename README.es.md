# SplitFolder — Herramienta para dividir carpetas grandes

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a> | <a href="README.de.md">Deutsch</a>
</p>

---

Divide archivos en carpetas grandes con demasiados archivos en subcarpetas distribuidas uniformemente por nombre — creado para resolver el problema de carpetas tan grandes que Finder / Explorer tardan en cargar. Funciona con cualquier tipo de archivo: fotos, documentos, archivos comprimidos, registros, conjuntos de datos, etc. Compatible con recursos compartidos SMB, modo de vista previa y redistribución de particiones existentes.

## Características

- **Agrupación por nombre** — Archivos con el mismo prefijo+número (ej. `report_001.pdf`, `report_001.xlsx`) se mantienen juntos
- **Ordenación natural** — `file2` va antes de `file10`, no lexicográficamente
- **Distribución uniforme** — Los grupos se distribuyen lo más equitativamente posible
- **Modo de vista previa** — Usa `--dry-run` para previsualizar sin mover archivos
- **Redistribución** — Las carpetas `part_*` existentes se detectan y pueden redistribuirse
- **Escaneo recursivo** — Opcionalmente, escanea todo el árbol de directorios
- **Compatible con SMB** — Usa `os.rename` en el mismo sistema de archivos, con respaldo de copia+eliminación entre dispositivos
- **Filtro de archivos basura de macOS** — Omite automáticamente `.DS_Store` y archivos `._*`
- **Protección contra duplicados** — Si un archivo ya existe, lo renombra a `xxx__dupN.ext`
- **Limpieza de carpetas vacías** — Elimina las carpetas `part_*` viejas y vacías

## Casos de uso

- **Carpetas grandes** — ¿Una carpeta con más de 10,000 archivos que tarda en abrirse? Divídela en partes más pequeñas.
- **Colecciones de fotos** — Distribuye archivos RAW/ARW/HIF/XMP en múltiples discos o ubicaciones de red.
- **Archivos de registro** — Particiona millones de logs por rango de nombre para facilitar la navegación.
- **Preparación de datasets** — Divide datos de entrenamiento en shards balanceados.
- **Cualquier carpeta plana grande** — Si una carpeta es demasiado grande para cargar, SplitFolder puede ayudar.

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
python3 main.py /ruta/a/carpeta/grande -n 10
```

Divide todos los archivos en 10 subcarpetas: `part_001_*`, `part_002_*`, ..., `part_010_*`.

### Ejemplos básicos

```bash
# Dividir en 5 partes con vista previa
python3 main.py /Volumes/Data/Archive -n 5 --dry-run

# Dividir en 20 partes con prefijo personalizado
python3 main.py /Volumes/Data/Archive -n 20 --prefix lote_

# Escanear recursivamente todos los subdirectorios
python3 main.py /Volumes/Data/Archive -n 10 --recursive

# Redistribuir carpetas part existentes (detectado por defecto)
python3 main.py /Volumes/Data/Archive -n 40

# Omitir limpieza de carpetas vacías
python3 main.py /Volumes/Data/Archive -n 10 --no-clean-empty
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
2. **Agrupar** — Agrupa archivos por prefijo+número (ej. `report_001.pdf` + `report_001.xlsx` → grupo `report_001`)
3. **Ordenar** — Ordena los grupos usando ordenación numérica natural
4. **Distribuir** — Distribuye uniformemente los grupos en N carpetas de destino
5. **Mover** — Mueve los archivos a sus carpetas de destino, conservando los nombres
6. **Limpiar** — Elimina las carpetas `part_*` vacías antiguas

### Convención de nombres de carpetas

```
part_001_report_0001-report_0500/
part_002_report_0501-report_1000/
part_003_report_1001-report_1500/
...
```

Cada nombre de carpeta muestra el rango de grupos de archivos que contiene.

## Licencia

[Apache License 2.0](LICENSE)
