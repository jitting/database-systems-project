"""
Database connection module for SkillLink application
Handles all PostgreSQL database operations using psycopg2
"""

import psycopg2
from psycopg2 import sql, Error
from typing import List, Tuple, Optional, Any


class DatabaseConnection:
    """Manages database connection and operations for SkillLink"""

    def __init__(self, host="localhost", database="skilllink", user="postgres", password=""):
        """Initialize database connection parameters"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple]]:
        """Execute a SELECT query and return results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_update(self, query: str, params: Optional[Tuple] = None) -> bool:
        """Execute INSERT, UPDATE, or DELETE query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing update: {e}")
            self.connection.rollback()
            return False

    # User queries
    def get_all_users(self) -> Optional[List[Tuple]]:
        """Retrieve all users"""
        query = "SELECT user_id, username, email, role, status, joined_at FROM users ORDER BY user_id"
        return self.execute_query(query)

    def get_users_by_role(self, role: str) -> Optional[List[Tuple]]:
        """Get users by specific role"""
        query = "SELECT user_id, username, email, role, status FROM users WHERE role = %s"
        return self.execute_query(query, (role,))

    def login_user(self, username: str, password_hash: str) -> Optional[Tuple]:
        """Validate user credentials"""
        query = """
        SELECT user_id, role, status
        FROM users
        WHERE username = %s AND password_hash = %s AND status = 'active'
        """
        result = self.execute_query(query, (username, password_hash))
        return result[0] if result else None

    # Freelancer queries
    def get_all_freelancers(self) -> Optional[List[Tuple]]:
        """Get all freelancer profiles with user info"""
        query = """
        SELECT u.user_id, u.username, f.headline, f.rate_per_hour, f.avg_rating
        FROM freelancer_profile f
        JOIN users u ON f.user_id = u.user_id
        ORDER BY f.avg_rating DESC
        """
        return self.execute_query(query)

    def get_freelancer_details(self, user_id: int) -> Optional[Tuple]:
        """Get detailed freelancer profile"""
        query = """
        SELECT u.username, u.email, f.headline, f.bio, f.rate_per_hour, f.avg_rating
        FROM freelancer_profile f
        JOIN users u ON f.user_id = u.user_id
        WHERE u.user_id = %s
        """
        result = self.execute_query(query, (user_id,))
        return result[0] if result else None

    def get_freelancer_skills(self, user_id: int) -> Optional[List[Tuple]]:
        """Get skills for a specific freelancer"""
        query = """
        SELECT s.skill_name, fs.proficiency_level
        FROM freelancer_skill fs
        JOIN freelancer_profile f ON fs.profile_id = f.profile_id
        JOIN skill s ON fs.skill_id = s.skill_id
        WHERE f.user_id = %s
        ORDER BY fs.proficiency_level DESC
        """
        return self.execute_query(query, (user_id,))

    # Project queries
    def get_all_projects(self) -> Optional[List[Tuple]]:
        """Get all projects"""
        query = """
        SELECT project_id, title, budget_min_cents, budget_max_cents, deadline
        FROM project
        ORDER BY deadline
        """
        return self.execute_query(query)

    def get_project_details(self, project_id: int) -> Optional[Tuple]:
        """Get detailed project information"""
        query = """
        SELECT p.project_id, p.title, p.description, p.budget_min_cents,
               p.budget_max_cents, p.deadline, u.username as client_name
        FROM project p
        JOIN users u ON p.client_id = u.user_id
        WHERE p.project_id = %s
        """
        result = self.execute_query(query, (project_id,))
        return result[0] if result else None

    def get_project_skills(self, project_id: int) -> Optional[List[Tuple]]:
        """Get required skills for a project"""
        query = """
        SELECT s.skill_name
        FROM project_skill ps
        JOIN skill s ON ps.skill_id = s.skill_id
        WHERE ps.project_id = %s
        """
        return self.execute_query(query, (project_id,))

    # Proposal queries
    def get_proposals_by_project(self, project_id: int) -> Optional[List[Tuple]]:
        """Get all proposals for a project"""
        query = """
        SELECT u.username, pr.bid_amount_cents, pr.status, pr.cover_letter
        FROM proposal pr
        JOIN users u ON pr.freelancer_id = u.user_id
        WHERE pr.project_id = %s
        ORDER BY pr.bid_amount_cents
        """
        return self.execute_query(query, (project_id,))

    def get_proposals_by_freelancer(self, freelancer_id: int) -> Optional[List[Tuple]]:
        """Get all proposals by a freelancer"""
        query = """
        SELECT p.title, pr.bid_amount_cents, pr.status
        FROM proposal pr
        JOIN project p ON pr.project_id = p.project_id
        WHERE pr.freelancer_id = %s
        ORDER BY pr.proposal_id DESC
        """
        return self.execute_query(query, (freelancer_id,))

    # Contract queries
    def get_active_contracts(self) -> Optional[List[Tuple]]:
        """Get all active contracts"""
        query = """
        SELECT c.contract_id, c.client_id, c.freelancer_id,
               c.total_amount_cents, c.status
        FROM contract c
        WHERE c.status = 'active'
        """
        return self.execute_query(query)

    def get_contract_milestones(self, contract_id: int) -> Optional[List[Tuple]]:
        """Get milestones for a specific contract"""
        query = """
        SELECT milestone_id, title, amount_cents, due_date, status
        FROM milestone
        WHERE contract_id = %s
        ORDER BY due_date
        """
        return self.execute_query(query, (contract_id,))

    # Payment queries
    def get_freelancer_earnings(self, freelancer_id: int) -> Optional[Tuple]:
        """Get total earnings for a freelancer"""
        query = """
        SELECT SUM(amount_cents) as total_earned
        FROM payment
        WHERE payee_id = %s AND status = 'released'
        """
        result = self.execute_query(query, (freelancer_id,))
        return result[0] if result else None

    # Review queries
    def get_freelancer_reviews(self, freelancer_id: int) -> Optional[List[Tuple]]:
        """Get all reviews for a freelancer"""
        query = """
        SELECT r.rating, r.feedback, u.username as reviewer
        FROM review r
        JOIN users u ON r.reviewer_id = u.user_id
        WHERE r.reviewee_id = %s
        ORDER BY r.review_id DESC
        """
        return self.execute_query(query, (freelancer_id,))

    # Skill queries
    def get_all_skills(self) -> Optional[List[Tuple]]:
        """Get all available skills"""
        query = "SELECT skill_id, skill_name, skill_description FROM skill ORDER BY skill_name"
        return self.execute_query(query)

    # Search queries
    def search_freelancers_by_skill(self, skill_name: str) -> Optional[List[Tuple]]:
        """Find freelancers with a specific skill"""
        query = """
        SELECT u.username, s.skill_name, fs.proficiency_level, f.avg_rating
        FROM freelancer_skill fs
        JOIN freelancer_profile f ON fs.profile_id = f.profile_id
        JOIN users u ON f.user_id = u.user_id
        JOIN skill s ON fs.skill_id = s.skill_id
        WHERE s.skill_name = %s
        ORDER BY fs.proficiency_level DESC, f.avg_rating DESC
        """
        return self.execute_query(query, (skill_name,))
