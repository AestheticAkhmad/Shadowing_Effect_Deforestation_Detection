from DataCollector import DataCollector
from DataReader import DataReader
from DeforestationDetector import DeforestationDetector
import matplotlib
matplotlib.use('Agg')
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import numpy as np

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
        self.dr.ReadData()
        #time.sleep(5)
        return "-> Data reading is complete.\n"
    
    def InitTransferData(self):
        self.dr.TransferData(self.data_holder)
        return "-> Data is initialized."
    
    def InitDeforestationDetection(self):
        self.dd = DeforestationDetector()

        # Calculate average backscatter
        self.data_holder.asc_mean_before, self.data_holder.asc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.asc_images)
        self.data_holder.desc_mean_before, self.data_holder.desc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.desc_images)
        self.data_holder.asc_mean_after_original = np.copy(self.data_holder.asc_mean_after)
        self.data_holder.desc_mean_after_original = np.copy(self.data_holder.desc_mean_after)

        # Apply denoise filter
        self.data_holder.asc_mean_before = self.dd.ApplyDenoise(self.data_holder.asc_mean_before)
        self.data_holder.asc_mean_after = self.dd.ApplyDenoise(self.data_holder.asc_mean_after)
        self.data_holder.desc_mean_before = self.dd.ApplyDenoise(self.data_holder.desc_mean_before)
        self.data_holder.desc_mean_after = self.dd.ApplyDenoise(self.data_holder.desc_mean_after)

        # Calculate RCR
        self.data_holder.RCR_asc = self.dd.GetRadarChangeRatio(self.data_holder.asc_mean_before, self.data_holder.asc_mean_after)
        self.data_holder.RCR_desc = self.dd.GetRadarChangeRatio(self.data_holder.desc_mean_before, self.data_holder.desc_mean_after)

        # Detect deforestation
        self.data_holder.deforested_image_asc = self.dd.DetectDeforestation(self.data_holder.RCR_asc, self.data_holder.asc_mean_after_original)
        self.data_holder.deforested_image_desc = self.dd.DetectDeforestation(self.data_holder.RCR_desc, self.data_holder.desc_mean_after_original)

        # Deforestation regions
        self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_asc, self.data_holder.deforested_image_desc)
        self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.asc_mean_after_original, self.data_holder.deforested_pixels_mask)

        # Deforestation area
        self.data_holder.deforested_pixels = self.dd.CountDeforestedPixels(self.data_holder.deforested_image_merged)
        self.data_holder.deforested_area = self.dd.CalculateDeforestedArea(self.data_holder.deforested_pixels)

        return "-> Deforestation detection is complete."
    
    def InitResults(self, images_frame, results_info):
        self.GeneratePlot()
        #self.GenerateHistogram()
        return "-> Results and plots are ready."
    
    def GeneratePlot(self):
        f, axarr = plt.subplots(1,3, figsize=(15, 5))

        axarr[0].set_title("Before deforestation")
        axarr[1].set_title("After deforestation")
        axarr[2].set_title("Detected deforestation")

        self.data_holder.asc_images[1] = np.stack([self.data_holder.asc_images[1]]*3, axis=-1)
        self.data_holder.asc_images[7] = np.stack([self.data_holder.asc_images[7]]*3, axis=-1)

        f.suptitle("Shadowing effect deforestation detection", fontsize=16, y=0.95)
        axarr[0].imshow(self.data_holder.asc_images[1], cmap='gray')
        axarr[1].imshow(self.data_holder.asc_images[7], cmap='gray')
        axarr[2].imshow(self.data_holder.deforested_image_merged)

        for ax in axarr:
            formatter = ScalarFormatter(useMathText=True)
            formatter.set_scientific(True)
            formatter.set_powerlimits((-1,1))
            
            ax.xaxis.set_major_formatter(formatter)
            ax.yaxis.set_major_formatter(formatter)

        axarr[0].set_ylabel("Height")
        f.text(0.5, 0.05, 'Width', ha='center')

        f.subplots_adjust(wspace=0.25)
        f.savefig('plot.png', dpi=500)
    
    

    