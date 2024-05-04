from DataCollector import DataCollector
from DataReader import DataReader
from DeforestationDetector import DeforestationDetector

import time

class AlgorithmExecutor:
    def __init__(self, data_holder) -> None:
        self.data_holder = data_holder

    def InitCollectData(self):
        self.dc = DataCollector(self.data_holder.roi, self.data_holder.date_from, self.data_holder.date_to)
        #self.dc.CollectData()
        time.sleep(5)
        return "-> Data collection is complete."
    
    def InitReadData(self):
        self.dr = DataReader(self.dc.file_paths)
        #self.dr.ReadData()
        time.sleep(5)
        return "-> Data reading is complete.\n"
    
    def InitTransferData(self):
        #self.dr.TransferData(self.data_holder)
        return "-> Data is initialized."
    
    def InitDeforestationDetection(self):
        self.dd = DeforestationDetector()

        time.sleep(5)

        # self.data_holder.asc_mean_before, self.data_holder.asc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.asc_images)
        # self.data_holder.desc_mean_before, self.data_holder.desc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.desc_images)

        # # Calculate RCR
        # self.data_holder.RCR_asc = self.dd.GetRadarChangeRatio(self.data_holder.asc_mean_before, self.data_holder.asc_mean_after)
        # self.data_holder.RCR_desc = self.dd.GetRadarChangeRatio(self.data_holder.desc_mean_before, self.data_holder.desc_mean_after)

        # # Detect deforestation
        # self.data_holder.deforested_image_asc = self.dd.DetectDeforestation(self.data_holder.RCR_asc, self.data_holder.asc_mean_after)
        # self.data_holder.deforested_image_desc = self.dd.DetectDeforestation(self.data_holder.RCR_desc, self.data_holder.desc_mean_after)

        # # Deforestation regions
        # self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_asc, self.data_holder.deforested_image_desc)
        # self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.asc_mean_after, self.data_holder.deforested_pixels_mask)

        # # Deforestation area
        # self.data_holder.deforested_pixels = self.dd.CountDeforestedPixels(self.data_holder.deforested_image_merged)
        # self.data_holder.deforested_area = self.dd.CalculateDeforestedArea(self.data_holder.deforested_pixels)

        return "-> Deforestation detection is complete."

    
    

    