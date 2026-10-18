# Вело-вселенная

Открытый справочник и виртуальная веломастерская на русском языке: история велосипеда, устройство и названия деталей, типы велосипедов, инструмент, производители, сборка своими руками и пошаговые инструкции по ремонту.

Сайт: https://avtomaster24bot-lab.github.io/velo-universe/

## Как устроено
- `content/` — весь текст в виде структурированных данных (Python-модули): `parts.py`, `toollist.py`, `guides.py`, `biketypes.py`, `history.py`, `makers.py`, `buildguide.py`, `glossary.py`, статьи `art_compat.py`, `art_susp_ebike.py`, `art_other.py`, `round3.py` (неисправности, бескамерка, прокачка, моменты, чек-лист, таблица Cateye), `credits.json` (источники фото). Калькуляторы — `site/js/calc.js`.
- Ссылки внутри текста пишутся как `[[part:chain|цепь]]`, `[[tool:chain-tool]]`, `[[guide:nexus-tube]]`, `[[type:mtb]]`, `[[page:history]]` — сборщик проверяет, что цель существует.
- `tools/build.py` — генерирует статический сайт в `site/` (HTML + поисковый индекс `search.json`).
- `tools/svgs.py` — собственные SVG-схемы (анатомия, геометрия, трансмиссия, колесо, втулка, вилка/Lefty, планетарная передача).
- `tools/fetch.py` — скачивает фото с Wikimedia Commons, уменьшает в WebP и записывает автора/лицензию.
- `tools/checklinks.py` — проверка битых ссылок.

```
python3 tools/build.py && python3 tools/checklinks.py site
```
Публикация: GitHub Actions выкладывает папку `site/` на GitHub Pages при каждом push в `main`.

Фото — Wikimedia Commons (PD / CC0 / CC BY / CC BY-SA), авторы и лицензии на странице «Источники». Тексты инструкций справочные — моменты затяжки и порядок работ сверяйте с мануалом производителя.
