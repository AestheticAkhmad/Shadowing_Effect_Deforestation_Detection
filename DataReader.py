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

    def LoadData(self, datacube, idx, lock):
        images = list()
        band = datacube[self.polarization]

        image_count = 0
        if idx == 0 or idx == 2:
            image_count = 5
            start = len(datacube['t']) - 1
            stop = -1
            step = -1
        else:
            image_count = 3
            start = 0
            stop = len(datacube['t'])
            step = 1

        for i in range(start, stop, step):
            image_np = np.array(band.isel(t=i).values)
            images.append(image_np)

            if len(images) >= image_count:
                break
        
        with lock:
            self.loaded_data[idx] = images

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

    def TransferData(self, data_holder):
        data_holder.asc_images = self.loaded_data[0] + self.loaded_data[1]
        data_holder.desc_images = self.loaded_data[2] + self.loaded_data[3]