from club.models import User

def run():
    users = [
        {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@example.com",
            "phone_number": "1234567890",
            "is_admin": True,
            "is_board": True,
            "department": User.Department.FINANCE,
        },
        {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "phone_number": "2345678901",
            "is_admin": False,
            "is_board": True,
            "department": User.Department.MARKETING,
        },
        {
            "first_name": "Carol",
            "last_name": "Williams",
            "email": "carol.williams@example.com",
            "phone_number": "3456789012",
            "is_admin": False,
            "is_board": False,
            "department": User.Department.TECHNICAL_TEAM,
        },
        {
            "first_name": "David",
            "last_name": "Brown",
            "email": "david.brown@example.com",
            "phone_number": "4567890123",
            "is_admin": True,
            "is_board": True,
            "department": User.Department.HR,
        },
        {
            "first_name": "Eve",
            "last_name": "Davis",
            "email": "eve.davis@example.com",
            "phone_number": "5678901234",
            "is_admin": False,
            "is_board": False,
            "department": User.Department.ER,
        },
    ]

    for user_data in users:
        if not User.objects.filter(email=user_data["email"]).exists():
            user = User(**user_data)
            user.set_password("password123")
            user.save()
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user_data['email']}")

    print("Sample users processed.")
