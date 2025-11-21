# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
import asyncio
import json
from pathlib import Path
import httpx
from functools import partial
from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()

        # Search history
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()

        # Temperature unit
        self.current_unit = "metric"
        self.current_temp = 0

        # Setup page & UI
        self.setup_page()
        self.build_ui()

    # ------------------ History Methods ------------------
    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.search_history, f)

    def add_to_history(self, city: str):
        if city and city not in self.search_history:
            self.search_history.insert(0, city)
            self.search_history = self.search_history[:10]  # last 10
            self.save_history()
            self.history_dropdown.options = [ft.dropdown.Option(c) for c in self.search_history]
            self.page.update()

    async def get_weather_from_history(self, city: str):
        if not city:
            return
        self.city_input.value = city
        self.page.update()
        await self.get_weather()

    # ------------------ Current Location ------------------
    async def get_location_weather(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                city = data.get("city")
                if city:
                    self.city_input.value = city
                    self.page.update()
                    await self.get_weather()
        except Exception:
            self.show_error("Could not get your location")

    # ------------------ Page Setup ------------------
    def setup_page(self):
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.window.center()

    # ------------------ UI ------------------
    def build_ui(self):
        # Title
        self.title = ft.Text("Weather App", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)

        # Theme toggle
        self.theme_button = ft.IconButton(
            icon=ft.Icons.DARK_MODE, tooltip="Toggle theme", on_click=self.toggle_theme
        )
        title_row = ft.Row([self.title, self.theme_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # City input
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=lambda e: self.page.run_task(self.get_weather)
        )

        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=lambda e: self.page.run_task(self.get_weather),
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700)
        )

        # My Location button
        self.location_button = ft.ElevatedButton(
            "My Location",
            icon=ft.Icons.MY_LOCATION,
            on_click=lambda e: self.page.run_task(self.get_location_weather),
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700)
        )

        # History dropdown
        self.history_dropdown = ft.Dropdown(
            label="Recent Searches",
            width=250,
            options=[ft.dropdown.Option(city) for city in self.search_history],
            on_change=lambda e: self.page.run_task(partial(self.get_weather_from_history, e.control.value))
        )

        # Weather container
        self.weather_container = ft.Container(visible=False, bgcolor=ft.Colors.BLUE_50, border_radius=10, padding=20)

        # Error message
        self.error_message = ft.Text("", color=ft.Colors.RED_700, visible=False)

        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)

        # Add to page
        self.page.add(
            ft.Column(
                [
                    title_row,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.city_input,
                    ft.Row([self.search_button, self.location_button, self.history_dropdown], spacing=10),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    # ------------------ Theme ------------------
    def toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_button.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_button.icon = ft.Icons.DARK_MODE
        self.page.update()

    # ------------------ Weather ------------------
    async def get_weather(self):
        city = self.city_input.value.strip()
        if not city:
            self.show_error("Please enter a city name")
            return

        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()

        try:
            weather_data = await self.weather_service.get_weather(city)
            await self.display_weather(weather_data)
            self.add_to_history(city)
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.loading.visible = False
            self.page.update()

    async def display_weather(self, data: dict):
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)
        pressure = data.get("main", {}).get("pressure", 0)
        clouds = data.get("clouds", {}).get("all", 0)

        self.weather_container.content = ft.Column(
            [
                ft.Text(f"{city_name}, {country}", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Image(src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png", width=100, height=100),
                        ft.Text(description, size=20, italic=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(f"{temp:.1f}°C", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.Text(f"Feels like {feels_like:.1f}°C", size=16, color=ft.Colors.GREY_700),
                ft.Divider(),
                ft.Row(
                    [
                        self.create_info_card(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%"),
                        self.create_info_card(ft.Icons.AIR, "Wind Speed", f"{wind_speed} m/s"),
                        self.create_info_card(ft.Icons.SPEED, "Pressure", f"{pressure} hPa"),
                        self.create_info_card(ft.Icons.CLOUD, "Cloudiness", f"{clouds}%"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        if temp > 35:
            alert = ft.Banner(
                bgcolor=ft.Colors.AMBER_100,
                leading=ft.Icon(ft.Icons.WARNING, color=ft.Colors.AMBER, size=40),
                content=ft.Text("⚠️ High temperature alert!"),
            )
            self.page.banner = alert
            self.page.banner.open = True

        self.weather_container.animate_opacity = 300
        self.weather_container.opacity = 0
        self.weather_container.visible = True
        self.page.update()
        await asyncio.sleep(0.1)
        self.weather_container.opacity = 1
        self.page.update()
        self.error_message.visible = False

    def create_info_card(self, icon, label, value):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=120,
        )

    def show_error(self, message: str):
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)
