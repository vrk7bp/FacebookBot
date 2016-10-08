# Facebook Bot

Bots seem to have hit the main stream since the public release of the Amazon Echo in late 2014. Although bots have been around since long before then, this
seems to have been the catalyst for a much larger increaes in potential users of bots. Since Echo came out, we've seen bot and bot platforms released by
a wider range of companies including Microsoft and Facebook. Although it hasn't reached the level of influence that the mobile phone has, bots have the
potential to combine with "smart home" devices, cars, and other electronics to become the next revolution in computing

As Facebook's Messenger platform is trending towards almost a billion users, it is likely the bot platform with the greatest user footprint. With that in
mind, I decided to make my first bot using Facebook. The company has pretty awesome documentation on making your first bot, just written in Node.JS. For
someone like me who prefers Python, the interpretation from Node.JS to Flask (my preferred Web Framework) took a bit of time. With that in mind, I decided
to make this GitHub Repo, which would be an almost exact mimic of the Facebook example explained in the 'Get Started' tutorial (https://developers.facebook.com/docs/messenger-platform/quickstart), but with Flask instead of Node.JS

The Flask backend provided in this repo isn't tied to any cloud provider in particular, which means some tweaks may have to be made based on how you're
provider prefers things. There is also a 'requirements.txt' file provided for building the proper Python virtual environment. Its pretty massive, I think because
it lists out the dependencies that are needed for the 'requests' library that I use to send messages back to the user.

A couple notes about the structure of things:

   #constants.py - This is the file that holds any constants that you want to define. Your verification and page-token should be put here, and you can feel free to define more if you want
   #views.py - This is the "proxy" for the bot web server. So this is where requests initially come in, and are then redirected to the necessary methods/files
   #messageHandler.py - This holds all the relevant methods for dealing with when messages are received.

Note: This repo is still a work in progress. As I dive deeper into the different interactions possible between users and bots, I will likely add
more handlers and files to deal with the idiosyncrisies of those handlers. So its possible that things might change up over time. 

Also, credit to Hartley Brody for giving me a foundation for my flask template. His original GitHub repo can be found here: https://github.com/hartleybrody/fb-messenger-bot
