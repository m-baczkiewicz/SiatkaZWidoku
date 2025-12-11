# -*- coding: utf-8 -*-
"""
QGIS Plugin: Siatka z widoku
Autor: Michał Bączkiewicz
Data: 2025-10-28
Opis: Plugin generujący siatkę prostokątną z aktualnego widoku mapy.
Naprawa: Obsługa układów współrzędnych (automatyczna konwersja na metry).
"""

import os 
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QInputDialog
from qgis.PyQt.QtGui import QIcon
from qgis.core import (
    QgsRectangle, QgsProject, QgsGeometry, QgsFeature, 
    QgsFields, QgsField, QgsVectorLayer, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsUnitTypes
)

class SiatkaZWidokuPlugin:

    LAYER_NAME = "Siatka z widoku"  # Stała nazwa warstwy

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        # Poprawka: Szukamy icon.jpg, bo taki plik jest w folderze, mimo że kod szukał png
        icon_path = os.path.join(os.path.dirname(__file__), "icon.jpg")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
            
        self.action = QAction(QIcon(icon_path), "Generuj siatkę z widoku", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Siatka z widoku", self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("Siatka z widoku", self.action)

    def remove_old_grid(self):
        """Usuwa starą warstwę siatki jeśli istnieje"""
        project = QgsProject.instance()
        layers_to_remove = []

        for layer in project.mapLayers().values():
            if layer.name() == self.LAYER_NAME:
                layers_to_remove.append(layer.id())

        # Usuń znalezione warstwy
        if layers_to_remove:
            project.removeMapLayers(layers_to_remove)

    def run(self):
        try:
            canvas = self.iface.mapCanvas()
            
            # Pobierz aktualne ustawienia mapy
            canvas_crs = canvas.mapSettings().destinationCrs()
            canvas_extent = canvas.extent()
            
            # Domyślny układ do generowania siatki to układ widoku
            grid_crs = canvas_crs
            working_extent = canvas_extent
            
            # Niezależnie czy podkład to WGS84, Google Mercator czy inny - siatkę generujemy w 1992.
            target_crs = QgsCoordinateReferenceSystem("EPSG:2180")
            
            # Jeśli układ widoku jest inny niż 1992, wykonujemy transformację zasięgu
            if canvas_crs != target_crs:
                transform = QgsCoordinateTransform(canvas_crs, target_crs, QgsProject.instance())
                working_extent = transform.transformBoundingBox(canvas_extent)
                grid_crs = target_crs
            else:
                # Jeśli już jesteśmy w 1992, bierzemy dane wprost
                working_extent = canvas_extent
                grid_crs = canvas_crs

            # Dialog dla rozmiaru komórki
            cell_size, ok = QInputDialog.getDouble(
                self.iface.mainWindow(), 
                "Rozmiar komórki", 
                "Podaj rozmiar komórki w metrach (np. 200 dla 4ha):", 
                200, 1, 10000, 2
            )
            if not ok:
                return

            # USUŃ STARĄ SIATKĘ przed utworzeniem nowej
            self.remove_old_grid()

            # Obliczenia na siatce (teraz na pewno w metrach)
            xmin = int(working_extent.xMinimum() / cell_size) * cell_size
            ymin = int(working_extent.yMinimum() / cell_size) * cell_size
            xmax = int(working_extent.xMaximum() / cell_size + 1) * cell_size
            ymax = int(working_extent.yMaximum() / cell_size + 1) * cell_size

            # Utwórz warstwę w odpowiednim układzie (grid_crs)
            layer = QgsVectorLayer(
                f"Polygon?crs={grid_crs.authid()}", 
                self.LAYER_NAME,
                "memory"
            )
            provider = layer.dataProvider()

            # Dodaj pola
            fields = QgsFields()
            fields.append(QgsField('id', QVariant.Int))
            fields.append(QgsField('col', QVariant.Int))
            fields.append(QgsField('row', QVariant.Int))
            # Dodatkowe pola informacyjne
            fields.append(QgsField('area_ha', QVariant.Double)) 
            provider.addAttributes(fields)
            layer.updateFields()

            # Generuj komórki
            features = []
            feature_id = 0
            row_num = 0

            y = ymax
            while y > ymin:
                col_num = 0
                x = xmin
                while x < xmax:
                    rect = QgsRectangle(x, y - cell_size, x + cell_size, y)
                    geometry = QgsGeometry.fromRect(rect)
                    feature = QgsFeature()
                    feature.setGeometry(geometry)
                    
                    # Oblicz powierzchnię w hektarach dla pewności
                    area_ha = (cell_size * cell_size) / 10000.0
                    
                    feature.setAttributes([
                        feature_id, col_num, row_num, area_ha
                    ])
                    features.append(feature)
                    feature_id += 1
                    col_num += 1
                    x += cell_size
                row_num += 1
                y -= cell_size

            # Dodaj features do warstwy
            provider.addFeatures(features)
            layer.updateExtents()
            QgsProject.instance().addMapLayer(layer)

            # Informacja dla użytkownika
            msg = f"Wygenerowano {feature_id} komórek o boku {cell_size}m."
            if canvas_crs.isGeographic():
                msg += " (Przeliczono automatycznie na układ EPSG:2180)"
                
            self.iface.messageBar().pushMessage(
                "Sukces", 
                msg, 
                level=0,  # INFO
                duration=4
            )

        except Exception as e:
            QMessageBox.critical(
                self.iface.mainWindow(), 
                "Błąd", 
                f"Wystąpił błąd: {str(e)}"
            )
