from pathlib import Path


REGISTER_EXTENSIONS = {'Images': ['JPEG', 'PNG', 'JPG', 'SVG', 'GIF', 'ICO'],
                       'Audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC', 'WMA'],
                       'Video': ['AVI', 'MP4', 'MOV', 'MKV', 'WMV'],
                       'Documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF'],
                       'Programs': ['BAT', 'CMD', 'EXE', 'C', 'CPP', 'JS', 'PY', 'VBS'],
                       'Archives': ['ZIP', 'GZ', 'TAR', 'RAR', '7Z', 'ARJ']
                       }


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def file_type(ext: str) -> str:
    for key, list_value in REGISTER_EXTENSIONS.items():
        if ext in list_value:
            return key
    else:
        return 'Others'


