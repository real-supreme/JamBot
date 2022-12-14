import traceback
import cv2, aiohttp
from io import BytesIO
import numpy as np
from PIL import Image, ImageEnhance
from .logger import log
from config import get_token

class BaseImgHandler:
    IMAGE_TYPES_ALLOWED = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    __slots__ = ('image', 'image_type', 'quality', 'original_image', 'stand_by')
    
    def __init__(self, image_type='.png', quality=100):
        self.image_type = image_type
        self.quality = quality
        self.image = None
        self._buffer_image = None
        
    def __repr__(self):
        return "<Image {self.image_type}:{self.quality}>"
    
    def __str__(self):
        return self.__class__.__name__
    
    def set_standby(self, image):
        self.stand_by = image
    
    async def clear_standby(self):
        await self.get_image(self.stand_by)
        del(self.stand_by)
    
    async def get_image(self, image):
        print(image)
        if isinstance(image, BytesIO):
            self.image = image.getvalue() # gives bytes
            npr = np.fromstring(self.image, np.uint8)
            self.image = cv2.imdecode(npr, cv2.IMREAD_COLOR)
        elif isinstance(image, str):
            if self.is_valid_imgURL(image):
                await self.get_image_from_url(image)
            elif self.image.startswith("file://") and self.image.endswith(self.IMAGE_TYPES_ALLOWED):
                self._buffer_image = self.image or None
                self.image = cv2.imread(image[7:]) # If None, false image
                if not self.image:
                    self.image = self._buffer_image
        elif isinstance(image, np.ndarray):
            self.image = image.copy()
        print(self.image, type(self.image), image, type(image))
        if self.image is None or image is None:
            raise TypeError("Image must be a BytesIO, str, or numpy.ndarray")
        self.original_image = self.image.copy()
        
    def is_valid_imgURL(self, url):
        return url.endswith(self.IMAGE_TYPES_ALLOWED) and url.startswith("http")
    
    def fix_url(self, url):
        try:
            url = url.split("?")[0]
        except AttributeError as e:
            print("Possible invalid URL format", e)
        return url            
        
            
    async def get_image_from_url(self, url):
        print("Getting image from url", url)
        if url.endswith("gif"):
            url = url[:-4]+".webp"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                # print(r.status, len(r.content))
                image = np.asarray(bytearray(await r.content.read()), dtype="uint8")
                print(type(image))
        if isinstance(image, np.ndarray):
            self.image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            if self.image is None:
                print("Error decoding image")
                self.image = image.copy()
        else:
            self.image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            
    async def prepare_to_send(self):
        if isinstance(self.image, bytes):
            return BytesIO(self.image)
        if self.image is not None and isinstance(self.image, np.ndarray):
            print(self.image_type)
            cv2.imwrite(f"sending.png", self.image)
            print("Sending image")
            _,iob = cv2.imencode('.png',self.image)
            buf = BytesIO(iob)
            print("iob", iob, _, type(iob), len(iob))
            return buf
    
class ImageManipulator(BaseImgHandler):
    def __init__(self, image, image_type='.png', quality=100):
        print(image)
        super().__init__(image_type, quality)
        if isinstance(image, str):
            image=self.fix_url(url=image)
            image_type = image.split(".")[-1]
            if "."+image_type not in self.IMAGE_TYPES_ALLOWED:
                raise TypeError("Image type must be one of: {}".format(self.IMAGE_TYPES_ALLOWED))
            self.image_type = "."+image_type
            if self.image_type == ".gif":
                self.image_type = ".webp"
        super().set_standby(image)
        
    def __filter_value(self, value):
        if value <-255:
            value = -255
        elif value > 255:
            value = 255
        return value
    
    def __percent_factor_value(self, value):
        HB= 255
        value += 255
        return value/HB
        
    
    async def brightness(self, value):
        value = self.__filter_value(value)
        try:
            sheet = np.ones(self.image.shape, dtype=self.image.dtype or "uint8")*value
            self._buffer_image = self.image
            self.image = cv2.add(self.image, sheet)
        except cv2.error:
            value = self.__percent_factor_value(value)
            pil_image = Image.fromarray(self.image)
            buf = BytesIO()
            ImageEnhance.Brightness(pil_image).enhance(value).save(buf, format="PNG", quality=self.quality)
            self._buffer_image = self.image
            self.image = buf.getvalue()
        except Exception as e:
            print("Error in brightness", e)
            traceback.print_exc()
        
    async def contrast(self, value):
        value = self.__filter_value(value)
        value = self.__percent_factor_value(value)
        print(f"Contrasting image with value {value}")
        pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        buf = BytesIO()
        ImageEnhance.Contrast(pil_image).enhance(value).save(buf, format="PNG", quality=self.quality)
        self._buffer_image = self.image
        self.image = buf.getvalue()
        
    async def sharpness(self, value):
        value = self.__filter_value(value)
        value = self.__percent_factor_value(value)
        pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        buf = BytesIO()
        ImageEnhance.Sharpness(pil_image).enhance(value).save(buf, format="PNG", quality=self.quality)
        self._buffer_image = self.image
        self.image = buf.getvalue()
        
    async def saturation(self, value):
        value = self.__filter_value(value)
        value = self.__percent_factor_value(value)
        pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        buf = BytesIO()
        ImageEnhance.Color(pil_image).enhance(value).save(buf, format="PNG", quality=self.quality)
        self._buffer_image = self.image
        self.image = buf.getvalue()
    
    async def smoothen(self, value):
        value = self.__filter_value(value)
        self._buffer_image = self.image
        self.image = cv2.medianBlur(self.image, int(value))
    
    async def kill(self, image=None):
        if image:
            if self.image:
                self._buffer_image = self.image
            self.image = image
        try:
            image = cv2.line(self.image, (0,0), (self.image.shape[1], self.image.shape[0]), (0,0,255), 5)
            image = cv2.line(image, (0,self.image.shape[0]), (self.image.shape[1], 0), (0,0,255), 5)
        except Exception as e:
            log.execption(e)
            
    async def sketchify(self):
        self._buffer_image = self.image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (25, 25), 0)
        self.image = cv2.divide(gray, gray_blur, scale=250.0)
                
    async def cartoonify(self):
        self._buffer_image = self.image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 3) 
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9) 
        color = cv2.detailEnhance(self.image, sigma_s=5, sigma_r=0.5)
        self.image = cv2.bitwise_and(color, color, mask=edges) 
        
    async def rotate(self, angle=90):
        self._buffer_image = self.image
        print(f"Rotating image by {angle}\n{type(self.image)}")
        if angle == 90:
            angle = cv2.ROTATE_90_CLOCKWISE
        elif angle == 180:
            angle = cv2.ROTATE_180
        elif angle == 270:
            angle = cv2.ROTATE_90_COUNTERCLOCKWISE
        self.image = cv2.rotate(self.image, angle)
        
    async def resize(self, width=None, height=None):
        if width and height:
            self.image = cv2.resize(self.image, (width, height))
    
    async def flip(self, direction="horizontal"):
        if direction == "horizontal":
            self.image = cv2.flip(self.image, 0)
        elif direction == "vertical":
            self.image = cv2.flip(self.image, 1)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
            
    async def invert(self):
        self.image = cv2.bitwise_not(self.image)
            
if __name__ == '__main__':
    ...