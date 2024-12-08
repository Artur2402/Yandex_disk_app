from typing import Dict, Set


FILE_TYPE_MAPPING: Dict[str, Set[str]] = {
  "image": {"jpg", "jpeg", "png", "gif", "bmp", "tiff"},
  "document": {"pdf", "doc", "docs", "txt", "odt", "xls", "xlsx", "ppt", "pptx"},
  "archive": {"zip", "rar", "7z", "tar", "gz"},
  "media": {"mp3", "wav", "aac", "flac", "mp4", "mkv", "avi", "mov"},
  "executable": {"exe", "msi", "bat", "sh", "bin"}
}


def get_file_type(file_name: str) -> str:
  """Определяет тип файла на основании его расширения."""
  extension = file_name.rsplit('.', 1)[-1].lower()

  for file_name, extension in FILE_TYPE_MAPPING.items():
    if extension in extension:
      return file_name

  return "other"