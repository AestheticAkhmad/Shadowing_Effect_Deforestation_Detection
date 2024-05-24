import numpy as np
from collections import deque
from skimage import restoration

class DeforestationDetector:
    def __init__(self) -> None:
        self.xb = 5
        self.xa = 3

    def ApplyDenoise(self, images):
        return restoration.denoise_tv_chambolle(images, weight=0.02)
    
    def NormalizeImage(self, image):
        #image = np.where(image >= 1.0, 0.9999, image)
        return image

    def GetAverageBackscatter(self, images):
        mb = np.mean(np.stack(images[:self.xb]), axis=0)
        ma = np.mean(np.stack(images[self.xb:]), axis=0)

        return mb, ma
    
    def ConvertToDecibel(self, image):
        threshold = 1e-15
        return np.where((image > threshold), 10 * np.log10(image), 0.0)

    def GetRadarChangeRatio(self, mb, ma):
        threshold = 1e-15
        RCR = np.where(mb > threshold, ma / mb, 0.0)
        RCR_no_nan_inf = np.nan_to_num(RCR, nan=0.0, posinf=0.0, neginf=0.0)
        return self.ConvertToDecibel(RCR_no_nan_inf)
    
    def is_valid(self, x, y, rcr):
        if x < 0 or x >= len(rcr):
            return False
        if y < 0 or y >= len(rcr[0]):
            return False
        return True
    
    def DoubleBounceBFS(self, x, y, visited, rcr, image):
        q = deque()
        q.append([x, y])
        t = 3.5
        area = 0
        to_color = list()
        
        while len(q) > 0:
            curr = q.popleft()

            if self.is_valid(curr[0], curr[1], rcr) == False:
                continue
            if visited[curr[0], curr[1]]:
                continue
            if rcr[curr[0], curr[1]] < t:
                continue
            

            to_color.append([curr[0], curr[1]])
            area += 1

            visited[curr[0], curr[1]] = True
            q.append([curr[0] - 1, curr[1]])
            q.append([curr[0], curr[1] - 1])
            q.append([curr[0] + 1, curr[1]])
            q.append([curr[0], curr[1] + 1])
        
        if area <= 10:
            return 0
        
        for idx in to_color:
            image[idx[0], idx[1], 0] = 255
            image[idx[0], idx[1], 1] = 0
            image[idx[0], idx[1], 2] = 0

    def ShadowBFS(self, x, y, visited, rcr, image):
        q = deque()
        q.append([x, y])
        t = -3.07
        area = 0
        to_color = list()
        
        while len(q) > 0:
            curr = q.popleft()

            if self.is_valid(curr[0], curr[1], rcr) == False:
                continue
            if visited[curr[0], curr[1]]:
                continue
            if rcr[curr[0], curr[1]] > t:
                continue

            to_color.append([curr[0], curr[1]])
            area += 1

            visited[curr[0], curr[1]] = True
            q.append([curr[0] - 1, curr[1]])
            q.append([curr[0], curr[1] - 1])
            q.append([curr[0] + 1, curr[1]])
            q.append([curr[0], curr[1] + 1])
        
        if area <= 10:
            return 0

        for idx in to_color:
            image[idx[0], idx[1], 0] = 255
            image[idx[0], idx[1], 1] = 0
            image[idx[0], idx[1], 2] = 0

    def DetectDeforestation(self, RCR, mean_after_image):
        visited = np.zeros(RCR.shape, dtype=bool)

        deforestation_image = np.stack([mean_after_image]*3, axis=-1)

        for x in range(RCR.shape[0]):
            for y in range(RCR.shape[1]):
                if visited[x, y] == False and RCR[x, y] < -4.5:
                    self.ShadowBFS(x, y, visited, RCR, deforestation_image)

        visited = np.zeros(RCR.shape, dtype=bool)

        for x in range(RCR.shape[0]):
            for y in range(RCR.shape[1]):
                if visited[x, y] == False and RCR[x, y] > 4.5:
                   self.DoubleBounceBFS(x, y, visited, RCR, deforestation_image)

        return deforestation_image
    
    def GetDeforestedPixels(self, deforested_image_asc, deforested_image_desc):
        return (deforested_image_asc[:, :, 0] == 255) | (deforested_image_desc[:, :, 0] == 255)

    def MergeDeforestedImages(self, image, deforested_pixels):
        merged_image = np.stack([image]*3, axis=-1)
        merged_image[deforested_pixels] = [255, 0, 0]
        return merged_image

    def CountDeforestedPixels(self, deforested_image):
        deforested_pixels_mask = (deforested_image[:, :, 0] == 255)
        return np.sum(deforested_pixels_mask)
    
    def CalculateDeforestedArea(self, deforested_pixels):
        return (deforested_pixels * 100) / 1000000
    
    def CalculateMean(self, img1, img2):
        return (img1 + img2) / 2.0