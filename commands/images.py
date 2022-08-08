from random import choice
from Utils.ImageHandler import ImageManipulator
from discord.cog import Cog
from discord import commands, Option, Attachment, File, Member
from cog_logger import log
from Utils.metautils import send

class Images(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def filtered_imager(self, ctx, image_file, image_url):
        log.info(f"CMD: brightness\n||{image_file}||{image_url}")
        try:
            if image_file:
                file = await image_file.to_file()
                imager = ImageManipulator(file.fp)
            elif image_url:
                imager = ImageManipulator(image_url)
            elif hasattr(ctx.message,'attachments') and len(ctx.message.attachments) > 0:
                imager = ImageManipulator(ctx.message.attachments[0].url)
            else:
                imager = ImageManipulator(image=ctx.author.display_avatar.url)
        except TypeError:
            await send(ctx, "Valid Image was not found.")
            return
        except Exception as e:
            print("Error occured in filtered_imager")
            log.exception(e)
            return
        return imager
        
        
    @commands.slash_command(name='brightness')
    async def brightness(self, ctx, value: Option(int, "How bright do you want it? (-255 to 255)",min_value=-255,max_value=255)=25, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Increase or decrease the brightness of an image. Your pfp will be used by default.
        """
        
        if value not in range(-255,256):
            await send(ctx, "Value must be between -255 and 255.")
            return
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.brightness(value)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Brightness changed by {value}*")
        
    @commands.slash_command(name='contrast')
    async def contrast(self, ctx, value: Option(int, "How bright do you want it? (0-255)",min=-255, max=255)=25, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Increase or decrease the contrast of an image. Your pfp will be used by default.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.contrast(value)
        buffered = await imager.prepare_to_send()
        img_type = imager.image_type if imager.image_type!=".gif" else ".jpg"
        fname = f"{ctx.author.display_name}_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Contrast changed by {value}*")
        
    @commands.slash_command(name='invert')
    async def invert(self, ctx, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Invert the colours of your image. Your pfp will be defaultly inverted.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.invert()
        buffered = await imager.prepare_to_send()
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_inverted"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"))
        
    @commands.slash_command(name='sharpness')
    async def sharpness(self, ctx, value: Option(int, "How Sharp do you want it? (-255 to 255)",min_value=-255,max_value=255)=25, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Increase or decrease the sharpness of an image. Your pfp will be used by default.
        """
        
        if value not in range(-255,256): #just in case
            await send(ctx, "Value must be between -255 and 255.")
            return
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.sharpness(value)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Sharpness changed by {value}*")
        
    @commands.slash_command(name='smoothen')
    async def smoothen(self, ctx, value: Option(int, "How smooth do you want it? (-255 to 255)",min_value=-255,max_value=255)=25, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Increase or decrease the smoothness of an image. Your pfp will be used by default.
        """
        
        if value not in range(-255,256):
            await send(ctx, "Value must be between -255 and 255.")
            return
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.smoothen(value)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image changed by {value}*")
    
    @commands.slash_command(name='saturation')
    async def saturation(self, ctx, value: Option(int, "How saturated do you want it? (-255 to 255)",min_value=-255,max_value=255)=25, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Increase or decrease the saturation of an image. Your pfp will be used by default.
        """
        
        if value not in range(-255,256):
            await send(ctx, "Value must be between -255 and 255.")
            return
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.saturation(value)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image changed by {value}*")
    
    @commands.slash_command(name='kill')
    async def kill_user(self, ctx, user: Option(Member, "Who do you want to kill?")=None):
        """
        Kills a user.
        """
        try:
            await ctx.defer()
        except:
            ...
        if user is None:
            user = ctx.author
        if user.id == self.bot.user.id:
            await send(ctx, content="I can't kill myself.",ephemeral=True)
            return
        imager = ImageManipulator(image=user.display_avatar.url)
        await imager.clear_standby()
        await imager.kill()
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        file = File(buffered, filename=f"{user.display_name}_killed{img_type}")
        if user.id != ctx.author.id:
            await send(ctx, content=f"*{user.display_name} has been killed*", file=file)
        else:
            await send(ctx, content="*You have been killed*", file=file)
            
    @commands.slash_command(name='sketchify')
    async def sketchify(self, ctx, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Sketchify an image. Your pfp will be used by default.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.sketchify()
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_sketchified"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image Sketchified*")
        
    @commands.slash_command(name='rotate')
    async def rotate(self, ctx, value: Option(int, "How many degrees do you want to rotate? (0 to 360)",choices=[0,90,180,270,360])=90, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Rotate an image. Your pfp will be used by default.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        if value != 0 and value != 360:
            await imager.rotate(value)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_rotated_{value}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image rotated by {value}*")
        
    @commands.slash_command(name='flip')
    async def flip(self, ctx, direction: Option(str, "What direction do you want to flip? (horizontal or vertical)",choices=["horizontal","vertical"])="horizontal", image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Flip an image. Your pfp will be used by default.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.flip(direction)
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_flipped_{direction}"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image flipped by {direction}*")
        
    @commands.slash_command(name='cartoonify')
    async def cartoonify(self, ctx, image_file: Option(Attachment, "What image do you want to change?")=None, image_url:Option(str, "URL of the image to edit")=None):
        """
        Cartoonify an image. Your pfp will be used by default.
        """
        try:
            await ctx.defer()
        except:
            ...
        imager = await self.filtered_imager(ctx, image_file, image_url)
        await imager.clear_standby()
        await imager.cartoonify()
        buffered = await imager.prepare_to_send()
        print(buffered, type(buffered))
        img_type = imager.image_type if imager.image_type!=".gif" else ".webp"
        fname = f"{ctx.author.display_name}_cartoonified"
        await send(ctx, file=File(buffered, filename=f"{fname}{img_type}"), content=f"*Image cartoonified*")
    
def setup(bot):
    bot.add_cog(Images(bot))
    log.debug('Images is loaded')
    print('Images is loaded')
    return Images(bot)