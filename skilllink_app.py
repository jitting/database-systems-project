"""
SkillLink - Freelancer Marketplace GUI Application
Main application file with tabbed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import DatabaseConnection
from config import DB_CONFIG
from typing import Optional


class SkillLinkApp:
    """Main application class for SkillLink GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("SkillLink - Freelancer Marketplace")
        self.root.geometry("1200x700")

        # Database connection
        self.db = DatabaseConnection(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

        # Try to connect to database FIRST
        if not self.db.connect():
            messagebox.showerror("Database Error",
                                 "Failed to connect to database.\n"
                                 "Please check your connection settings.")
            self.root.quit()
            return

        # Initialize UI after successful connection
        self.setup_ui()

    def setup_ui(self):
        """Setup main UI components"""
        # Create menu bar
        self.create_menu()

        # Create main container with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.create_freelancers_tab()
        self.create_projects_tab()
        self.create_proposals_tab()
        self.create_contracts_tab()
        self.create_search_tab()
        self.create_client_dashboard_tab()
        self.create_admin_panel_tab()

    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh All", command=self.refresh_all_tabs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Database menu
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Connection Settings", command=self.show_db_settings)
        db_menu.add_command(label="Reconnect", command=self.reconnect_db)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_freelancers_tab(self):
        """Create tab for browsing freelancers"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Freelancers")

        # Top section with controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Freelancers", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Refresh", command=self.load_freelancers).pack(side=tk.RIGHT, padx=5)

        # Treeview for displaying freelancers
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.freelancers_tree = ttk.Treeview(tree_frame,
                                             columns=("ID", "Username", "Headline", "Rate/Hour", "Rating"),
                                             show="headings",
                                             yscrollcommand=vsb.set,
                                             xscrollcommand=hsb.set)

        vsb.config(command=self.freelancers_tree.yview)
        hsb.config(command=self.freelancers_tree.xview)

        # Configure columns
        self.freelancers_tree.heading("ID", text="ID")
        self.freelancers_tree.heading("Username", text="Username")
        self.freelancers_tree.heading("Headline", text="Headline")
        self.freelancers_tree.heading("Rate/Hour", text="Rate/Hour ($)")
        self.freelancers_tree.heading("Rating", text="Avg Rating")

        self.freelancers_tree.column("ID", width=50)
        self.freelancers_tree.column("Username", width=150)
        self.freelancers_tree.column("Headline", width=300)
        self.freelancers_tree.column("Rate/Hour", width=100)
        self.freelancers_tree.column("Rating", width=100)

        # Pack treeview and scrollbars
        self.freelancers_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click to show details
        self.freelancers_tree.bind("<Double-1>", self.show_freelancer_details)

        # Details section
        details_frame = ttk.LabelFrame(frame, text="Freelancer Details", padding=10)
        details_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.freelancer_details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap=tk.WORD)
        self.freelancer_details_text.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.load_freelancers()

    def create_projects_tab(self):
        """Create tab for browsing projects"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Projects")

        # Top section with controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Projects", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Refresh", command=self.load_projects).pack(side=tk.RIGHT, padx=5)

        # Treeview for displaying projects
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.projects_tree = ttk.Treeview(tree_frame,
                                          columns=("ID", "Title", "Min Budget", "Max Budget", "Deadline"),
                                          show="headings",
                                          yscrollcommand=vsb.set,
                                          xscrollcommand=hsb.set)

        vsb.config(command=self.projects_tree.yview)
        hsb.config(command=self.projects_tree.xview)

        # Configure columns
        self.projects_tree.heading("ID", text="ID")
        self.projects_tree.heading("Title", text="Title")
        self.projects_tree.heading("Min Budget", text="Min Budget ($)")
        self.projects_tree.heading("Max Budget", text="Max Budget ($)")
        self.projects_tree.heading("Deadline", text="Deadline")

        self.projects_tree.column("ID", width=50)
        self.projects_tree.column("Title", width=300)
        self.projects_tree.column("Min Budget", width=120)
        self.projects_tree.column("Max Budget", width=120)
        self.projects_tree.column("Deadline", width=120)

        self.projects_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click to show details
        self.projects_tree.bind("<Double-1>", self.show_project_details)

        # Details section
        details_frame = ttk.LabelFrame(frame, text="Project Details", padding=10)
        details_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.project_details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap=tk.WORD)
        self.project_details_text.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.load_projects()

    def create_proposals_tab(self):
        """Create tab for viewing proposals"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Proposals")

        # Input section
        input_frame = ttk.LabelFrame(frame, text="View Proposals", padding=10)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Project ID:").grid(row=0, column=0, padx=5, pady=5)
        self.proposal_project_id = ttk.Entry(input_frame, width=20)
        self.proposal_project_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="View Proposals for Project",
                   command=self.load_proposals_by_project).grid(row=0, column=2, padx=5, pady=5)

        # Treeview for displaying proposals
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.proposals_tree = ttk.Treeview(tree_frame,
                                           columns=("Freelancer", "Bid Amount", "Status", "Cover Letter"),
                                           show="headings",
                                           yscrollcommand=vsb.set,
                                           xscrollcommand=hsb.set)

        vsb.config(command=self.proposals_tree.yview)
        hsb.config(command=self.proposals_tree.xview)

        self.proposals_tree.heading("Freelancer", text="Freelancer")
        self.proposals_tree.heading("Bid Amount", text="Bid Amount ($)")
        self.proposals_tree.heading("Status", text="Status")
        self.proposals_tree.heading("Cover Letter", text="Cover Letter")

        self.proposals_tree.column("Freelancer", width=150)
        self.proposals_tree.column("Bid Amount", width=120)
        self.proposals_tree.column("Status", width=100)
        self.proposals_tree.column("Cover Letter", width=400)

        self.proposals_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def create_contracts_tab(self):
        """Create tab for viewing contracts"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Contracts")

        # Top section with controls
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Active Contracts", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Refresh", command=self.load_contracts).pack(side=tk.RIGHT, padx=5)

        # Treeview for displaying contracts
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.contracts_tree = ttk.Treeview(tree_frame,
                                           columns=("Contract ID", "Client ID", "Freelancer ID",
                                                    "Total Amount", "Status"),
                                           show="headings",
                                           yscrollcommand=vsb.set,
                                           xscrollcommand=hsb.set)

        vsb.config(command=self.contracts_tree.yview)
        hsb.config(command=self.contracts_tree.xview)

        self.contracts_tree.heading("Contract ID", text="Contract ID")
        self.contracts_tree.heading("Client ID", text="Client ID")
        self.contracts_tree.heading("Freelancer ID", text="Freelancer ID")
        self.contracts_tree.heading("Total Amount", text="Total Amount ($)")
        self.contracts_tree.heading("Status", text="Status")

        self.contracts_tree.column("Contract ID", width=100)
        self.contracts_tree.column("Client ID", width=100)
        self.contracts_tree.column("Freelancer ID", width=120)
        self.contracts_tree.column("Total Amount", width=120)
        self.contracts_tree.column("Status", width=100)

        self.contracts_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click to show milestones
        self.contracts_tree.bind("<Double-1>", self.show_contract_milestones)

        # Milestones section
        milestones_frame = ttk.LabelFrame(frame, text="Contract Milestones", padding=10)
        milestones_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        self.milestones_text = scrolledtext.ScrolledText(milestones_frame, height=6, wrap=tk.WORD)
        self.milestones_text.pack(fill=tk.BOTH, expand=True)

        # Load initial data
        self.load_contracts()

    def create_search_tab(self):
        """Create tab for searching"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Search")

        # Search by skill section
        search_frame = ttk.LabelFrame(frame, text="Search Freelancers by Skill", padding=10)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Skill Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_skill_entry = ttk.Entry(search_frame, width=30)
        self.search_skill_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(search_frame, text="Search",
                   command=self.search_by_skill).grid(row=0, column=2, padx=5, pady=5)

        # Results treeview
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.search_tree = ttk.Treeview(tree_frame,
                                        columns=("Username", "Skill", "Proficiency", "Rating"),
                                        show="headings",
                                        yscrollcommand=vsb.set,
                                        xscrollcommand=hsb.set)

        vsb.config(command=self.search_tree.yview)
        hsb.config(command=self.search_tree.xview)

        self.search_tree.heading("Username", text="Username")
        self.search_tree.heading("Skill", text="Skill")
        self.search_tree.heading("Proficiency", text="Proficiency Level")
        self.search_tree.heading("Rating", text="Avg Rating")

        self.search_tree.column("Username", width=200)
        self.search_tree.column("Skill", width=200)
        self.search_tree.column("Proficiency", width=150)
        self.search_tree.column("Rating", width=120)

        self.search_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def create_client_dashboard_tab(self):
        """Create tab for client dashboard"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Client Dashboard")

        # Client selection
        client_frame = ttk.LabelFrame(frame, text="Select Client", padding=10)
        client_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(client_frame, text="Client ID:").grid(row=0, column=0, padx=5, pady=5)
        self.client_id_entry = ttk.Entry(client_frame, width=20)
        self.client_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(client_frame, text="Load Dashboard",
                   command=self.load_client_dashboard).grid(row=0, column=2, padx=5, pady=5)

        # My Projects section
        projects_section = ttk.LabelFrame(frame, text="My Projects", padding=10)
        projects_section.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Projects treeview
        tree_frame = ttk.Frame(projects_section)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        self.client_projects_tree = ttk.Treeview(tree_frame,
                                                  columns=("ID", "Title", "Budget", "Proposals", "Status"),
                                                  show="headings",
                                                  yscrollcommand=vsb.set)
        vsb.config(command=self.client_projects_tree.yview)

        self.client_projects_tree.heading("ID", text="Project ID")
        self.client_projects_tree.heading("Title", text="Title")
        self.client_projects_tree.heading("Budget", text="Budget Range")
        self.client_projects_tree.heading("Proposals", text="# Proposals")
        self.client_projects_tree.heading("Status", text="Status")

        self.client_projects_tree.column("ID", width=80)
        self.client_projects_tree.column("Title", width=250)
        self.client_projects_tree.column("Budget", width=150)
        self.client_projects_tree.column("Proposals", width=100)
        self.client_projects_tree.column("Status", width=100)

        self.client_projects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind to show proposals
        self.client_projects_tree.bind("<Double-1>", self.show_project_proposals_for_client)

    def create_admin_panel_tab(self):
        """Create tab for admin panel"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Admin Panel")

        # Statistics section
        stats_frame = ttk.LabelFrame(frame, text="Platform Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)

        self.stats_text = tk.Text(stats_frame, height=6, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.X)

        ttk.Button(stats_frame, text="Refresh Statistics",
                   command=self.load_admin_stats).pack(pady=5)

        # User Management section
        user_mgmt_frame = ttk.LabelFrame(frame, text="User Management", padding=10)
        user_mgmt_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # User filter
        filter_frame = ttk.Frame(user_mgmt_frame)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="Filter by Role:").pack(side=tk.LEFT, padx=5)
        self.admin_role_filter = ttk.Combobox(filter_frame,
                                               values=["All", "client", "freelancer", "admin"],
                                               state="readonly",
                                               width=15)
        self.admin_role_filter.set("All")
        self.admin_role_filter.pack(side=tk.LEFT, padx=5)

        ttk.Button(filter_frame, text="Load Users",
                   command=self.load_admin_users).pack(side=tk.LEFT, padx=5)

        # Users treeview
        tree_frame = ttk.Frame(user_mgmt_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        self.admin_users_tree = ttk.Treeview(tree_frame,
                                              columns=("ID", "Username", "Email", "Role", "Status", "Joined"),
                                              show="headings",
                                              yscrollcommand=vsb.set)
        vsb.config(command=self.admin_users_tree.yview)

        self.admin_users_tree.heading("ID", text="User ID")
        self.admin_users_tree.heading("Username", text="Username")
        self.admin_users_tree.heading("Email", text="Email")
        self.admin_users_tree.heading("Role", text="Role")
        self.admin_users_tree.heading("Status", text="Status")
        self.admin_users_tree.heading("Joined", text="Joined At")

        self.admin_users_tree.column("ID", width=60)
        self.admin_users_tree.column("Username", width=120)
        self.admin_users_tree.column("Email", width=200)
        self.admin_users_tree.column("Role", width=80)
        self.admin_users_tree.column("Status", width=80)
        self.admin_users_tree.column("Joined", width=150)

        self.admin_users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Admin actions
        actions_frame = ttk.Frame(user_mgmt_frame)
        actions_frame.pack(fill=tk.X, pady=5)

        ttk.Button(actions_frame, text="Block Selected User",
                   command=self.admin_block_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Unblock Selected User",
                   command=self.admin_unblock_user).pack(side=tk.LEFT, padx=5)

    # Data loading methods
    def load_freelancers(self):
        """Load and display all freelancers"""
        # Clear existing data
        for item in self.freelancers_tree.get_children():
            self.freelancers_tree.delete(item)

        # Fetch data
        freelancers = self.db.get_all_freelancers()
        if freelancers:
            for freelancer in freelancers:
                user_id, username, headline, rate, rating = freelancer
                # Convert cents to dollars
                rate_dollars = rate / 100 if rate else 0
                self.freelancers_tree.insert("", tk.END,
                                             values=(user_id, username, headline,
                                                     f"${rate_dollars:.2f}", f"{rating:.2f}"))

    def load_projects(self):
        """Load and display all projects"""
        # Clear existing data
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)

        # Fetch data
        projects = self.db.get_all_projects()
        if projects:
            for project in projects:
                proj_id, title, min_budget, max_budget, deadline = project
                # Convert cents to dollars
                min_dollars = min_budget / 100 if min_budget else 0
                max_dollars = max_budget / 100 if max_budget else 0
                self.projects_tree.insert("", tk.END,
                                          values=(proj_id, title,
                                                  f"${min_dollars:.2f}",
                                                  f"${max_dollars:.2f}",
                                                  deadline))

    def load_proposals_by_project(self):
        """Load proposals for a specific project"""
        project_id = self.proposal_project_id.get()

        if not project_id:
            messagebox.showwarning("Input Required", "Please enter a Project ID")
            return

        try:
            project_id = int(project_id)
        except ValueError:
            messagebox.showerror("Invalid Input", "Project ID must be a number")
            return

        # Clear existing data
        for item in self.proposals_tree.get_children():
            self.proposals_tree.delete(item)

        # Fetch data
        proposals = self.db.get_proposals_by_project(project_id)
        if proposals:
            for proposal in proposals:
                username, bid_amount, status, cover_letter = proposal
                bid_dollars = bid_amount / 100 if bid_amount else 0
                self.proposals_tree.insert("", tk.END,
                                           values=(username, f"${bid_dollars:.2f}",
                                                   status, cover_letter))
        else:
            messagebox.showinfo("No Results", f"No proposals found for project ID {project_id}")

    def load_contracts(self):
        """Load and display active contracts"""
        # Clear existing data
        for item in self.contracts_tree.get_children():
            self.contracts_tree.delete(item)

        # Fetch data
        contracts = self.db.get_active_contracts()
        if contracts:
            for contract in contracts:
                contract_id, client_id, freelancer_id, total_amount, status = contract
                amount_dollars = total_amount / 100 if total_amount else 0
                self.contracts_tree.insert("", tk.END,
                                           values=(contract_id, client_id, freelancer_id,
                                                   f"${amount_dollars:.2f}", status))

    def search_by_skill(self):
        """Search freelancers by skill"""
        skill_name = self.search_skill_entry.get().strip()

        if not skill_name:
            messagebox.showwarning("Input Required", "Please enter a skill name")
            return

        # Clear existing data
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        # Fetch data
        results = self.db.search_freelancers_by_skill(skill_name)
        if results:
            for result in results:
                username, skill, proficiency, rating = result
                self.search_tree.insert("", tk.END,
                                        values=(username, skill, proficiency, f"{rating:.2f}"))
        else:
            messagebox.showinfo("No Results", f"No freelancers found with skill: {skill_name}")

    # Detail view methods
    def show_freelancer_details(self, event):
        """Show detailed information for selected freelancer"""
        selection = self.freelancers_tree.selection()
        if not selection:
            return

        item = self.freelancers_tree.item(selection[0])
        user_id = item['values'][0]

        # Get freelancer details
        details = self.db.get_freelancer_details(user_id)
        skills = self.db.get_freelancer_skills(user_id)

        # Clear and update details text
        self.freelancer_details_text.delete(1.0, tk.END)

        if details:
            username, email, headline, bio, rate, rating = details
            rate_dollars = rate / 100 if rate else 0

            details_str = f"Username: {username}\n"
            details_str += f"Email: {email}\n"
            details_str += f"Headline: {headline}\n"
            details_str += f"Bio: {bio}\n"
            details_str += f"Rate per Hour: ${rate_dollars:.2f}\n"
            details_str += f"Average Rating: {rating:.2f}\n\n"
            details_str += "Skills:\n"

            if skills:
                for skill_name, proficiency in skills:
                    details_str += f"  - {skill_name} (Level {proficiency}/5)\n"
            else:
                details_str += "  No skills listed\n"

            self.freelancer_details_text.insert(1.0, details_str)

    def show_project_details(self, event):
        """Show detailed information for selected project"""
        selection = self.projects_tree.selection()
        if not selection:
            return

        item = self.projects_tree.item(selection[0])
        project_id = item['values'][0]

        # Get project details
        details = self.db.get_project_details(project_id)
        skills = self.db.get_project_skills(project_id)

        # Clear and update details text
        self.project_details_text.delete(1.0, tk.END)

        if details:
            proj_id, title, description, min_budget, max_budget, deadline, client = details
            min_dollars = min_budget / 100 if min_budget else 0
            max_dollars = max_budget / 100 if max_budget else 0

            details_str = f"Project ID: {proj_id}\n"
            details_str += f"Title: {title}\n"
            details_str += f"Client: {client}\n"
            details_str += f"Description: {description}\n"
            details_str += f"Budget: ${min_dollars:.2f} - ${max_dollars:.2f}\n"
            details_str += f"Deadline: {deadline}\n\n"
            details_str += "Required Skills:\n"

            if skills:
                for (skill_name,) in skills:
                    details_str += f"  - {skill_name}\n"
            else:
                details_str += "  No specific skills required\n"

            self.project_details_text.insert(1.0, details_str)

    def show_contract_milestones(self, event):
        """Show milestones for selected contract"""
        selection = self.contracts_tree.selection()
        if not selection:
            return

        item = self.contracts_tree.item(selection[0])
        contract_id = item['values'][0]

        # Get milestones
        milestones = self.db.get_contract_milestones(contract_id)

        # Clear and update milestones text
        self.milestones_text.delete(1.0, tk.END)

        details_str = f"Milestones for Contract ID {contract_id}:\n\n"

        if milestones:
            for milestone in milestones:
                milestone_id, title, amount, due_date, status = milestone
                amount_dollars = amount / 100 if amount else 0
                details_str += f"Milestone {milestone_id}: {title}\n"
                details_str += f"  Amount: ${amount_dollars:.2f}\n"
                details_str += f"  Due Date: {due_date}\n"
                details_str += f"  Status: {status}\n\n"
        else:
            details_str += "No milestones found for this contract\n"

        self.milestones_text.insert(1.0, details_str)

    # Utility methods
    def refresh_all_tabs(self):
        """Refresh data in all tabs"""
        self.load_freelancers()
        self.load_projects()
        self.load_contracts()
        messagebox.showinfo("Refresh", "All data refreshed successfully")

    def show_db_settings(self):
        """Show database connection settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Database Settings")
        settings_window.geometry("400x250")

        ttk.Label(settings_window, text="Database Connection Settings",
                  font=("Arial", 12, "bold")).pack(pady=10)

        frame = ttk.Frame(settings_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
        host_entry = ttk.Entry(frame, width=30)
        host_entry.insert(0, self.db.host)
        host_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Database:").grid(row=1, column=0, sticky=tk.W, pady=5)
        db_entry = ttk.Entry(frame, width=30)
        db_entry.insert(0, self.db.database)
        db_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="User:").grid(row=2, column=0, sticky=tk.W, pady=5)
        user_entry = ttk.Entry(frame, width=30)
        user_entry.insert(0, self.db.user)
        user_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        pass_entry = ttk.Entry(frame, width=30, show="*")
        pass_entry.insert(0, self.db.password)
        pass_entry.grid(row=3, column=1, pady=5)

        def save_settings():
            self.db.host = host_entry.get()
            self.db.database = db_entry.get()
            self.db.user = user_entry.get()
            self.db.password = pass_entry.get()
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings saved. Please reconnect to apply changes.")

        ttk.Button(frame, text="Save", command=save_settings).grid(row=4, column=0, columnspan=2, pady=20)

    def reconnect_db(self):
        """Reconnect to database"""
        self.db.disconnect()
        if self.db.connect():
            messagebox.showinfo("Success", "Reconnected to database successfully")
            self.refresh_all_tabs()
        else:
            messagebox.showerror("Error", "Failed to reconnect to database")

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About SkillLink",
                            "SkillLink - Freelancer Marketplace\n\n"
                            "Version 1.0\n\n"
                            "A desktop application for managing freelancer projects,\n"
                            "proposals, contracts, and more.\n\n"
                            "Built with Python, Tkinter, and PostgreSQL")

    # Client Dashboard methods
    def load_client_dashboard(self):
        """Load client's projects and proposals"""
        client_id = self.client_id_entry.get()

        if not client_id:
            messagebox.showwarning("Input Required", "Please enter a Client ID")
            return

        try:
            client_id = int(client_id)
        except ValueError:
            messagebox.showerror("Invalid Input", "Client ID must be a number")
            return

        # Clear existing data
        for item in self.client_projects_tree.get_children():
            self.client_projects_tree.delete(item)

        # Get client's projects
        query = """
        SELECT p.project_id, p.title, p.budget_min_cents, p.budget_max_cents,
               COUNT(pr.proposal_id) as proposal_count
        FROM project p
        LEFT JOIN proposal pr ON p.project_id = pr.project_id
        WHERE p.client_id = %s
        GROUP BY p.project_id, p.title, p.budget_min_cents, p.budget_max_cents
        ORDER BY p.project_id DESC
        """
        projects = self.db.execute_query(query, (client_id,))

        if projects:
            for project in projects:
                proj_id, title, min_budget, max_budget, prop_count = project
                min_dollars = min_budget / 100 if min_budget else 0
                max_dollars = max_budget / 100 if max_budget else 0
                budget_str = f"${min_dollars:.2f} - ${max_dollars:.2f}"

                # Check if project has accepted proposal
                status_query = """
                SELECT COUNT(*) FROM proposal
                WHERE project_id = %s AND status = 'accepted'
                """
                accepted = self.db.execute_query(status_query, (proj_id,))
                status = "In Progress" if accepted and accepted[0][0] > 0 else "Open"

                self.client_projects_tree.insert("", tk.END,
                                                  values=(proj_id, title, budget_str,
                                                          prop_count, status))
            messagebox.showinfo("Success", f"Loaded {len(projects)} projects for Client ID {client_id}")
        else:
            messagebox.showinfo("No Results", f"No projects found for Client ID {client_id}")

    def show_project_proposals_for_client(self, event):
        """Show proposals for selected project"""
        selection = self.client_projects_tree.selection()
        if not selection:
            return

        item = self.client_projects_tree.item(selection[0])
        project_id = item['values'][0]

        # Create new window to show proposals
        proposals_window = tk.Toplevel(self.root)
        proposals_window.title(f"Proposals for Project {project_id}")
        proposals_window.geometry("800x400")

        # Get proposals
        proposals = self.db.get_proposals_by_project(project_id)

        if proposals:
            # Create treeview
            tree_frame = ttk.Frame(proposals_window)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            vsb = ttk.Scrollbar(tree_frame, orient="vertical")
            tree = ttk.Treeview(tree_frame,
                                columns=("Freelancer", "Bid", "Status", "Cover Letter"),
                                show="headings",
                                yscrollcommand=vsb.set)
            vsb.config(command=tree.yview)

            tree.heading("Freelancer", text="Freelancer")
            tree.heading("Bid", text="Bid Amount")
            tree.heading("Status", text="Status")
            tree.heading("Cover Letter", text="Cover Letter")

            tree.column("Freelancer", width=150)
            tree.column("Bid", width=100)
            tree.column("Status", width=100)
            tree.column("Cover Letter", width=400)

            for proposal in proposals:
                username, bid_amount, status, cover_letter = proposal
                bid_dollars = bid_amount / 100 if bid_amount else 0
                tree.insert("", tk.END,
                            values=(username, f"${bid_dollars:.2f}", status, cover_letter))

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            ttk.Label(proposals_window, text="No proposals for this project",
                      font=("Arial", 12)).pack(pady=50)

    # Admin Panel methods
    def load_admin_stats(self):
        """Load platform statistics for admin"""
        self.stats_text.delete(1.0, tk.END)

        # Get various statistics
        stats = []

        # Total users
        total_users = self.db.execute_query("SELECT COUNT(*) FROM users")
        stats.append(f"Total Users: {total_users[0][0] if total_users else 0}")

        # Users by role
        clients = self.db.execute_query("SELECT COUNT(*) FROM users WHERE role = 'client'")
        freelancers = self.db.execute_query("SELECT COUNT(*) FROM users WHERE role = 'freelancer'")
        admins = self.db.execute_query("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        stats.append(f"  - Clients: {clients[0][0] if clients else 0}")
        stats.append(f"  - Freelancers: {freelancers[0][0] if freelancers else 0}")
        stats.append(f"  - Admins: {admins[0][0] if admins else 0}")

        # Total projects
        total_projects = self.db.execute_query("SELECT COUNT(*) FROM project")
        stats.append(f"\nTotal Projects: {total_projects[0][0] if total_projects else 0}")

        # Active contracts
        active_contracts = self.db.execute_query("SELECT COUNT(*) FROM contract WHERE status = 'active'")
        stats.append(f"Active Contracts: {active_contracts[0][0] if active_contracts else 0}")

        # Total payments
        total_payments = self.db.execute_query("SELECT SUM(amount_cents) FROM payment WHERE status = 'released'")
        total_amount = total_payments[0][0] if total_payments and total_payments[0][0] else 0
        stats.append(f"Total Payments Released: ${total_amount / 100:.2f}")

        self.stats_text.insert(1.0, "\n".join(stats))

    def load_admin_users(self):
        """Load users for admin management"""
        # Clear existing data
        for item in self.admin_users_tree.get_children():
            self.admin_users_tree.delete(item)

        # Get role filter
        role_filter = self.admin_role_filter.get()

        if role_filter == "All":
            users = self.db.get_all_users()
        else:
            users = self.db.get_users_by_role(role_filter)

        if users:
            for user in users:
                user_id, username, email, role, status, joined_at = user
                self.admin_users_tree.insert("", tk.END,
                                              values=(user_id, username, email, role, status, joined_at))

    def admin_block_user(self):
        """Block selected user"""
        selection = self.admin_users_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a user to block")
            return

        item = self.admin_users_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]

        if messagebox.askyesno("Confirm Block", f"Block user '{username}' (ID: {user_id})?"):
            query = "UPDATE users SET status = 'blocked' WHERE user_id = %s"
            if self.db.execute_update(query, (user_id,)):
                messagebox.showinfo("Success", f"User '{username}' has been blocked")
                self.load_admin_users()
            else:
                messagebox.showerror("Error", "Failed to block user")

    def admin_unblock_user(self):
        """Unblock selected user"""
        selection = self.admin_users_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select a user to unblock")
            return

        item = self.admin_users_tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]

        if messagebox.askyesno("Confirm Unblock", f"Unblock user '{username}' (ID: {user_id})?"):
            query = "UPDATE users SET status = 'active' WHERE user_id = %s"
            if self.db.execute_update(query, (user_id,)):
                messagebox.showinfo("Success", f"User '{username}' has been unblocked")
                self.load_admin_users()
            else:
                messagebox.showerror("Error", "Failed to unblock user")

    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit SkillLink?"):
            self.db.disconnect()
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SkillLinkApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
