from discord.ext import commands
import praw
import os
import json
import requests
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class ImageCog(object):
    def __init__(self, bot):
        self.credentials = load_credentials()
        self.bot = bot
        self.reddit_obj = praw.Reddit(user_agent='kestrel-discord by u/_Pseudos_ ver 0.1 see '
                                                 'https://bitbucket.org/Ragnamus/ '
                                                 'for source')
        self.reddit_obj.set_oauth_app_info(client_id=self.credentials['reddit_id'],
                                           client_secret=self.credentials['reddit_secret'],
                                           redirect_uri='http://127.0.0.1:65010/authorize_callback')
        # app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors', \
        #             'modflair modlog modothers modposts modself modwiki mysubreddits privatemessages', \
        #              'read report save submit subscribe vote wikiedit wikiread'

        # print(self.reddit_obj.get_authorize_url('state', app_scopes, True))

        # access_information = self.reddit_obj.get_access_information(self.credentials['reddit_access'])
        # print(access_information)

        self.reddit_obj.refresh_access_information(self.credentials['reddit_refresh'])
        # self.reddit_obj.set_access_credentials(**access_information)

        authenticated_user = self.reddit_obj.get_me()
        print(authenticated_user.name, authenticated_user.link_karma)


    @commands.command(hidden=True)
    async def cat(self):
        await self.bot.say(self.reddit_images('cats'))

    @commands.command(hidden=True)
    async def dog(self):
        await self.bot.say(self.reddit_images('dogpictures'))

    def reddit_images(self, subreddit):
        post = self.reddit_obj.get_random_submission(subreddit=subreddit)
        if 'https://i.reddituploads.com' in post.url:
            # this is a direct post
            return post.url
        elif 'http://imgur.com/gallery' in post.url:
            # need to extract image
            soup = BeautifulSoup(requests.get(post.url).content, 'html.parser')
            for img_link in soup.select('a.image > img'):
                if 'http://i.imgur.com' in img_link['src']:
                    return img_link['src']
        elif 'http://imgur.com' in post.url or 'https://imgur.com' in post.url:
            # this is a post to imgur, need the image link
            ext = post.url.partition('imgur.com/')[2]
            return 'http://i.imgur.com/' + ext + '.jpg'
        elif 'http://i.imgur.com' in post.url:
            # direct imgur link, post
            return post.url
        elif 'https://www.reddit.com' in post.url:
            soup = BeautifulSoup(requests.get(post.url).content, 'html.parser')
            for img_link in soup.select('a.image > img'):
                if 'https://i.redd.it' in img_link['src']:
                    return img_link['src']
            loopyloop = True
        elif 'https://i.redd.it' in post.url:
            return post.url
        else:
            pass

def load_credentials():
    with open(os.path.join(DATA_DIR, 'credentials.json')) as f:
        return json.load(f)

def setup(bot):
    bot.add_cog(ImageCog(bot))