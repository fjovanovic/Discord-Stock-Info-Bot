import datetime as dt

from discord import (
    ButtonStyle, 
    Interaction, 
    Embed, 
    Colour, 
    SelectOption
)
from discord.ui import View, Button
from discord.ui import button

from constants import YAHOO_FINANCE_URL
from .my_modal_institutional_holders import MyModalInstitutionalHolders
from .my_select_institutional_holders import MySelectInstitutionalHolders


class MyViewShowInstitutionalHolders(View):
    def __init__(self, ticker: str, data: dict, page: int, size: int) -> None:
        super().__init__()
        self.ticker = ticker
        self.data = data
        self.page = page
        self.size = size
    
    
    @button(label='🢘 Previous', style=ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: Interaction, button: Button) -> None:
        self.page -= 1
        if self.page == 0:
            self.children[0].disabled = True
        
        if self.page < self.size:
            self.children[1].disabled = False
        
        if self.page == 0:
            my_embed = Embed(
                title='More info',
                url=f'{YAHOO_FINANCE_URL}{self.ticker}',
                colour=Colour.blue(),
                timestamp=dt.datetime.now()
            )

            my_embed.set_author(name=f'{self.ticker}', icon_url=interaction.user.avatar.url)
            for (key, holder) in self.data['Holder'].items():
                my_embed.add_field(
                    name=f'Institutional holder #{int(key) + 1}',
                    value=f'`{holder} ({self.data["Value"][str(key)]:,} $)`',
                    inline=False
                )

            await interaction.response.edit_message(embed=my_embed, view=self)
            return
        
        my_select = MySelectInstitutionalHolders(self.data)
        for i in range(1, self.size + 1):
            my_select.add_option(
                label=f'{self.data["Holder"][str(i-1)]}',
                value=f'{i-1}',
                description=f'{self.data["Value"][str(i-1)]:,} $'
            )
        for child in self.children:
            if isinstance(child, (MySelectInstitutionalHolders, SelectOption)):
                self.remove_item(child)
        self.add_item(my_select)

        my_embed = Embed(
            color=Colour.green(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'Page {self.page} / {self.size}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(
            name='Holder', 
            value=f'`{self.data["Holder"][str(self.page - 1)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Shares', 
            value=f'`{self.data["Shares"][str(self.page - 1)]:,}`', 
            inline=False
        )
        my_embed.add_field(
            name='Date Reported', 
            value=f'`{dt.datetime.fromtimestamp(self.data["Date Reported"][str(self.page - 1)] / 1000)}`', 
            inline=False
        )
        my_embed.add_field(
            name='% Out', 
            value=f'`{self.data["% Out"][str(self.page - 1)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Value', 
            value=f'`{self.data["Value"][str(self.page - 1)]:,} $`', 
            inline=False
        )

        await interaction.response.edit_message(embed=my_embed, view=self)
    

    @button(label='Next 🢚', style=ButtonStyle.primary)
    async def next_button(self, interaction: Interaction, button: Button) -> None:
        self.page += 1
        if self.page == 1:
            self.children[0].disabled = False
        
        if self.page >= self.size:
            self.children[1].disabled = True
        
        my_select = MySelectInstitutionalHolders(self.data)
        for i in range(1, self.size + 1):
            my_select.add_option(
                label=f'{self.data["Holder"][str(i-1)]}',
                value=f'{i-1}',
                description=f'{self.data["Value"][str(i-1)]:,} $'
            )
        for child in self.children:
            if isinstance(child, (MySelectInstitutionalHolders, SelectOption)):
                self.remove_item(child)
        self.add_item(my_select)

        my_embed = Embed(
            color=Colour.green(),
            timestamp=dt.datetime.now()
        )

        my_embed.set_author(name=f'Page {self.page} / {self.size}', icon_url=interaction.user.avatar.url)
        my_embed.add_field(
            name='Holder', 
            value=f'`{self.data["Holder"][str(self.page - 1)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Shares', 
            value=f'`{self.data["Shares"][str(self.page - 1)]:,}`', 
            inline=False
        )
        my_embed.add_field(
            name='Date Reported', 
            value=f'`{dt.datetime.fromtimestamp(self.data["Date Reported"][str(self.page - 1)] / 1000)}`', 
            inline=False
        )
        my_embed.add_field(
            name='% Out', 
            value=f'`{self.data["% Out"][str(self.page - 1)]}`', 
            inline=False
        )
        my_embed.add_field(
            name='Value', 
            value=f'`{self.data["Value"][str(self.page - 1)]:,} $`', 
            inline=False
        )

        await interaction.response.edit_message(embed=my_embed, view=self)
    

    @button(label='Go to page', style=ButtonStyle.success)
    async def go_to_page_button(self, interaction: Interaction, button: Button) -> None:
        my_modal = MyModalInstitutionalHolders(view=self)

        await interaction.response.send_modal(my_modal)