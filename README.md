# SkillLink - Freelancer Marketplace GUI Application

A desktop application built with Python and Tkinter for managing a freelancer marketplace platform. This application provides an intuitive interface to browse freelancers, projects, proposals, contracts, and search for talent by skills.

## Features

- **Freelancer Management**: View all freelancers with their profiles, skills, and ratings
- **Project Browsing**: Browse available projects with budget and deadline information
- **Proposal Tracking**: View proposals submitted for specific projects
- **Contract Management**: Track active contracts and their milestones
- **Skill Search**: Find freelancers by specific skills and proficiency levels
- **Detailed Views**: Double-click on items to see detailed information

## Prerequisites

Before running this application, make sure you have:

1. **Python 3.6 or higher** installed
2. **PostgreSQL** installed and running
3. **Tkinter** (usually comes with Python)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` - PostgreSQL adapter for Python

### Step 2: Set Up PostgreSQL Database

1. Create a new PostgreSQL database named `skilllink`:

```sql
CREATE DATABASE skilllink;
```

2. Connect to the database and run the SQL script provided in `skilllink database.sql` to create tables and populate sample data:

```bash
psql -U postgres -d skilllink -f "skilllink database.sql"
```

Or open your PostgreSQL client and execute the contents of the SQL file.

### Step 3: Configure Database Connection

Edit the `config.py` file or use the application's Database Settings menu to configure your connection:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'skilllink',
    'user': 'postgres',
    'password': 'your_password_here'  # Add your PostgreSQL password
}
```

## Running the Application

Run the main application file:

```bash
python skilllink_app.py
```

## Application Structure

```
apppy/
├── skilllink_app.py      # Main application with GUI
├── database.py           # Database connection and query methods
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Usage Guide

### Freelancers Tab

- View all freelancers in the system
- See their headline, hourly rate, and average rating
- **Double-click** on any freelancer to see detailed profile including skills

### Projects Tab

- Browse all available projects
- View budget ranges and deadlines
- **Double-click** on any project to see full description and required skills

### Proposals Tab

- Enter a Project ID to view all proposals for that project
- See freelancer bids and cover letters
- Compare different proposals

### Contracts Tab

- View all active contracts
- See client, freelancer, and contract amounts
- **Double-click** on a contract to view its milestones

### Search Tab

- Search for freelancers by skill name
- Results show proficiency levels and ratings
- Helps find the best talent for specific skills

## Database Schema Overview

The application works with the following main tables:

- **users** - User accounts (clients, freelancers, admins)
- **freelancer_profile** - Freelancer profiles and ratings
- **skill** - Available skills in the platform
- **freelancer_skill** - Skills possessed by freelancers
- **project** - Posted projects
- **proposal** - Proposals submitted by freelancers
- **contract** - Active contracts
- **milestone** - Contract milestones
- **payment** - Payment records
- **review** - Reviews and ratings

## Features in Detail

### Database Connection Settings

Access via: **Database → Connection Settings**

Modify your database connection parameters without editing code.

### Refresh Data

Access via: **File → Refresh All**

Reload all data from the database to see the latest updates.

### About

Access via: **Help → About**

View application information and version.

## Troubleshooting

### Connection Error

If you see "Failed to connect to database":

1. Check that PostgreSQL is running
2. Verify your database credentials in `config.py`
3. Ensure the `skilllink` database exists
4. Check that the database is accepting connections

### No Data Displayed

If tables are empty:

1. Verify the SQL script was executed successfully
2. Click "Refresh" buttons in each tab
3. Use **File → Refresh All** from the menu

### Import Errors

If you see "No module named 'psycopg2'":

```bash
pip install psycopg2-binary
```

## Sample Data

The application comes pre-populated with sample data including:

- 12 users (3 clients, 8 freelancers, 1 admin)
- 10 skills (Python, SQL, React, Django, etc.)
- 10 projects with various budgets
- Multiple proposals and active contracts
- Reviews and ratings

## Future Enhancements

Potential features to add:

- User authentication and role-based access
- Add/Edit/Delete functionality for all entities
- Advanced filtering and sorting
- Reports and analytics
- Export data to CSV/PDF
- Real-time notifications

## Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter
- **Database**: PostgreSQL
- **Database Adapter**: psycopg2

## License

This is an educational project for database and GUI programming.

## Support

For issues or questions:

1. Check the PostgreSQL logs
2. Verify your Python version is 3.6+
3. Ensure all dependencies are installed
4. Check that the database schema matches the application queries
# database-systems-project
