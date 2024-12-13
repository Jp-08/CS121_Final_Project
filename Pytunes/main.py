import sqlite3
import customtkinter
from tkinter import messagebox, simpledialog

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("pytunes.db")
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Create tracks table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT NOT NULL,
            genre TEXT NOT NULL,
            release_year INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect("pytunes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# User registration
def register_user(username, password):
    conn = sqlite3.connect("pytunes.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Show login window
def show_login():
    login_window = customtkinter.CTkToplevel(app)
    login_window.title("Login")
    login_window.geometry("400x300")
    customtkinter.CTkLabel(login_window, text="Login to Pytunes", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Username and Password fields
    username_entry = customtkinter.CTkEntry(login_window, placeholder_text="Username")
    username_entry.pack(pady=10)
    password_entry = customtkinter.CTkEntry(login_window, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate_user(username, password):
            messagebox.showinfo("Login Success", "Welcome to Pytunes!")
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_register_window():
        login_window.destroy()
        show_register()

    # Add Login and Register buttons
    customtkinter.CTkButton(login_window, text="Login", command=login).pack(pady=10)
    customtkinter.CTkButton(login_window, text="Register", command=open_register_window).pack(pady=10)

# Show registration window
def show_register():
    register_window = customtkinter.CTkToplevel(app)
    register_window.title("Register")
    register_window.geometry("400x300")
    customtkinter.CTkLabel(register_window, text="Register for Pytunes", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Username and Password fields
    username_entry = customtkinter.CTkEntry(register_window, placeholder_text="Username")
    username_entry.pack(pady=10)
    password_entry = customtkinter.CTkEntry(register_window, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Registration Success", "Account created successfully!")
            register_window.destroy()
            show_login()
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    # Add Register button
    customtkinter.CTkButton(register_window, text="Register", command=register).pack(pady=10)

 # Initialize the main application window
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("900x600")
app.title("Pytunes")

# Initialize the database
init_db()

# Title Frame and Labels 
title_frame = customtkinter.CTkFrame(app, corner_radius=15, fg_color="#292929", width=800)
title_frame.pack(pady=40, padx=20)

title_label = customtkinter.CTkLabel(title_frame, text=" Pytunes \n Your Music Library ", font=("Helvetica", 30, "bold"), text_color="#FFD700", justify="center", wraplength=750)
title_label.pack(pady=15)

subtitle_label = customtkinter.CTkLabel(title_frame, text="Manage your music effortlessly with style and ease.", font=("Helvetica", 16, "italic"), text_color="#B0B0B0")
subtitle_label.pack(pady=5)

# Frame for displaying track details in a table-like format
track_list_frame = customtkinter.CTkFrame(app)
track_list_frame.pack(pady=20, padx=10)

# Function to fetch all tracks from the database
def get_tracks():
    conn = sqlite3.connect("pytunes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to create and refresh the table with track details
def refresh_tracks():
    # Clear the existing widgets
    for widget in track_list_frame.winfo_children():
        widget.destroy()

    tracks = get_tracks()

    if not tracks:
        customtkinter.CTkLabel(track_list_frame, text="No tracks available.", font=("Helvetica", 14)).pack(pady=10)
        return

    # Create table header
    headers = ["ID", "Title", "Artist", "Album", "Genre", "Release Year"]
    for col, header in enumerate(headers):
        customtkinter.CTkLabel(track_list_frame, text=header, font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

    # Display the tracks in a table-like grid
    for row, track in enumerate(tracks, start=1):
        customtkinter.CTkLabel(track_list_frame, text=str(track[0]), font=("Helvetica", 12)).grid(row=row, column=0, padx=10, pady=5)
        customtkinter.CTkLabel(track_list_frame, text=track[1], font=("Helvetica", 12)).grid(row=row, column=1, padx=10, pady=5)
        customtkinter.CTkLabel(track_list_frame, text=track[2], font=("Helvetica", 12)).grid(row=row, column=2, padx=10, pady=5)
        customtkinter.CTkLabel(track_list_frame, text=track[3], font=("Helvetica", 12)).grid(row=row, column=3, padx=10, pady=5)
        customtkinter.CTkLabel(track_list_frame, text=track[4], font=("Helvetica", 12)).grid(row=row, column=4, padx=10, pady=5)
        customtkinter.CTkLabel(track_list_frame, text=track[5], font=("Helvetica", 12)).grid(row=row, column=5, padx=10, pady=5)

def add_track():
    add_window = customtkinter.CTkToplevel(app)
    add_window.title("Add Track")
    add_window.geometry("600x600")

    customtkinter.CTkLabel(add_window, text="Add a New Track", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Input fields
    fields = {}
    field_names = ["Track Title", "Artist", "Album", "Genre", "Release Year"]
    for name in field_names:
        customtkinter.CTkLabel(add_window, text=f"{name}:", font=("Helvetica", 12)).pack(pady=5)
        field_entry = customtkinter.CTkEntry(add_window, font=("Helvetica", 12))
        field_entry.pack(pady=5)
        fields[name] = field_entry

    def submit_track():
        title = fields["Track Title"].get()
        artist = fields["Artist"].get()
        album = fields["Album"].get()
        genre = fields["Genre"].get()
        release_year = fields["Release Year"].get()

        if not title or not artist or not album or not genre or not release_year:
            messagebox.showinfo("Error", "All fields are required.")
            return

        try:
            user_id = 1  # Replace this with the logged-in user's ID
            conn = sqlite3.connect("pytunes.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tracks (title, artist, album, genre, release_year, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, artist, album, genre, int(release_year), user_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Track added successfully!")
            add_window.destroy()
            refresh_tracks()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding track: {e}")

    customtkinter.CTkButton(add_window, text="Add Track", command=submit_track, fg_color="green").pack(pady=20)

# Function to update an existing track
def update_track():
    update_window = customtkinter.CTkToplevel(app)
    update_window.title("Update Track")
    update_window.geometry("600x600")

    customtkinter.CTkLabel(update_window, text="Update Track", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Input fields
    fields = {}
    customtkinter.CTkLabel(update_window, text="Track ID:", font=("Helvetica", 12)).pack(pady=5)
    track_id_entry = customtkinter.CTkEntry(update_window, font=("Helvetica", 12))
    track_id_entry.pack(pady=5)

    field_names = ["Track Title", "Artist", "Album", "Genre", "Release Year"]
    for name in field_names:
        customtkinter.CTkLabel(update_window, text=f"{name}:", font=("Helvetica", 12)).pack(pady=5)
        field_entry = customtkinter.CTkEntry(update_window, font=("Helvetica", 12))
        field_entry.pack(pady=5)
        fields[name] = field_entry

    def submit_update():
        track_id = track_id_entry.get()
        if not track_id.isdigit():
            messagebox.showinfo("Error", "Invalid Track ID.")
            return

        track_id = int(track_id)
        title = fields["Track Title"].get()
        artist = fields["Artist"].get()
        album = fields["Album"].get()
        genre = fields["Genre"].get()
        release_year = fields["Release Year"].get()

        if not title or not artist or not album or not genre or not release_year:
            messagebox.showinfo("Error", "All fields are required.")
            return

        try:
            # Update the track in the database
            conn = sqlite3.connect("pytunes.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tracks
                SET title = ?, artist = ?, album = ?, genre = ?, release_year = ?
                WHERE track_id = ?
            """, (title, artist, album, genre, int(release_year), track_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Track updated successfully!")
            update_window.destroy()
            refresh_tracks()  # Refresh track list immediately
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating track: {e}")

    customtkinter.CTkButton(update_window, text="Update Track", command=submit_update, fg_color="blue").pack(pady=20)

# Function to delete a track
def delete_track():
    delete_window = customtkinter.CTkToplevel(app)
    delete_window.title("Delete Track")
    delete_window.geometry("400x300")

    customtkinter.CTkLabel(delete_window, text="Delete a Track", font=("Helvetica", 18, "bold")).pack(pady=20)

    # Input field for Track ID
    customtkinter.CTkLabel(delete_window, text="Track ID:", font=("Helvetica", 12)).pack(pady=5)
    track_id_entry = customtkinter.CTkEntry(delete_window, font=("Helvetica", 12))
    track_id_entry.pack(pady=10)

    def confirm_delete():
        track_id = track_id_entry.get()
        if not track_id.isdigit():
            messagebox.showinfo("Error", "Invalid Track ID.")
            return

        track_id = int(track_id)

        try:
            # Delete the track from the database
            conn = sqlite3.connect("pytunes.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tracks WHERE track_id = ?", (track_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Track deleted successfully!")
            delete_window.destroy()
            refresh_tracks()  # Refresh track list immediately
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting track: {e}")

    customtkinter.CTkButton(delete_window, text="Delete Track", command=confirm_delete, fg_color="#F44336").pack(pady=20)

# Refresh Tracks Button and other UI components (same as original code)
def refresh_library():
    refresh_tracks()
    messagebox.showinfo("Library Refreshed", "Track library has been refreshed successfully!")

# Navigation Bar and Buttons 
nav_bar = customtkinter.CTkFrame(app, height=50, fg_color="transparent")
nav_bar.pack(side="top", fill="x")


# Function to show the help information
def show_help():
    messagebox.showinfo(
        "Help",
        "Welcome to Pytunes!\n\n"
        "1. Add Track: Add a new track to your music library.\n"
        "2. Update Track: Edit an existing track's details.\n"
        "3. Delete Track: Remove a track from your library.\n"
        "4. Search Tracks: Use the search bar to find tracks easily.\n"
        "For more information, contact support at support@pytunes.com."
    )

# Function to show about information
def show_about():
    messagebox.showinfo(
        "About Pytunes",
        "Pytunes\nVersion 1.0\n\n"
        "Developed with love for music enthusiasts. Manage your music library "
        "effortlessly. Stay tuned for updates!"
    )


# Buttons
button_frame = customtkinter.CTkFrame(app, corner_radius=10)
button_frame.pack(pady=20)

# Add Track Button (Green)
customtkinter.CTkButton(
    button_frame,
    text="Add Track",
    command=add_track,
    width=200,
    fg_color="#4CAF50",  # Green color
    hover_color="#45A049"
).pack(pady=5)

# Update Track Button (Blue)
customtkinter.CTkButton(
    button_frame,
    text="Update Track",
    command=update_track,
    width=200,
    fg_color="#2196F3",  # Blue color
    hover_color="#1976D2"
).pack(pady=5)

# Delete Track Button (Red)
customtkinter.CTkButton(
    button_frame,
    text="Delete Track",
    command=delete_track,  
    width=200,
    fg_color="#F44336",  
    hover_color="#D32F2F"
).pack(pady=5)

# Navigation Buttons (Help, About, Refresh)
nav_bar = customtkinter.CTkFrame(app, height=50, fg_color="#202020")
nav_bar.pack(side="top", fill="x")

# Container for Navigation Buttons
nav_button_container = customtkinter.CTkFrame(nav_bar, fg_color="#202020")
nav_button_container.pack(expand=True)

# Help Button (Green)
customtkinter.CTkButton(
    nav_button_container,
    text="Help",
    width=100,
    fg_color="#4CAF50",
    hover_color="#45A049",
    command=show_help,
).pack(side="left", padx=10)

# About Button (Blue)
customtkinter.CTkButton(
    nav_button_container,
    text="About",
    width=100,
    fg_color="#2196F3",
    hover_color="#1976D2",
    command=show_about,
).pack(side="left", padx=10)

# Refresh Button (Red)
customtkinter.CTkButton(
    nav_button_container,
    text="Refresh",
    width=100,
    fg_color="#F44336",
    hover_color="#D32F2F",
    command=refresh_library,
).pack(side="left", padx=10)

init_db()

show_login()

refresh_tracks()

app.mainloop()
