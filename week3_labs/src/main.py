import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # Page configuration
    page.window_frameless = False
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_height = 350
    page.window_width = 400
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # Controls
    title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER
    )

    username = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )

    password = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        password=True,
        can_reveal_password=True,
        icon=ft.Icons.LOCK,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT
    )

    def show_dialog(title, message, icon, color):
        dlg = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=20),  
            title=ft.Row(
                [
                    ft.Icon(name=icon, color=color, size=35),
                    ft.Text(title, weight=ft.FontWeight.BOLD, size=18),
                ],
                alignment="center",
                spacing=10,
            ),
            content=ft.Text(
                message,
                text_align=ft.TextAlign.CENTER,
                size=14,
            ),
            actions=[
                ft.TextButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_100,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda e: page.close(dlg),
                )
            ],
            actions_alignment="center",
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # Login logic
    def login_click(e):
        print("Login button clicked!")
        if not username.value or not password.value:
            show_dialog("Input Error", "Please enter username and password", ft.Icons.INFO, "blue")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username=%s AND password=%s",
                (username.value, password.value)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                show_dialog("Login Successful", f"Welcome, {username.value}!", ft.Icons.CHECK_CIRCLE, "green")
            else:
                show_dialog("Login Failed", "Invalid username or password", ft.Icons.ERROR, "red")

        except mysql.connector.Error as err:   
            print("MYSQL ERROR:", err)         
            show_dialog("Database Error", str(err), ft.Icons.ERROR, "orange")

    login_btn = ft.ElevatedButton(
        text="Login",
        icon=ft.Icons.LOGIN,
        width=100,
        on_click=login_click
    )

    # Layout
    page.add(
        title,
        ft.Container(
            content=ft.Column([username, password], spacing=20),
        ),
        ft.Container(
            content=login_btn,
            margin=ft.margin.Margin(0, 20, 40, 0),
            alignment=ft.alignment.top_right
        )
    )

ft.app(target=main)