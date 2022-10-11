import discord
import traceback
import sys
import aiohttp
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(context.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = context.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        await context.send(error)
        if isinstance(error,commands.CommandNotFound):
            await context.reply("Unknown command")
        if isinstance(error,commands.MissingPermissions):
            await context.reply("You do not have the correct permissions for this command.")
        if isinstance(error,commands.CommandOnCooldown):
            num = error.retry_after
            if num>60:
                msg = num/60
                if msg>90:
                    hour = msg/60
                    await context.reply(f"You are on cooldown for this command for **{round(hour)} hours**")
                if msg<90:
                    await context.reply(f"You are on cooldown for this command for **{round(msg)} minutes**")
            if num<60:
                await context.send(f"You are on cooldown for this command for **{round(num)} seconds**")
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return
        if isinstance(error,commands.errors.BotMissingPermissions):
            await context.send("I do not have the correct permissions for this command.")
        if isinstance(error, commands.DisabledCommand):
            await context.reply(f'{context.command} has been disabled.')
        if isinstance(error, commands.MissingRequiredArgument):
            await context.reply("You forgot to give input!")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await context.author.reply(f'{context.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if context.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await context.reply('I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(context.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    """Below is an example of a Local Error Handler for our command do_repeat"""


def setup(client):
    client.add_cog(CommandErrorHandler(client))