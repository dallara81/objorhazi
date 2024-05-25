# Hotel Software v1.0
# (c) 2024 Ferenc Szilvai

from abc import ABC, abstractmethod
from datetime import datetime


# Abstract base class for rooms
class Room(ABC):
    def __init__(self, rate, room_no):
        self.rate = rate  # Room rate
        self.room_no = room_no  # Room number


# Single room class inheriting from Room
class SingleRoom(Room):
    def __init__(self, room_no):
        super().__init__(rate=30000, room_no=room_no)  # Single room rate set to 30000
        self.category = "single"  # Room category


# Double room class inheriting from Room
class DoubleRoom(Room):
    def __init__(self, room_no):
        super().__init__(rate=40000, room_no=room_no)  # Double room rate set to 40000
        self.category = "double"  # Room category


# Hotel class to manage rooms and bookings
class Hotel:
    def __init__(self, name):
        self.name = name  # Hotel name
        self.rooms = []  # List to store rooms
        self.bookings = []  # List to store bookings

    # Method to add a room to the hotel
    def add_room(self, room):
        self.rooms.append(room)

    # Method to reserve a room
    def reserve_room(self, room_no, date):
        # Validate date
        if datetime.strptime(date, '%Y-%m-%d') <= datetime.now():
            return "Invalid date. Please provide a future date."
        for room in self.rooms:
            if room.room_no == room_no:
                for booking in self.bookings:
                    if booking.room.room_no == room_no and booking.date == date:
                        return "This room is already booked on this date."
                new_booking = Booking(room, date)
                self.bookings.append(new_booking)
                return f"The booking cost is: {new_booking.room.rate} Ft"
        return "No such room number."

    # Method to cancel a reservation
    def cancel_reservation(self, room_no, date):
        for booking in self.bookings:
            if booking.room.room_no == room_no and booking.date == date:
                self.bookings.remove(booking)
                return "Booking successfully canceled."
        return "No such booking exists."

    # Method to list all bookings
    def list_bookings(self):
        if not self.bookings:
            return "No bookings."
        return [(booking.room.room_no, booking.room.category, booking.date) for booking in self.bookings]

    # Method to check available rooms on a specific date
    def check_available_rooms(self, date):
        """Get the list of available rooms for a given date."""
        try:
            # Validate date format
            valid_date = datetime.strptime(date, '%Y-%m-%d')
            if valid_date <= datetime.now():
                return "The provided date is in the past. Please provide a future date."
        except ValueError:
            return "Invalid date format. Please use the following format: yyyy-mm-dd."

        available_rooms = [room for room in self.rooms if not any(
            booking.date == date and booking.room.room_no == room.room_no for booking in self.bookings)]
        if not available_rooms:
            return "No available rooms on this date."
        return available_rooms


# Booking class to represent a room booking
class Booking:
    def __init__(self, room, date):
        self.room = room  # Room being booked
        self.date = date  # Booking date


# Initializing the hotel and pre-loading data
hotel = Hotel("Star Hotel")
hotel.add_room(SingleRoom(101))
hotel.add_room(DoubleRoom(102))
hotel.add_room(SingleRoom(103))
hotel.reserve_room(101, "2024-06-01")
hotel.reserve_room(102, "2024-06-01")
hotel.reserve_room(103, "2024-06-02")
hotel.reserve_room(101, "2024-06-03")
hotel.reserve_room(102, "2024-06-04")


# User interface function for interacting with the hotel system
def user_interface():
    print("\n *** Welcome to Wild East Hotel! Please use button 4 to view our available rooms. ***")

    while True:
        print("\nSelect the desired operation:")
        print("1 - Book a room")
        print("2 - Cancel a booking")
        print("3 - List bookings")
        print("4 - Available rooms for a specific date")
        print("5 - Exit")

        option = input("Please choose an option (1-5): ")

        if option == "1":
            room_no = int(input("Enter the room number: "))
            date = input("Enter the booking date (in yyyy-mm-dd format, e.g., 2024-06-01): ")
            try:
                # Validate the date
                valid_date = datetime.strptime(date, '%Y-%m-%d')
                # Check if the date is in the future
                if valid_date <= datetime.now():
                    raise ValueError("The date cannot be in the past.")
                # If the date is valid, proceed with the booking
                print(hotel.reserve_room(room_no, date))
            except ValueError as e:
                print(f"The date was entered incorrectly, please try again. Error: {e}")
        elif option == "2":
            room_no = int(input("Enter the room number: "))
            date = input("Enter the booking date (in yyyy-mm-dd format): ")
            print(hotel.cancel_reservation(room_no, date))
        elif option == "3":
            bookings = hotel.list_bookings()
            if isinstance(bookings, str):
                print(bookings)
            else:
                for booking in bookings:
                    print(f"Room number: {booking[0]}, Type: {booking[1]}, Date: {booking[2]}")

        elif option == "4":
            date = input("Enter the date to check available rooms (in yyyy-mm-dd format, e.g., 2024-06-01): ")
            result = hotel.check_available_rooms(date)
            if isinstance(result, str):
                print(result)  # Display error message or information text
            else:
                print("Available rooms for the date: " + date)
                for room in result:
                    print(f"Room number: {room.room_no}, Type: {room.category}, Price: {room.rate} Ft")
        elif option == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")


# Run the user interface
user_interface()