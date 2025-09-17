import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact


def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT  # default theme

    # Initialize database connection
    db_conn = init_db()

    # Input fields
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)

    # Contacts list
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    # Search field
    search_field = ft.TextField(
        label="Search by name",
        width=350,
        on_change=lambda e: display_contacts(
            page, contacts_list_view, db_conn, e.control.value
        ),
    )

    # Add contact button
    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn),
    )

    # Dark mode switch
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if theme_switch.value else ft.ThemeMode.LIGHT
        )
        page.update()

    theme_switch = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    # Layout
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
                        theme_switch,  # theme toggle
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                search_field,  # search bar added
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                contacts_list_view,
            ]
        )
    )

    # Load existing contacts
    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)