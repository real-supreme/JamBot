import discord
import traceback
import sys
from discord import commands, cog
import asyncio


class CommandErrorHandler(cog.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        print(f"{ctx.command} raised an error: {error}")
        if hasattr(ctx.command, 'on_error'):
            return
        
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
        @cog.Cog.listener()
        async def on_error(self, event_method: str, *args, **kwargs) -> None:
            print(f"Error_Handler::: {event_method}||{args}|{kwargs}")
            task = asyncio.create_task(super().on_error(event_method, *args, **kwargs))
            try:
                if args and args[0]:
                    ctx = args[0]
                    err = args[1].original
                    await self.on_application_command_error(ctx, err)
            except (IndexError, AttributeError):
                ...
            return await task
        
        @cog.Cog.listener()
        async def on_application_command_error(self, context, exception, *args, **kwargs):
            print(f"Error_Handler::: on_application_command_error::: {context}||{exception}||{args}||{kwargs}")
            if isinstance(exception, discord.commands.errors.ApplicationCommandInvokeError):
                await self.on_application_command_error(
                    context, exception.original, *args, **kwargs
                )
                return
            try:
                task = asyncio.create_task(
                    super().on_application_command_error(context, exception)
                )
            except:
                ...
            print(f"Handler::: {context}|{exception}||{args}|{kwargs}")
            cmd = context.command.full_parent_name
            print("Command failed: ", cmd)
            ...
            #multiple checks for appropriate error handling
            ...
            return await task
            
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
    print("Events - Error Handler loaded")
    return CommandErrorHandler(bot)