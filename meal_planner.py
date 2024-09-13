
#imports for GUI, reading and writing CSV Files, for hashing passwords securely, for opening URLs in the browser
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import hashlib
import os
import webbrowser
from tkinter import font as tkfont

#global variables that contain user details and meal plan details
USER_DATA_FILE = 'users.csv'
MEAL_DATA_FILE = 'meal_plan.csv'


# loading  meal data from meal_plan.CSV
def load_meals():
    meals = []
    with open(MEAL_DATA_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            meals.append(row)
    return meals


#global meal data
meals = load_meals()

#creation of meal planner class
class MealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Planner")
        self.primary_color = '#f7fdd0'
        self.font_name = "Constantia"
        self.font_size = 14
        self.logged_in = False
        self.favorites = []
        self.meal_type = None
        self.create_initial_screen()

#creation of initial screen that has the welcome message, sign up and log in button
    def create_initial_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Welcome to the Meal Planner", font=title_font, bg=self.primary_color).pack(pady=20)
        tk.Button(self.root, text="Sign Up", font=button_font, command=self.create_sign_up_screen).pack(pady=10)
        tk.Button(self.root, text="Login", font=button_font, command=self.create_login_screen).pack(pady=10)

#creation of sign up page that has the form fields
    def create_sign_up_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        entry_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Sign Up", font=title_font, bg=self.primary_color).pack(pady=20)

        tk.Label(self.root, text="First Name:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, font=entry_font)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.root, text="Last Name:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, font=entry_font)
        self.last_name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.email_entry = tk.Entry(self.root, font=entry_font)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Username:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.signup_username_entry = tk.Entry(self.root, font=entry_font)
        self.signup_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.signup_password_entry = tk.Entry(self.root, show="*", font=entry_font)
        self.signup_password_entry.pack(pady=5)

        tk.Button(self.root, text="Sign Up", font=button_font, command=self.sign_up).pack(pady=20)
        tk.Button(self.root, text="Back", font=button_font, command=self.create_initial_screen).pack(pady=10)

#retrieves the user inputs, validates them, and then takes user to log in page.
    def sign_up(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.signup_username_entry.get().strip()
        password = self.signup_password_entry.get().strip()

        if not all([first_name, last_name, email, username, password]):
            tk.messagebox.showwarning("Sign Up Error", "All fields must be filled out.")
            return

        if not self.is_unique_username(username):
            tk.messagebox.showwarning("Sign Up Error", "Username already taken.")
            return

        if not self.is_valid_email(email):
            tk.messagebox.showwarning("Sign Up Error", "Invalid email format.")
            return
#creates a hash object, converts password to bytes then stores the password to a hexadecimal string
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.save_user(first_name, last_name, email, username, hashed_password)
        tk.messagebox.showinfo("Sign Up Success", "Sign up successful! Please log in.")
        self.create_login_screen()

#saves a new username details in the user CSV
    def is_unique_username(self, username):
        if not os.path.exists(USER_DATA_FILE):
            return True
        with open(USER_DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == username:
                    return False
        return True

    def is_valid_email(self, email):
        import re
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return re.match(email_regex, email) is not None

    def save_user(self, first_name, last_name, email, username, hashed_password):
        with open(USER_DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, email, username, hashed_password])

#takes the user to the log in screen after signing up
    def create_login_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        entry_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Login", font=title_font, bg=self.primary_color).pack(pady=20)

        tk.Label(self.root, text="Username:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=entry_font)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=entry_font)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", font=button_font, command=self.login).pack(pady=20)
        tk.Button(self.root, text="Back", font=button_font, command=self.create_initial_screen).pack(pady=10)

#checks if the username and hashed password match the stored credentials
    def login(self):
        self.current_user = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if self.verify_user(self.current_user, hashed_password):
            self.logged_in = True
            self.create_welcome_screen()
        else:
            tk.messagebox.showerror("Login Error", "Invalid username or password.")

    def verify_user(self, username, hashed_password):
        if not os.path.exists(USER_DATA_FILE):
            return False
        with open(USER_DATA_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[3] == username and row[4] == hashed_password:
                    return True
        return False

#once verified the user is taken to the welcome screen
    def create_welcome_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Welcome to the Meal Planner! What would you like to eat?", font=title_font,
                 bg=self.primary_color).pack(pady=20)

        tk.Button(self.root, text="Breakfast", font=button_font,
                  command=lambda: self.select_meal_category("Breakfast")).pack(pady=10)
        tk.Button(self.root, text="Lunch", font=button_font, command=lambda: self.select_meal_category("Lunch")).pack(
            pady=10)
        tk.Button(self.root, text="Supper", font=button_font, command=lambda: self.select_meal_category("Supper")).pack(
            pady=10)

# buttons to navigate to profile screen and to log out
        tk.Button(self.root, text="View Profile", font=button_font, command=self.create_profile_screen).pack(pady=10)
        tk.Button(self.root, text="Log Out", font=button_font, command=self.logout).pack(pady=20)

#displays users profile and their favourite meals
    def create_profile_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        if not self.logged_in:
            tk.messagebox.showwarning("Profile Error", "You must be logged in to view your profile.")
            self.create_login_screen()
            return

        username = self.current_user

        tk.Label(self.root, text=f"Hello, {username}!", font=title_font, bg=self.primary_color).pack(pady=20)

        categories = ["Breakfast", "Lunch", "Supper"]
        for category in categories:
            tk.Label(self.root, text=f"From the {category} category, here are your favorite meals:", font=label_font,
                     bg=self.primary_color).pack(pady=10)
            favorites_in_category = [meal for meal in self.favorites if meal["meal_type"] == category]

            if not favorites_in_category:
                tk.Label(self.root, text="No favorite meals in this category.", font=label_font,
                         bg=self.primary_color).pack(pady=5)
            else:
                for meal in favorites_in_category:
                    frame = tk.Frame(self.root, bg=self.primary_color)
                    frame.pack(pady=5, fill="x")

                    tk.Label(frame, text=meal["meal_name"], font=label_font, bg=self.primary_color).pack(side="left")
                    tk.Button(frame, text="See Recipe", font=button_font,
                              command=lambda link=meal["recipe_link"]: webbrowser.open(link)).pack(side="right")

                tk.Button(self.root, text=f"See Recommendations for {category}", font=button_font,
                          command=lambda cat=category: self.show_recommendations_by_category(cat)).pack(pady=10)

        tk.Button(self.root, text="Back to Main Menu", font=button_font, command=self.create_welcome_screen).pack(
            pady=20)

#user can log out which will take them to the initial screen
    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.favorites = []
        self.create_initial_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

#this shows recommendation based on the users favourite meal - the category used to recommend is ingredients
    def show_recommendations_by_category(self, category):
        if not self.favorites:
            tk.messagebox.showinfo("Recommendations", "No favorite meals to base recommendations on.")
            return

        ingredients = [meal["ingredients"] for meal in self.favorites if meal["meal_type"] == category]
        if not ingredients:
            tk.messagebox.showinfo("Recommendations", f"No ingredients to base recommendations for {category}.")
            return

        recommended_meals = [meal for meal in meals if meal["ingredients"] in ingredients and meal[
            "meal_type"] == category and meal not in self.favorites]

        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text=f"Recommended {category} Meals", font=title_font, bg=self.primary_color).pack(pady=20)

        for meal in recommended_meals[:2]:  # Show up to 2 recommendations
            frame = tk.Frame(self.root, bg=self.primary_color)
            frame.pack(pady=5, fill="x")

            tk.Label(frame, text=meal["meal_name"], font=label_font, bg=self.primary_color).pack(side="left")
            tk.Button(frame, text="See Recipe", font=button_font,
                      command=lambda link=meal["recipe_link"]: webbrowser.open(link)).pack(side="right")

        tk.Button(self.root, text="Back to Profile", font=button_font, command=self.create_profile_screen).pack(pady=20)

#selection of meal type that will take user to the categories page
    def select_meal_category(self, meal_type):
        self.meal_type = meal_type
        self.create_category_screen()

#creates a page that contains the sub-categories
    def create_category_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text=f"Select a filter for {self.meal_type}", font=title_font, bg=self.primary_color).pack(
            pady=20)

        tk.Button(self.root, text="Filter Meals", font=button_font, command=self.create_filter_screen).pack(pady=20)
        tk.Button(self.root, text="See Recommendations", font=button_font, command=self.show_recommendations).pack(
            pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=button_font, command=self.create_welcome_screen).pack(
            pady=10)

#creates a page that allows users to be able to filter the meals
    def create_filter_screen(self):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Apply Filters", font=title_font, bg=self.primary_color).pack(pady=20)

        self.filters = {
            "preparation_time": tk.StringVar(value="All"),
            "calories": tk.StringVar(value="All"),
            "ingredients": tk.StringVar(value="All")
        }

        tk.Label(self.root, text="Preparation Time:", font=label_font, bg=self.primary_color).pack(pady=5)
        ttk.Combobox(self.root, textvariable=self.filters["preparation_time"],
                     values=["All", "Quick and Easy", "Moderate", "Extended"]).pack(pady=5)

        tk.Label(self.root, text="Calories:", font=label_font, bg=self.primary_color).pack(pady=5)
        ttk.Combobox(self.root, textvariable=self.filters["calories"],
                     values=["All", "Low in Calories", "Medium in Calories", "High in Calories"]).pack(pady=5)

        tk.Label(self.root, text="Ingredients:", font=label_font, bg=self.primary_color).pack(pady=5)
        ttk.Combobox(self.root, textvariable=self.filters["ingredients"],
                     values=["All", "Rich in carbs", "Rich in lean proteins", "Rich in vegetables"]).pack(pady=5)

        tk.Label(self.root, text="Plan Duration:", font=label_font, bg=self.primary_color).pack(pady=5)
        self.plan_duration = tk.StringVar(value="Daily")
        ttk.Radiobutton(self.root, text="Daily", variable=self.plan_duration, value="Daily").pack(pady=5)
        ttk.Radiobutton(self.root, text="Weekly", variable=self.plan_duration, value="Weekly").pack(pady=5)

        tk.Button(self.root, text="Filter Meals", font=button_font, command=self.filter_meals).pack(pady=20)
        tk.Button(self.root, text="Back to Meal Options", font=button_font, command=self.create_welcome_screen).pack(
            pady=10)

#applies filters to the meal list and displays the filtered result
    def filter_meals(self):
        filtered_meals = [meal for meal in meals if meal["meal_type"] == self.meal_type]

        prep_time = self.filters["preparation_time"].get()
        calories = self.filters["calories"].get()
        ingredients = self.filters["ingredients"].get()

        if prep_time != "All":
            filtered_meals = [meal for meal in filtered_meals if meal["preparation_time"] == prep_time]
        if calories != "All":
            filtered_meals = [meal for meal in filtered_meals if meal["calories"] == calories]
        if ingredients != "All":
            filtered_meals = [meal for meal in filtered_meals if meal["ingredients"] == ingredients]

#filters meals according to the daily or weekly option
        if self.plan_duration.get() == "Daily":
            filtered_meals = filtered_meals[:1]  # Show only one meal for the day
        elif self.plan_duration.get() == "Weekly":
            filtered_meals = filtered_meals[:7]  # Show up to seven meals for the week

        self.show_meals(filtered_meals)

#displays the list of filtered meals or all meals if no filter is applied.
    def show_meals(self, meals):
        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        if self.plan_duration.get() == "Daily":
            tk.Label(self.root, text="Your meal for the day is:", font=title_font, bg=self.primary_color).pack(pady=20)
        else:
            tk.Label(self.root, text=f"Meals for the week:", font=title_font, bg=self.primary_color).pack(pady=20)

        for meal in meals:
            frame = tk.Frame(self.root, bg=self.primary_color)
            frame.pack(pady=5, fill="x")

            tk.Label(frame, text=meal["meal_name"], font=label_font, bg=self.primary_color).pack(side="left")
            tk.Button(frame, text="See Recipe", font=button_font,
                      command=lambda link=meal["recipe_link"]: webbrowser.open(link)).pack(side="right")

            if meal in self.favorites:
                tk.Button(frame, text="Unfavorite", font=button_font,
                          command=lambda m=meal: self.toggle_favorite(m)).pack(side="right")
            else:
                tk.Button(frame, text="Favorite", font=button_font,
                          command=lambda m=meal: self.toggle_favorite(m)).pack(side="right")

        tk.Button(self.root, text="Back to Category", font=button_font, command=self.create_category_screen).pack(
            pady=10)
        tk.Button(self.root, text="Log Out", font=button_font, command=self.logout).pack(pady=10)

#checks if the meal is a favourite, when added or removed a message is displayed
    def toggle_favorite(self, meal):
        if meal in self.favorites:
            self.favorites.remove(meal)
            tk.messagebox.showinfo("Removed from Favorites",
                                   f"The meal '{meal['meal_name']}' has been removed from your favorites.")
        else:
            self.favorites.append(meal)
            tk.messagebox.showinfo("Added to Favorites",
                                   f"The meal '{meal['meal_name']}' has been added to your favorites.")

# after updating favorites it automatically takes the user to the category section
        self.create_category_screen()

#provides meal recommendations based on the user’s favorite meals.
    def show_recommendations(self):
        if not self.favorites:
            tk.messagebox.showinfo("Recommendations", "No favorite meals to base recommendations on.")
            return

        ingredients = [meal["ingredients"] for meal in self.favorites]
        if not ingredients:
            tk.messagebox.showinfo("Recommendations", "No ingredients to base recommendations on.")
            return

        recommended_meals = [
            meal for meal in meals
            if meal["ingredients"] in ingredients and meal["meal_type"] == self.meal_type and meal not in self.favorites
        ]

        self.clear_window()
        self.root.configure(bg=self.primary_color)

        title_font = tkfont.Font(family=self.font_name, size=16)
        label_font = tkfont.Font(family=self.font_name, size=self.font_size)
        button_font = tkfont.Font(family=self.font_name, size=self.font_size)

        tk.Label(self.root, text="Recommended Meals", font=title_font, bg=self.primary_color).pack(pady=20)

        for meal in recommended_meals[:2]:  # Show up to 2 recommendations
            frame = tk.Frame(self.root, bg=self.primary_color)
            frame.pack(pady=5, fill="x")

            tk.Label(frame, text=meal["meal_name"], font=label_font, bg=self.primary_color).pack(side="left")
            tk.Button(frame, text="See Recipe", font=button_font,
                      command=lambda link=meal["recipe_link"]: webbrowser.open(link)).pack(side="right")

        tk.Button(self.root, text="Back to Category", font=button_font, command=self.create_category_screen).pack(
            pady=10)
        tk.Button(self.root, text="Back to Main Menu", font=button_font, command=self.create_welcome_screen).pack(
            pady=10)

#allows the user to log out and return to the initial screen
    def logout(self):
        self.logged_in = False
        self.create_initial_screen()

#clears all widgets from the window.
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

#starts the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()