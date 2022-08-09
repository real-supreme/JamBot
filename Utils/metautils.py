import io
from discord import File
from .ImageHandler import BaseImgHandler as handler
class DImageFile(File):
    def __init__(self, fp, **kwargs):
        if isinstance(fp, str):
            if not fp.endswith(handler.IMAGE_TYPES_ALLOWED):
                raise TypeError("Unsupported image type")
            fp = open(fp, "rb")
        elif isinstance(fp, bytes):
            fp = io.BytesIO(fp)
        
        super().__init__(fp, filename=kwargs.get('filename', None), description=kwargs.get('description', None), spoiler=kwargs.get('spoiler', False))
        
    def __str__(self):
        return self.filename or str(self.fp)
    
async def send(ctx, *args, **kwargs):
    ephemeral = kwargs.pop('ephemeral', False)
    # try:
    #     if kwargs.get('file', None):
    #         if len(kwargs['file'].fp.read())>=8*1024*1024:
    #             await ctx.send("Image is too large to send")
    #             return
    # except (TypeError,AttributeError):
    #     ...
    print("Sending...", ctx, args, kwargs)
    try:
        return await ctx.respond(*args, **kwargs, ephemeral=ephemeral)
    except:
        return await ctx.send(*args, **kwargs)