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
    def __init__(self, data_holder, orbits_available) -> None:
        self.data_holder = data_holder
        self.orbits_available = orbits_available

    def InitCollectData(self):
        self.dc = DataCollector(self.data_holder.roi, self.data_holder.date_from, self.data_holder.date_to)
        self.dc.CollectData()
        return "-> Data collection is complete."
    
    def InitReadData(self):
        self.dr = DataReader(self.dc.file_paths)
        self.dr.ReadData()
        return "-> Data reading is complete.\n"
    
    def InitTransferData(self):
        self.dr.TransferData(self.data_holder)
        return "-> Data is initialized."
    
    def CalculateForBothOrbits(self):
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


    def CalculateForAscOrbit(self):
        # Calculate average backscatter
        self.data_holder.asc_mean_before, self.data_holder.asc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.asc_images)
        self.data_holder.asc_mean_after_original = np.copy(self.data_holder.asc_mean_after)

        # Apply denoise filter
        self.data_holder.asc_mean_before = self.dd.ApplyDenoise(self.data_holder.asc_mean_before)
        self.data_holder.asc_mean_after = self.dd.ApplyDenoise(self.data_holder.asc_mean_after)

        # Calculate RCR
        self.data_holder.RCR_asc = self.dd.GetRadarChangeRatio(self.data_holder.asc_mean_before, self.data_holder.asc_mean_after)

        # Detect deforestation
        self.data_holder.deforested_image_asc = self.dd.DetectDeforestation(self.data_holder.RCR_asc, self.data_holder.asc_mean_after_original)

        # Deforestation regions
        self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_asc, self.data_holder.deforested_image_asc)

        # Deforestation image
        self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.asc_mean_after_original, self.data_holder.deforested_pixels_mask)


    def CalculateForDescOrbit(self):
        # Calculate average backscatter
        self.data_holder.desc_mean_before, self.data_holder.desc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.desc_images)
        self.data_holder.desc_mean_after_original = np.copy(self.data_holder.desc_mean_after)

        # Apply denoise filter
        self.data_holder.desc_mean_before = self.dd.ApplyDenoise(self.data_holder.desc_mean_before)
        self.data_holder.desc_mean_after = self.dd.ApplyDenoise(self.data_holder.desc_mean_after)

        # Calculate RCR
        self.data_holder.RCR_desc = self.dd.GetRadarChangeRatio(self.data_holder.desc_mean_before, self.data_holder.desc_mean_after)

        # Detect deforestation
        self.data_holder.deforested_image_desc = self.dd.DetectDeforestation(self.data_holder.RCR_desc, self.data_holder.desc_mean_after_original)

        # Deforestation regions
        self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_desc, self.data_holder.deforested_image_desc)

        # Deforestation image
        self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.desc_mean_after_original, self.data_holder.deforested_pixels_mask)


    def InitDeforestationDetection(self):
        self.dd = DeforestationDetector()

        # Calculate average backscatter
        if self.orbits_available == 'both':
            self.CalculateForBothOrbits()

        elif self.orbits_available == 'asc':
            self.CalculateForAscOrbit()

        elif self.orbits_available == 'desc':
            self.CalculateForDescOrbit()

        # Deforestation area
        self.data_holder.deforested_pixels = self.dd.CountDeforestedPixels(self.data_holder.deforested_image_merged)
        self.data_holder.deforested_area = self.dd.CalculateDeforestedArea(self.data_holder.deforested_pixels)

        return "-> Deforestation detection is complete."
    
    def InitResults(self, images_frame, results_info):
        self.GeneratePlot()
        self.GenerateHistogram()
        print("Deforested pixels: ", self.data_holder.deforested_pixels)
        print("Deforested area: ", self.data_holder.deforested_area)
        return "-> Results and plots are ready."
    
    def GenerateHistogram(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

        # Ascending orbit histogram
        ax1.hist(self.data_holder.RCR_asc.flatten(), bins=100, alpha=0.85)
        ax1.set_title('Ascending Orbit')
        ax1.set_xlabel('Value (dB)')
        ax1.set_ylabel('Frequency (Pixels)')

        # Descending orbit histogram
        ax2.hist(self.data_holder.RCR_desc.flatten(), bins=100, alpha=0.85)
        ax2.set_title('Descending Orbit')
        ax2.set_xlabel('Value (dB)')

        ax1.set_xlim(-10, 10)
        ax2.set_xlim(-10, 10)

        tick_step = 2
        # Assuming `data_asc` and `data_desc` cover the range you expect for your data
        # Replace `min_value` and `max_value` with actual min and max values if necessary
        # min_value = min(self.RCR_asc.min(), self.RCR_desc.min())
        # max_value = max(self.RCR_asc.max(), self.RCR_desc.max())

        ticks = np.arange(-10, 11, tick_step) 

        # Generate a range of tick values
        # ticks = np.arange(np.floor(min_value / tick_step) * tick_step, 
        #                 np.ceil(max_value / tick_step) * tick_step + tick_step, 
        #                 tick_step)

        # Apply the ticks to both subplots
        ax1.set_xticks(ticks)
        ax2.set_xticks(ticks)

        # Set the formatter for the y-axis
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-1, 1))
        ax1.yaxis.set_major_formatter(formatter)

        self.hist_name = f'hist-{self.data_holder.date_from}_' + f'{self.data_holder.date_to}.png'
        fig.savefig(self.hist_name, dpi=500)

        # Adjust the layout and display the plot
        #plt.tight_layout()
        #plt.show()
    
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
        self.plot_name = f'plot-{self.data_holder.date_from}_' + f'{self.data_holder.date_to}.png'
        f.savefig(self.plot_name, dpi=500)
    
    

    