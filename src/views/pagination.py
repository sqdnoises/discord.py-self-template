"""
Class that contains custom pagination views.
"""

from typing import Any, Literal, Union, Callable, NoReturn

from classes import Bot, Context
from customtypes import MISSING

import discord

__all__ = (
    "PaginationView",
    "SlashPaginationView"
)

async def missing(text: str | None = None) -> Callable:
    def func(*args, **kwargs) -> NoReturn:
        raise NotImplementedError(text)
    return func

class PaginationView(discord.ui.View):
    """View for managing command paginations"""
    
    def __init__(
        self,
        bot: Bot,
        ctx: Context = None,
        paginated_things: list | tuple[
            dict[
                Union[
                    Literal["args"],
                    Literal["kwargs"]
                ],
                Union[
                    tuple[Any, ...],
                    dict[str, Any]
                ]
            ]
        ] = MISSING,
        *,
        user: discord.User | discord.Member | None = None,
        reply: bool = False,
        items: int = 5,
        timeout: float | None = None
    ) -> None:
        super().__init__(timeout=timeout)
        
        if ctx:
            self.ctx = ctx
            self.user = ctx.author
            self.send = ctx.send
            if reply:
                self.send = ctx.reply
        else:
            self.send = missing("PaginationView.send() was not implemented!")
            self.user = user
        
        self.bot = bot
        
        self.page = 1
        self.pages = paginated_things
        self.items = items
    
    async def start(self):
        await self.update_pages()
        await self.update_buttons()
        page = self.pages[self.page]
        args = page.get("args", ())
        kwargs = page.get("kwargs", {})
        await self.send(*args, **kwargs, view=self)
    
    async def update_pages(
        self,
        *,
        first: bool = False,
        previous: bool = False,
        next: bool = False,
        last: bool = True
    ) -> None:
        if first:
            self.page = 1
        elif previous:
            self.page -= 1
        elif next:
            self.page += 1
        elif last:
            self.page = len(self.pages)
        
        self.page = 1
    
    async def update_buttons(self) -> None:
        buttons: list[discord.ui.Button] = [
            child for child in self.children
            if child.type == discord.ComponentType.button
            and (
                button.custom_id == "first" or
                button.custom_id == "previous" or
                button.custom_id == "next" or
                button.custom_id == "last"
            )
        ]
        
        if len(buttons) == 0:
            first = discord.ui.Button(emoji="⏪", style=discord.ButtonStyle.grey, custom_id="first")
            first.callback = self.first_page
            self.add_item(first)
            
            prev = discord.ui.Button(emoji="⬅️", style=discord.ButtonStyle.grey, custom_id="previous")
            prev.callback = self.previous_page
            self.add_item(prev)
            
            next = discord.ui.Button(emoji="➡️", style=discord.ButtonStyle.grey, custom_id="next")
            next.callback = self.next_page
            self.add_item(next)
            
            last = discord.ui.Button(emoji="⏩", style=discord.ButtonStyle.grey, custom_id="last")
            last.callback = self.last_page
            self.add_item(last)
            
            buttons: list[discord.ui.Button] = [
                child for child in self.children
                if child.type == discord.ComponentType.button
                and (
                    button.custom_id == "first" or
                    button.custom_id == "previous" or
                    button.custom_id == "next" or
                    button.custom_id == "last"
                )
            ]
        
        buttons[0].disabled = self.page == 1
        buttons[1].disabled = self.page == 1
        buttons[2].disabled = self.page == len(self.pages)
        buttons[3].disabled = self.page == len(self.pages)
        
        if all([button.disabled for button in buttons]):
            while len(buttons) > 0:
                button = buttons[0]
                self.remove_item(button)
                buttons.pop(0)
        
        for button in buttons:
            if button.disabled:
                button.style = discord.ButtonStyle.red
            else:
                button.style = discord.ButtonStyle.green
    
    async def _interaction_check(self, interaction: discord.Interaction, content: str = "This is not your menu.") -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                content = content,
                ephemeral = True
            )
            return False
        return True
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        await self._interaction_check(interaction)
    
    async def first_page(self, interaction: discord.Interaction) -> None:
        self.update_pages(first=True)
        await self.update_buttons()
        page = self.pages[self.page]
        args = page.get("args", ())
        kwargs = page.get("kwargs", {})
        await interaction.response.edit_message(*args, **kwargs, view=self)
    
    async def previous_page(self, interaction: discord.Interaction) -> None:
        self.update_pages(previous=True)
        await self.update_buttons()
        page = self.pages[self.page]
        args = page.get("args", ())
        kwargs = page.get("kwargs", {})
        await interaction.response.edit_message(*args, **kwargs, view=self)
    
    async def next_page(self, interaction: discord.Interaction) -> None:
        self.update_pages(next=True)
        await self.update_buttons()
        page = self.pages[self.page]
        args = page.get("args", ())
        kwargs = page.get("kwargs", {})
        await interaction.response.edit_message(*args, **kwargs, view=self)
    
    async def last_page(self, interaction: discord.Interaction) -> None:
        self.update_pages(last=True)
        await self.update_buttons()
        page = self.pages[self.page]
        args = page.get("args", ())
        kwargs = page.get("kwargs", {})
        await interaction.response.edit_message(*args, **kwargs, view=self)

class SlashPaginationView(PaginationView):
    """View for managing slash command paginations"""
    
    def __init__(
        self,
        bot: Bot,
        interaction: discord.Interaction = None,
        paginated_things: list | tuple[
            dict[
                Union[
                    Literal["args"],
                    Literal["kwargs"]
                ],
                Union[
                    tuple[Any, ...],
                    dict[str, Any]
                ]
            ]
        ] = MISSING,
        *,
        user: discord.User | discord.Member | None = None,
        items: int = 5,
        timeout: float | None = None
    ) -> None:
        if interaction:
            user = interaction.user
        super().__init__(bot=bot, paginated_things=paginated_things, user=user, items=items, timeout=timeout)
        self.interaction = interaction
        self.send = interaction.response.send_message