import discord
from discord.ext import commands
import os
import sys
import urllib.request
import cv2
from matplotlib.pylab import array, uint8

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, 'cogs/images')


class EditCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 1
        self.phi = 1
        self.theta = 1
        self.maxIntensity = 255.0

    def hyperize(self, urlstr):
        name = os.path.join(IMAGE_DIR, str(self.counter) + ".jpg")
        print(name)
        urllib.request.urlretrieve(urlstr, name)
        self.counter += 1

        # Read image
        img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)

        imgnew = (self.maxIntensity/self.phi) * (
                  img / (self.maxIntensity / self.theta)) ** 1.5
        imgnew = array(imgnew, dtype=uint8)

        # Applying hyper
        im_color = cv2.applyColorMap(imgnew, cv2.COLORMAP_AUTUMN)

        im_blur = cv2.blur(im_color, (30, 10))

        # Saving filtered image to new file
        cv2.imwrite(os.path.join(IMAGE_DIR, 'test.jpg'), im_blur)

    @commands.command(pass_context=True)
    async def hyper(self, ctx, urlstr: str):
        self.hyperize(urlstr)
        chid = ctx.message.channel
        print(ctx.message.channel.id)
        path = os.path.join(IMAGE_DIR, 'test.jpg')
        print(path)
        with open(path, 'rb') as f:
            await self.bot.send_file(chid, f)


def setup(bot):
    bot.add_cog(EditCog(bot))


if __name__ == '__main__':
    imc = EditCog("rq")
    imc.hyperize("http://i.imgur.com/NYwSoYp.jpg")
