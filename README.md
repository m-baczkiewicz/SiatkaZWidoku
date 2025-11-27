# Siatka z widoku (QGIS Plugin)

Prosta wtyczka do QGIS generująca siatkę prostokątną dopasowaną do aktualnego zasięgu widoku mapy. Narzędzie zoptymalizowane do szybkiego planowania powierzchni (domyślnie działki 4 ha).

## Opis

Wtyczka pozwala jednym kliknięciem nałożyć na widoczny obszar mapy siatkę kwadratów o zadanym boku. [cite_start]Działa w trybie "nadpisywania" – każde kolejne uruchomienie usuwa poprzednią siatkę, co pozwala na dynamiczną pracę bez zaśmiecania projektu zbędnymi warstwami[cite: 1, 2].

### Główne funkcje:
* **Generowanie z widoku:** Siatka powstaje tylko tam, gdzie aktualnie patrzysz.
* [cite_start]**Domyślny wymiar 4 ha:** Domyślna wielkość oczka to 200x200 metrów, idealna do szacowania powierzchni 4 hektarów[cite: 1].
* **Automatyczna korekta układu (FIX):** Wtyczka wykrywa, jeśli mapa jest w stopniach (np. WGS 84) i automatycznie przelicza geometrię na metry (układ PUWG 1992 / EPSG:2180). Zapobiega to błędom generowania "gigantycznych kwadratów" przy pracy na podkładach OpenStreetMap/Google.
* [cite_start]**Czysta legenda:** Automatycznie usuwa starą warstwę *Siatka z widoku* przed wygenerowaniem nowej[cite: 2].

## Instalacja

1. Pobierz folder z wtyczką.
2. Umieść go w katalogu wtyczek QGIS:
   * **Windows:** `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\`
   * **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   * **Mac:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
3. Uruchom QGIS.
4. Wejdź w menu **Wtyczki** -> **Zarządzanie wtyczkami**.
5. Wyszukaj "Siatka z widoku" i zaznacz checkbox, aby ją aktywować.

## Jak używać

1. Ustaw widok mapy w QGIS na interesujący Cię obszar.
2. Kliknij ikonę wtyczki na pasku narzędzi (ikona siatki).
3. W oknie dialogowym podaj długość boku komórki w metrach (domyślnie `200`).
4. Zatwierdź – siatka zostanie dodana do projektu jako warstwa tymczasowa w pamięci.

## Informacje o wtyczce

* [cite_start]**Nazwa:** Siatka z widoku [cite: 2]
* [cite_start]**Wersja:** 1.1 [cite: 2]
* [cite_start]**Autor:** Michał Bączkiewicz [cite: 1, 2]
* [cite_start]**Kontakt:** michal.baczkiewicz05@gmail.com [cite: 2]
* [cite_start]**Data aktualizacji:** 2025-10-28 [cite: 1]
