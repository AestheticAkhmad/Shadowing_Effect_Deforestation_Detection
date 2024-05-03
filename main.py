from DataCollector import DataCollector
from DataReader import DataReader
from DataHolder import DataHolder
from DeforestationDetector import DeforestationDetector

from DeforestationApplication import DeforestationApplication

import matplotlib.pyplot as plt
import numpy as np

# roi = {"west": 13.76, "south": 52.37, "east": 13.84, "north": 52.42}
# date_from = "2016-07-15"
# date_to = "2021-07-15"

# collector = DataCollector(roi, date_from, date_to)
# #collector.CollectData()

# reader = DataReader(collector.file_paths)
# reader.ReadData()

# holder = DataHolder()
# reader.TransferData(holder)

# detector = DeforestationDetector()

# def plot(image):
#     plt.imshow(image, cmap='gray')  # Use the 'gray' colormap for grayscale
#     plt.colorbar()  # Optionally add a colorbar to see the intensity scale
#     plt.axis('off')  # Turn off axis numbering and ticks
#     plt.show()

# def ConvertToDecibel(images):
#     threshold = 1e-20
#     return np.where((images > threshold), 10 * np.log10(images), 0.0)

# # Getting 
# holder.asc_mean_before, holder.asc_mean_after = detector.GetAverageBackscatter(holder.asc_images)
# holder.desc_mean_before, holder.desc_mean_after = detector.GetAverageBackscatter(holder.desc_images)

# # Calculate RCR
# holder.RCR_asc = detector.GetRadarChangeRatio(holder.asc_mean_before, holder.asc_mean_after)
# holder.RCR_desc = detector.GetRadarChangeRatio(holder.desc_mean_before, holder.desc_mean_after)

# # Detect deforestation
# holder.deforested_image_asc = detector.DetectDeforestation(holder.RCR_asc, holder.asc_mean_after)
# holder.deforested_image_desc = detector.DetectDeforestation(holder.RCR_desc, holder.desc_mean_after)

# # Deforestation regions
# holder.deforested_pixels_mask = detector.GetDeforestedPixels(holder.deforested_image_asc, holder.deforested_image_desc)
# holder.deforested_image_merged = detector.MergeDeforestedImages(holder.asc_mean_after, holder.deforested_pixels_mask)

# # Deforestation area
# holder.deforested_pixels = detector.CountDeforestedPixels(holder.deforested_image_merged)
# holder.deforested_area = detector.CalculateDeforestedArea(holder.deforested_pixels)

# print("Deforested pixels: ", holder.deforested_pixels)
# print("Deforested area: ", holder.deforested_area, "km^2")
# print(len(holder.desc_images))
#plot(holder.deforested_image_merged)
# plot(ConvertToDecibel(holder.desc_mean_after))



#### TESTING APPLICATION

main_app = DeforestationApplication()