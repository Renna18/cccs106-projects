import flet as ft
from database import (
    update_contact_db,
    delete_contact_db,
    add_contact_db,
    get_all_contacts_db
)


def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView with optional search."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)  # ✅ now supports search

    for contact in contacts:
        contact_id, name, phone, email = contact
        contacts_list_view.controls.append(
            ft.Card(
                elevation=3,
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                                    ft.PopupMenuButton(
                                        icon=ft.Icons.MORE_VERT,
                                        items=[
                                            ft.PopupMenuItem(
                                                text="Edit",
                                                icon=ft.Icons.EDIT,
                                                on_click=lambda _, c=contact: open_edit_dialog(
                                                    page, c, db_conn, contacts_list_view
                                                ),
                                            ),
                                            ft.PopupMenuItem(),  # separator
                                            ft.PopupMenuItem(
                                                text="Delete",
                                                icon=ft.Icons.DELETE,
                                                on_click=lambda _, cid=contact_id: delete_contact(
                                                    page, cid, db_conn, contacts_list_view
                                                ),
                                            ),
                                        ],
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.PHONE, size=16),
                                    ft.Text(phone if phone else "N/A"),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.EMAIL, size=16),
                                    ft.Text(email if email else "N/A"),
                                ]
                            ),
                        ],
                        spacing=5,
                    ),
                ),
            )
        )
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn, search_field=None):
    """Adds a new contact and refreshes the list."""
    name_input, phone_input, email_input = inputs

    # ✅ Input validation: check if name is empty
    if not name_input.value.strip():
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    else:
        name_input.error_text = None  # clear error if previously set

    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    # Clear the input fields after adding
    for field in inputs:
        field.value = ""

    # ✅ Refresh list with search applied (if search field exists)
    display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view, search_field=None):
    """Shows confirmation before deleting a contact."""

    def confirm_delete(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        # ✅ Refresh with current search term
        display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")

    def cancel_delete(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_delete),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
    )

    page.open(dialog)


def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_field=None):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        update_contact_db(
            db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value
        )
        dialog.open = False
        page.update()
        # ✅ Refresh with current search term
        display_contacts(page, contacts_list_view, db_conn, search_field.value if search_field else "")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email]),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=lambda e: setattr(dialog, "open", False) or page.update(),
            ),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )

    page.open(dialog)


def create_search_bar(page, contacts_list_view, db_conn):
    """Creates a search TextField for filtering contacts."""
    search_field = ft.TextField(
        label="Search contacts",
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, search_field.value),
        expand=True,
    )
    return search_field