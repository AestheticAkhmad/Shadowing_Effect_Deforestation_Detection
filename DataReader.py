import xarray as xr
import threading
import numpy as np
from DataHolder import DataHolder

class DataReader:
    def __init__(self, file_paths = list()) -> None:
        # Files to read the images from
        self.file_paths = file_paths

        # Threads to read images concurrently
        self.lock = threading.Lock()
        self.threads = list()

        # Storage for loaded data
        self.loaded_data = [None] * len(file_paths)
        self.polarization = "VV"

        # Available orbits
        self.orbits = [True, True, True, True]

    def LoadData(self, datacube, idx, lock):
        images = list()
        band = datacube[self.polarization]
        full_count = False

        image_count = 0
        if idx == 0 or idx == 2:
            image_count = 5
            start = len(datacube['t']) - 1
            print("Datacube length: ", len(datacube['t']))
            stop = -1
            step = -1
        else:
            image_count = 3
            start = 0
            stop = len(datacube['t'])
            print("Datacube length: ", len(datacube['t']))
            step = 1

        for i in range(start, stop, step):
            image_np = np.array(band.isel(t=i).values)

            if self.IsImageEmpty(image_np):
                continue

            images.append(image_np)

            if len(images) >= image_count:
                full_count = True
                break
        
        with lock:
            self.loaded_data[idx] = images

            if not full_count:
                self.orbits[idx] = False

    def ReadData(self):
        if len(self.file_paths) < 4:
            return

        for idx, file_path in enumerate(self.file_paths):
            datacube = xr.open_dataset(file_path)
            thread = threading.Thread(target=self.LoadData, args=(datacube, idx, self.lock))
            thread.start()
            self.threads.append(thread)
        
        for thread in self.threads:
            thread.join()

    def IsImageEmpty(self, img, epsilon=1e-5):
        img_without_nan = np.nan_to_num(img)
        num_close_to_zero = np.sum(np.abs(img_without_nan) < epsilon)
        ratio = num_close_to_zero / img.size

        if num_close_to_zero / img.size > 0.3:
            return True
        else:
            return False

    def TransferData(self, data_holder):
        if not self.orbits[0] and not self.oribts[1]:
            data_holder.desc_images = self.loaded_data[2] + self.loaded_data[3]
            return "desc"
        
        elif not self.orbits[2] and not self.oribts[3]:
            data_holder.asc_images = self.loaded_data[0] + self.loaded_data[1]
            return "asc"

        else:
            data_holder.asc_images = self.loaded_data[0] + self.loaded_data[1]
            data_holder.desc_images = self.loaded_data[2] + self.loaded_data[3]
            return "both"
        