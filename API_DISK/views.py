from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseBadRequest
import logging

from .api import get_public_file
from .forms import PublicKeyForm
from .utils import get_file_type

# Инициализация логгера для отслеживания ошибок
logger = logging.getLogger(__name__)


def file_list_view(request):
	form = PublicKeyForm(request.POST or None)
	files = []

	if request.method == "POST" and form.is_valid():
		public_key = form.cleaned_data["public_key"]
		file_type = form.cleaned_data["filter"]

		# Логируем публичный ключ и выбранный фильтр
		logger.info(f"Public key: {public_key}, File type: {file_type}")

		# Проверяем кэш
		cache_key = f"yandex_disk_files_{public_key}"
		files = cache.get(cache_key)

		if files is None:
			# Попытка получить данные через API
			data = get_public_file(public_key)

			# Проверка наличия ошибки
			if "error" in data:
				logger.error(f"Ошибка API: {data['error']}")
				return HttpResponseBadRequest(f"Ошибка API: {data['error']}")

			# Проверяем на наличие файлов в ответе
			if "_embedded" in data:
				files = data["_embedded"]["items"]
				cache.set(cache_key, files, timeout=600)
			else:
				logger.error("Пустой ответ от API или данные не содержат файлов")
				return HttpResponseBadRequest("Не удалось получить файлы с Яндекс.Диска")

		# Фильтрация файлов
		if file_type != "all" and files:
			files = [file for file in files if file_type == get_file_type(file["name"])]

	return render(
		request,
		"./file_list.html",
		{"form": form, "files": files},
	)