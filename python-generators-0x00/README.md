# alx-backend-python
# Python Generators Project

## Database CSV Importer with UUID Generation

This project demonstrates importing user data from a CSV file into a MySQL database while automatically generating UUID primary keys.

# Features
- Creates MySQL database and table automatically
- Reads user data from CSV file (name, email, age)
- Generates UUIDs for each user record
- Handles errors and connection management properly
- Uses Python generators for efficiency

# Things to have
- Python 3.x
- MySQL Server 5.7+
- mysql-connector-python package

Database schema
CREATE TABLE user_data (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age INT NOT NULL
)

##File structure
.Python-Generators-0x00
├── 0-main.py        # Main execution script
├── seed.py          # Database operations
├── user_data.csv    # Sample data (name,email,age)
└── README.md        # This file


# Output received

Database ALX_prodev created successfully
connection successful
Table user_data created successfully
Data inserted with generated UUIDs
Database ALX_prodev is present 
[('0005957a-651e-4992-874f-9b926a4ea022', 'Lauren Beahan', 'Spencer_DuBuque43@yahoo.com', Decimal('71')), ('017ba183-e288-4l.com', Decimal('91')), ('027207ea-b90a-49c9-820b-f4a2cdad7d7f', 'Shannon Ankunding', 'Ronniel.com', Decimal('91')), ('027207ea-b90a-49c9-820b-f4a2cdad7d7f', 'Shannon Ankunding', 'Ronnie32@yahoo.com', Decimal('61'))]
PS C:\Users\cliff\OneDrive - Strathmore University\Documents\ALX Prodev Back End Web Dev Program\Github Repos\alx-backend-python\python-generators-0x00>