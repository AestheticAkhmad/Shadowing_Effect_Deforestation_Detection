from DataCollector import DataCollector
from DataReader import DataReader
from DeforestationDetector import DeforestationDetector
import matplotlib
matplotlib.use('Agg')
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import numpy as np
import imageio
import tkinter as tk


from PIL import Image, ImageTk

class AlgorithmExecutor:
    def __init__(self, data_holder, polarization, folder) -> None:
        self.data_holder = data_holder
        self.orbits_available = None
        self.polarization = polarization
        self.folder = folder

    def InitCollectData(self):
        self.dc = DataCollector(self.data_holder.roi, self.data_holder.date_from, self.data_holder.date_to, self.folder)
        
        print(self.data_holder.roi)

        self.dc.CollectData()

        return "-> Data collection is complete."
    
    def InitReadData(self):
        #temp_paths = ['test_12/asc_before.nc', 'test_12/asc_after.nc', 'test_12/desc_before.nc', 'test_12/desc_after.nc']
        #temp_paths = ['test_12/desc_before.nc', 'test_12/desc_after.nc']
        #self.dr = DataReader(temp_paths, self.polarization)
        self.dr = DataReader(self.dc.file_paths, self.polarization)
        self.dr.ReadData()

        return "-> Data reading is complete.\n"
    
    def InitTransferData(self):
        self.orbits_available = self.dr.TransferData(self.data_holder)
        return "-> Data is initialized."

    def CalculateForAscOrbit(self):
        # Calculate average backscatter
        self.data_holder.asc_mean_before, self.data_holder.asc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.asc_images)
        self.data_holder.asc_mean_before_original = np.copy(self.data_holder.asc_mean_before)
        self.data_holder.asc_mean_after_original = np.copy(self.data_holder.asc_mean_after)

        self.data_holder.asc_mean_before = self.dd.NormalizeImage(self.data_holder.asc_mean_before)
        self.data_holder.asc_mean_after = self.dd.NormalizeImage(self.data_holder.asc_mean_after)

        # Apply denoise filter
        self.data_holder.asc_mean_before = self.dd.ApplyDenoise(self.data_holder.asc_mean_before)
        self.data_holder.asc_mean_after = self.dd.ApplyDenoise(self.data_holder.asc_mean_after)

        # Calculate RCR
        self.data_holder.RCR_asc = self.dd.GetRadarChangeRatio(self.data_holder.asc_mean_before, self.data_holder.asc_mean_after)

        # Detect deforestation
        self.data_holder.deforested_image_asc = self.dd.DetectDeforestation(self.data_holder.RCR_asc, self.data_holder.asc_mean_after)

        # Deforestation regions
        self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_asc, self.data_holder.deforested_image_asc)

        # Deforestation image
        self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.asc_mean_after_original, self.data_holder.deforested_pixels_mask)


    def CalculateForDescOrbit(self):
        # Calculate average backscatter
        self.data_holder.desc_mean_before, self.data_holder.desc_mean_after = self.dd.GetAverageBackscatter(self.data_holder.desc_images)
        self.data_holder.desc_mean_before_original = np.copy(self.data_holder.desc_mean_before)
        self.data_holder.desc_mean_after_original = np.copy(self.data_holder.desc_mean_after)

        self.data_holder.desc_mean_before = self.dd.NormalizeImage(self.data_holder.desc_mean_before)
        self.data_holder.desc_mean_after = self.dd.NormalizeImage(self.data_holder.desc_mean_after)

        # Apply denoise filter
        self.data_holder.desc_mean_before = self.dd.ApplyDenoise(self.data_holder.desc_mean_before)
        self.data_holder.desc_mean_after = self.dd.ApplyDenoise(self.data_holder.desc_mean_after)

        # Calculate RCR
        self.data_holder.RCR_desc = self.dd.GetRadarChangeRatio(self.data_holder.desc_mean_before, self.data_holder.desc_mean_after)

        # Detect deforestation
        self.data_holder.deforested_image_desc = self.dd.DetectDeforestation(self.data_holder.RCR_desc, self.data_holder.desc_mean_after)

        # Deforestation regions
        self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_desc, self.data_holder.deforested_image_desc)

        # Deforestation image
        self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.desc_mean_after_original, self.data_holder.deforested_pixels_mask)


    def InitDeforestationDetection(self):
        self.dd = DeforestationDetector()

        # Calculate average backscatter
        if self.orbits_available == 'both':
            self.CalculateForAscOrbit()
            self.CalculateForDescOrbit()
            
            self.data_holder.mean_after_original = self.dd.CalculateMean(self.data_holder.asc_mean_after_original, self.data_holder.desc_mean_after_original)

            self.data_holder.deforested_pixels_mask = self.dd.GetDeforestedPixels(self.data_holder.deforested_image_asc, self.data_holder.deforested_image_desc)
            
            self.data_holder.deforested_image_merged = self.dd.MergeDeforestedImages(self.data_holder.mean_after_original, self.data_holder.deforested_pixels_mask)
  
        elif self.orbits_available == 'asc':
            self.CalculateForAscOrbit()

        elif self.orbits_available == 'desc':
            self.CalculateForDescOrbit()

        # Deforestation area
        self.data_holder.deforested_pixels = self.dd.CountDeforestedPixels(self.data_holder.deforested_image_merged)
        self.data_holder.deforested_area = self.dd.CalculateDeforestedArea(self.data_holder.deforested_pixels)
        print("Deforested area: ", self.data_holder.deforested_area)
        

        return "-> Deforestation detection is complete."
    
    def InitResults(self, canvas, results_info):
        self.GeneratePlot()
        self.SaveDeforestedImage()
        self.PlotDeforestedImage(canvas)
        self.PlotResultsInfo(results_info)
        #self.GenerateHistogram()
        return "-> Results and plot are ready."

    def PlotDeforestedImage(self, canvas):
        plot_path = self.plot_name  # Replace with the path to your image file
        plot = Image.open(plot_path)
        plot_width, image_height = plot.size
        plot_image = ImageTk.PhotoImage(plot)
    
        canvas.create_image(0, 0, image=plot_image, anchor='nw')
        canvas.image = plot_image

        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    def PlotResultsInfo(self, results_info):
        info  = f'Date from    : {self.data_holder.date_from}\n'
        info += f'Date to      : {self.data_holder.date_to}\n'
        info += f'-----------------------------\n'
        info += f"ROI     west : {self.data_holder.roi['west']}\n"
        info += f"       south : {self.data_holder.roi['south']}\n"
        info += f"        east : {self.data_holder.roi['east']}\n"
        info += f"       north : {self.data_holder.roi['north']}\n"
        info += f'-----------------------------\n'
        info += f'Deforestation: {self.data_holder.deforested_area} km^2\n'
        results_info.config(text=info)


    def SaveDeforestedImage(self):
        rgb_deforested_uint8 = self.data_holder.deforested_image_merged.astype(np.uint8)
        imageio.imwrite(f'{self.folder}/{self.data_holder.date_from}sdd_rgb_deforested.png', rgb_deforested_uint8)

    def GenerateHistogram(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

        if self.orbits_available == 'asc' or self.orbits_available == 'both':
            # Ascending orbit histogram
            ax1.hist(self.data_holder.RCR_asc.flatten(), bins=100, alpha=0.85)
            ax1.set_title('Ascending Orbit')
            ax1.set_xlabel('Value (dB)')
            ax1.set_ylabel('Frequency (Pixels)')

        if self.orbits_available == 'desc' or self.orbits_available == 'both':
            # Descending orbit histogram
            ax2.hist(self.data_holder.RCR_desc.flatten(), bins=100, alpha=0.85)
            ax2.set_title('Descending Orbit')
            ax2.set_xlabel('Value (dB)')

        ax1.set_xlim(-10, 10)
        ax2.set_xlim(-10, 10)

        tick_step = 2
        ticks = np.arange(-10, 11, tick_step) 

        # Apply the ticks to both subplots
        ax1.set_xticks(ticks)
        ax2.set_xticks(ticks)

        # Set the formatter for the y-axis
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-1, 1))
        ax1.yaxis.set_major_formatter(formatter)

        #self.hist_name = f'test_plots/hist-{self.data_holder.date_from}_' + f'{self.data_holder.date_to}.png'
        fig.savefig(self.hist_name, dpi=500)

    
    def GeneratePlot(self):
        f, axarr = plt.subplots(1,3, figsize=(10, 4))

        axarr[0].set_title("Before deforestation")
        axarr[1].set_title("After deforestation")
        axarr[2].set_title("Detected deforestation")

        before_stacked = None
        after_stacked = None

        if self.orbits_available == 'desc':
            before_stacked = np.stack([self.data_holder.desc_mean_before_original]*3, axis=-1)
            after_stacked = np.stack([self.data_holder.desc_mean_after_original]*3, axis=-1)
            rcr = np.stack([self.data_holder.RCR_desc]*3, axis=-1)
            
        else:
            before_stacked = np.stack([self.data_holder.asc_mean_before_original]*3, axis=-1)
            after_stacked = np.stack([self.data_holder.asc_mean_after_original]*3, axis=-1)
            rcr = np.stack([self.data_holder.RCR_asc]*3, axis=-1)

        f.suptitle(f"Shadowing effect deforestation detection ({self.dr.polarization})", fontsize=16)
        axarr[0].imshow(before_stacked, cmap='gray')
        axarr[1].imshow(after_stacked, cmap='gray')
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
        self.plot_name = f'{self.folder}/deforestation_plot.png'
        f.savefig(self.plot_name, dpi=150)
        f.savefig(f'{self.folder}/deforestation_plot_hr.png', dpi=500)
    