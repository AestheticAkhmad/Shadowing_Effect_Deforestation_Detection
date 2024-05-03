
class DataHolder:
    def __init__(self) -> None:
        # Ascending
        self.asc_images = list()
        self.asc_mean_before = None
        self.asc_mean_after = None
        self.RCR_asc = None

        # Descending
        self.desc_images = list()
        self.desc_mean_before = None
        self.desc_mean_after = None
        self.RCR_desc = None

        # Deforestation
        self.deforested_pixels = 0
        self.deforested_area = 0.0
        self.deforested_image_asc = None
        self.deforested_image_desc = None
        self.deforested_pixels_mask = None
        self.deforested_image_merged = None
