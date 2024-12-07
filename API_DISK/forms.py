from django import forms
from urllib.parse import urlparse, parse_qs


class PublicKeyForm(forms.Form):
  CATEGORY_CHOICES = (
    ('all', 'Все'),
    ('archive', 'Архивы'),
    ('document', 'Документы'),
    ('image', 'Изображения'),
    ('media', 'Медиа файлы'),
    ('executable', "Исполняемые файлы")
  )

  public_key = forms.CharField(
    label='Публичная ссылка',
    max_length=256,
    help_text='Введите публичную ссылку на ресурс.',
    required=True
  )
  filter = forms.ChoiceField(
    label='Фильтр',
    choices=CATEGORY_CHOICES,
    help_text='Выберите тип файла для отображения'
  )
  max_files = forms.IntegerField(
    label='Максимум файлов',
    min_value=1,
    required=False,
    help_text='Введите максимальное кол-во файлов для отображения. Оставьте пустым для отображения всех файлов'
  )

# Функция извлечения public_key из ссылки.
  def clean_public_key(self):
    url = self.cleaned_data['public_key']

    # Логируем введенную ссылку
    # print(f"Введенная ссылка: {url}")

    try:
      parsed_url = urlparse(url)

      if "disk.yandex.ru" in parsed_url.netloc:
        if '/d/' in parsed_url.path:
          public_key = parsed_url.path.split('/d/')[-1]
        elif '/public/' in parsed_url.path:
          public_key = parsed_url.path.split('/public/')[-1]
        else:
          raise forms.ValidationError("Не удалось извлечь публичный ключ из ссылки.")

        if public_key:
          print(f"Извлеченный публичный ключ: {public_key}")
          return public_key
      else:
        raise forms.ValidationError("Некорректный домен. Ссылка должна вести на Яндекс.Диск.")

    except Exception as e:
      raise forms.ValidationError(f"Ошибка обработки ссылки: {e}")