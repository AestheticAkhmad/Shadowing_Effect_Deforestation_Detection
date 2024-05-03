import openeo
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self, roi = None, date_from = "", date_to = "") -> None:
        # Conncetion to the OpenEO API
        self.connection = openeo.connect("openeo.dataspace.copernicus.eu")
        self.connection.authenticate_oidc()

        # File paths for storage
        path = "data/"
        self.file_paths = [path + "asc_before.nc", path + "asc_after.nc", path + "desc_before.nc", path + "desc_after.nc"]

        # Request info
        self.roi = roi
        self.date_from = date_from
        self.date_to = date_to
        self.datacubes = [None] * 4

    def GetConvertedDate(self, date, direction = ""):
        if direction == "back":
            date_original = datetime.strptime(date, "%Y-%m-%d").date()
            days_to_sub = timedelta(days=90)
            date_original = date_original - days_to_sub
            date_from = date_original.strftime("%Y-%m-%d")
            return date_from
        elif direction == "forward":
            date_original = datetime.strptime(date, "%Y-%m-%d").date()
            days_to_add = timedelta(days=90)
            date_original = date_original + days_to_add
            date_to = date_original.strftime("%Y-%m-%d")
            return date_to

    def CollectData(self):
        self.datacubes[0] = self.connection.load_collection(
            "SENTINEL1_GRD",
            spatial_extent= self.roi,
            temporal_extent=[self.GetConvertedDate(self.date_from, "back"), self.date_from],
            bands=["VV"],
            properties=[
                openeo.collection_property("sat:orbit_state") == "ascending",
                openeo.collection_property("sar:instrument_mode") == "IW",
                openeo.collection_property("sar:pixel_spacing_range") == "10m",
            ]
        )

        self.datacubes[1] = self.connection.load_collection(
            "SENTINEL1_GRD",
            spatial_extent= self.roi,
            temporal_extent=[self.date_to, self.GetConvertedDate(self.date_to, "forward")],
            bands=["VV"],
            properties=[
                openeo.collection_property("sat:orbit_state") == "ascending",
                openeo.collection_property("sar:instrument_mode") == "IW",
                openeo.collection_property("sar:pixel_spacing_range") == "10m",
            ]
        )

        self.datacubes[2] = self.connection.load_collection(
            "SENTINEL1_GRD",
            spatial_extent= self.roi,
            temporal_extent=[self.GetConvertedDate(self.date_from, "back"), self.date_from],
            bands=["VV"],
            properties=[
                openeo.collection_property("sat:orbit_state") == "descending",
                openeo.collection_property("sar:instrument_mode") == "IW",
                openeo.collection_property("sar:pixel_spacing_range") == "10m",
            ]
        )

        self.datacubes[3] = self.connection.load_collection(
            "SENTINEL1_GRD",
            spatial_extent= self.roi,
            temporal_extent=[self.date_to, self.GetConvertedDate(self.date_to, "forward")],
            bands=["VV"],
            properties=[
                openeo.collection_property("sat:orbit_state") == "descending",
                openeo.collection_property("sar:instrument_mode") == "IW",
                openeo.collection_property("sar:pixel_spacing_range") == "10m",
            ]
        )

        for datacube, file_path in zip(self.datacubes, self.file_paths):
            gamma0_datacube = datacube.sar_backscatter(coefficient="gamma0-ellipsoid")
            gamma0_datacube.download(file_path, format="netCDF")
