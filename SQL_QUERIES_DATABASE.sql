--Table creation

CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('client', 'freelancer', 'admin')) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE freelancer_profile (
    profile_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    headline VARCHAR(255),
    bio VARCHAR(700),
    rate_per_hour INTEGER,
    avg_rating DECIMAL(3,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


CREATE TABLE skill (
    skill_id BIGSERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    skill_description TEXT
);

CREATE TABLE freelancer_skill (
    profile_id BIGINT,
    skill_id BIGINT,
    proficiency_level SMALLINT CHECK (proficiency_level BETWEEN 1 AND 5),
    PRIMARY KEY (profile_id, skill_id),
    FOREIGN KEY (profile_id) REFERENCES freelancer_profile(profile_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id) ON DELETE CASCADE
);

CREATE TABLE project (
    project_id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    budget_min_cents INTEGER NOT NULL,
    budget_max_cents INTEGER NOT NULL,
    price_model VARCHAR(20),
    deadline DATE,
    FOREIGN KEY (client_id) REFERENCES users(user_id)
);

CREATE TABLE project_skill (
    project_id BIGINT,
    skill_id BIGINT,
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES project(project_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id) ON DELETE CASCADE
);
CREATE TABLE proposal (
    proposal_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL,
    freelancer_id BIGINT NOT NULL,
    bid_amount_cents INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    cover_letter TEXT,
    FOREIGN KEY (project_id) REFERENCES project(project_id),
    FOREIGN KEY (freelancer_id) REFERENCES users(user_id),
    UNIQUE (project_id, freelancer_id)
);
CREATE TABLE contract (
    contract_id BIGSERIAL PRIMARY KEY,
    proposal_id BIGINT UNIQUE NOT NULL,
    client_id BIGINT NOT NULL,
    freelancer_id BIGINT NOT NULL,
    total_amount_cents INTEGER,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (proposal_id) REFERENCES proposal(proposal_id),
    FOREIGN KEY (client_id) REFERENCES users(user_id),
    FOREIGN KEY (freelancer_id) REFERENCES users(user_id)
);
CREATE TABLE milestone (
    milestone_id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    title VARCHAR(255),
    amount_cents INTEGER NOT NULL,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (contract_id) REFERENCES contract(contract_id) ON DELETE CASCADE
);
CREATE TABLE payment (
    payment_id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    milestone_id BIGINT,
    payer_id BIGINT NOT NULL,
    payee_id BIGINT NOT NULL,
    amount_cents INTEGER NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (contract_id) REFERENCES contract(contract_id),
    FOREIGN KEY (milestone_id) REFERENCES milestone(milestone_id),
    FOREIGN KEY (payer_id) REFERENCES users(user_id),
    FOREIGN KEY (payee_id) REFERENCES users(user_id)
);
CREATE TABLE review (
    review_id BIGSERIAL PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    reviewer_id BIGINT NOT NULL,
    reviewee_id BIGINT NOT NULL,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    UNIQUE (contract_id, reviewer_id),
    FOREIGN KEY (contract_id) REFERENCES contract(contract_id),
    FOREIGN KEY (reviewer_id) REFERENCES users(user_id),
    FOREIGN KEY (reviewee_id) REFERENCES users(user_id)
);

-- Table Population
-- made a mistake in population, so I'm deleting all data and started over again:
TRUNCATE TABLE
review,
payment,
milestone,
contract,
proposal,
project_skill,
project,
freelancer_skill,
skill,
freelancer_profile,
users
RESTART IDENTITY CASCADE;

INSERT INTO users (user_id, username, email, password_hash, role, status)
VALUES
(1,'client1','client1@mail.com','hash1','client','active'),
(2,'client2','client2@mail.com','hash2','client','active'),
(3,'client3','client3@mail.com','hash3','client','active'),
(4,'admin1','admin@mail.com','hash4','admin','active'),
(5,'freelancer1','free1@mail.com','hash5','freelancer','active'),
(6,'freelancer2','free2@mail.com','hash6','freelancer','active'),
(7,'freelancer3','free3@mail.com','hash7','freelancer','active'),
(8,'freelancer4','free4@mail.com','hash8','freelancer','active'),
(9,'freelancer5','free5@mail.com','hash9','freelancer','active'),
(10,'freelancer6','free6@mail.com','hash10','freelancer','active'),
(11,'freelancer7','free7@mail.com','hash11','freelancer','active'),
(12,'freelancer8','free8@mail.com','hash12','freelancer','active');

INSERT INTO freelancer_profile (profile_id, user_id, headline, bio, rate_per_hour, avg_rating)
VALUES
(1,5,'Backend Developer','APIs and Databases',220,4.5),
(2,6,'Frontend Developer','React specialist',200,4.2),
(3,7,'Data Analyst','BI and dashboards',180,4.6),
(4,8,'UI/UX Designer','User-centered design',160,4.3),
(5,9,'Mobile Developer','Flutter & Android',210,4.1),
(6,10,'DevOps Engineer','Cloud and CI/CD',230,4.7),
(7,11,'ML Engineer','Machine learning models',250,4.8),
(8,12,'QA Engineer','Automated testing',150,4.0);

INSERT INTO skill (skill_id, skill_name, skill_description)
VALUES
(1,'Python','Programming language'),
(2,'SQL','Relational databases'),
(3,'Java','Object-oriented programming'),
(4,'React','Frontend framework'),
(5,'Django','Python web framework'),
(6,'Figma','UI/UX design tool'),
(7,'Flutter','Mobile framework'),
(8,'Docker','Containerization'),
(9,'AWS','Cloud services'),
(10,'Testing','Software testing');

INSERT INTO freelancer_skill (profile_id, skill_id, proficiency_level)
VALUES
(1,1,5),
(1,2,5),
(1,8,4),

(2,4,5),
(2,2,4),

(3,1,5),
(3,2,5),

(4,6,5),
(4,4,3),

(5,7,5),
(5,1,3),

(6,8,5),
(6,9,4),

(7,1,5),
(7,5,5);

INSERT INTO project (project_id, client_id, title, description, budget_min_cents, budget_max_cents, price_model, deadline)
VALUES
(1,1,'Web Platform','Full-stack web platform',50000,120000,'fixed','2025-08-01'),
(2,1,'API Development','REST API services',60000,100000,'fixed','2025-07-15'),
(3,2,'Mobile App','Cross-platform app',70000,140000,'fixed','2025-09-01'),
(4,2,'Dashboard','Analytics dashboard',40000,90000,'fixed','2025-06-30'),
(5,3,'UI Redesign','Website redesign',30000,60000,'fixed','2025-07-20'),
(6,3,'Cloud Migration','Move infra to cloud',80000,150000,'fixed','2025-09-15'),
(7,1,'ML Model','Prediction system',90000,180000,'fixed','2025-10-01'),
(8,2,'Testing Suite','Automated tests',35000,70000,'fixed','2025-06-25'),
(9,3,'E-commerce App','Online store',100000,200000,'fixed','2025-11-01'),
(10,1,'DevOps Pipeline','CI/CD setup',60000,110000,'fixed','2025-08-10');

INSERT INTO project_skill (project_id, skill_id)
VALUES
(1,1),(1,2),(1,4),
(2,1),(2,5),
(3,7),(3,1),
(4,2),
(5,6),
(6,9),(6,8),
(7,1),(7,5),
(8,10),
(10,8);

INSERT INTO proposal (proposal_id, project_id, freelancer_id, bid_amount_cents, status, cover_letter)
VALUES
(1,1,5,110000,'pending','Experienced backend dev'),
(2,1,6,105000,'pending','Strong frontend skills'),
(3,2,5,90000,'accepted','API specialist'),
(4,3,9,130000,'pending','Mobile expert'),
(5,4,7,85000,'pending','Data analyst'),
(6,5,8,55000,'pending','UI designer'),
(7,6,10,140000,'pending','Cloud expert'),
(8,7,11,170000,'pending','ML engineer'),
(9,8,12,60000,'pending','QA automation'),
(10,9,6,180000,'pending','E-commerce experience'),
(11,10,10,100000,'pending','DevOps pipeline');

INSERT INTO contract (contract_id, proposal_id, client_id, freelancer_id, total_amount_cents, status)
VALUES
(1,3,1,5,90000,'completed'),
(2,4,2,9,130000,'active'),
(3,6,3,8,55000,'active'),
(4,7,3,10,140000,'active'),
(5,8,1,11,170000,'active');

INSERT INTO milestone (milestone_id, contract_id, title, amount_cents, due_date, status)
VALUES
(1,1,'Design',30000,'2025-05-01','completed'),
(2,1,'Implementation',60000,'2025-06-01','completed'),

(3,2,'Phase 1',60000,'2025-07-01','completed'),
(4,2,'Phase 2',70000,'2025-08-01','pending'),

(5,3,'UI Draft',25000,'2025-06-15','completed'),
(6,3,'Final UI',30000,'2025-07-01','pending'),

(7,4,'Setup',70000,'2025-07-20','pending'),
(8,4,'Deployment',70000,'2025-08-20','pending'),

(9,5,'Model Training',90000,'2025-08-15','pending'),
(10,5,'Evaluation',80000,'2025-09-15','pending');

INSERT INTO payment (payment_id, contract_id, milestone_id, payer_id, payee_id, amount_cents, status)
VALUES
(1,1,1,1,5,30000,'released'),
(2,1,2,1,5,60000,'released'),
(3,2,3,2,9,60000,'released'),
(4,3,5,3,8,25000,'released'),
(5,3,6,3,8,30000,'escrowed'),
(6,4,7,3,10,70000,'escrowed'),
(7,5,9,1,11,90000,'escrowed'),
(8,2,4,2,9,70000,'escrowed');

INSERT INTO review (review_id, contract_id, reviewer_id, reviewee_id, rating, feedback)
VALUES
(1,1,1,5,5,'Excellent backend work'),
(2,1,5,1,5,'Great client'),
(3,1,2,9,4,'Good communication'),
(4,1,9,2,4,'Smooth project');




--Update queries:
-- In oredr to update the proposal status, we can use:
UPDATE proposal
SET status = 'accepted'
WHERE proposal_id = 2;

-- In oredr to Update freelancer hourly rate
UPDATE freelancer_profile
SET rate_per_hour = 250
WHERE profile_id = 2;

--DELETE Queries
-- to Remove inactive proposal
DELETE FROM proposal
WHERE status = 'rejected';

--to Delete project (cascade found in triggers deletes skills & proposals)
-- !!!! after trying to run this query, the DBMS successfully returns an error because it is a foreign key in proposals
DELETE FROM project
WHERE project_id = 2;


--Functions:
--To calculate the avg rating:
CREATE OR REPLACE FUNCTION get_freelancer_avg_rating(fid BIGINT)
RETURNS DECIMAL AS $$
BEGIN
    RETURN (
        SELECT COALESCE(AVG(rating),0)
        FROM review
        WHERE reviewee_id = fid
    );
END;
$$ LANGUAGE plpgsql;


-- to Count Freelancer Proposals
CREATE OR REPLACE FUNCTION count_freelancer_proposals(fid BIGINT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM proposal
        WHERE freelancer_id = fid
    );
END;
$$ LANGUAGE plpgsql;

-- to compute the Total Contract Value

CREATE OR REPLACE FUNCTION get_contract_total(cid BIGINT)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT SUM(amount_cents)
        FROM milestone
        WHERE contract_id = cid
    );
END;
$$ LANGUAGE plpgsql;


--Procedures:
-- to Accept Proposal & Create Contract
CREATE OR REPLACE PROCEDURE accept_proposal(p_proposal_id BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE proposal
    SET status = 'accepted'
    WHERE proposal_id = p_proposal_id;

    INSERT INTO contract (proposal_id, client_id, freelancer_id, status)
    SELECT proposal_id, p.client_id, p.freelancer_id, 'active'
    FROM proposal p
    JOIN project pr ON p.project_id = pr.project_id
    WHERE proposal_id = p_proposal_id;
END;
$$;

-- to Complete Milestone & Release Payment
CREATE OR REPLACE PROCEDURE release_payment(m_id BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE milestone
    SET status = 'completed'
    WHERE milestone_id = m_id;

    INSERT INTO payment (contract_id, milestone_id, payer_id, payee_id, amount_cents, status)
    SELECT contract_id, milestone_id, c.client_id, c.freelancer_id, amount_cents, 'released'
    FROM milestone m
    JOIN contract c ON m.contract_id = c.contract_id
    WHERE milestone_id = m_id;
END;
$$;

--to Block User (Admin)
CREATE OR REPLACE PROCEDURE block_user(uid BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET status = 'blocked'
    WHERE user_id = uid;
END;
$$;

--triggers:
--to implement that only freelancers can submit proposals
CREATE OR REPLACE FUNCTION check_proposal_role()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE user_id = NEW.freelancer_id) <> 'freelancer' THEN
        RAISE EXCEPTION 'Only freelancers can submit proposals';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_proposal_role
BEFORE INSERT ON proposal
FOR EACH ROW
EXECUTE FUNCTION check_proposal_role();


--to implement the fact that Contract Must Have At Least One Milestone
CREATE OR REPLACE FUNCTION check_milestones_before_completion()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' THEN
        IF NOT EXISTS (
            SELECT 1 FROM milestone
            WHERE contract_id = NEW.contract_id
        ) THEN
            RAISE EXCEPTION 'Cannot complete contract without milestones';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_milestones_on_complete
BEFORE UPDATE ON contract
FOR EACH ROW
EXECUTE FUNCTION check_milestones_before_completion();

--to Auto-Update Freelancer Avg Rating
CREATE OR REPLACE FUNCTION update_avg_rating()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE freelancer_profile
    SET avg_rating = get_freelancer_avg_rating(NEW.reviewee_id)
    WHERE user_id = NEW.reviewee_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_rating
AFTER INSERT ON review
FOR EACH ROW
EXECUTE FUNCTION update_avg_rating();


--Implementing functional requirements

--User Login (credential validation)
SELECT user_id, role, status
FROM users
WHERE username = 'freelancer1'
  AND password_hash = 'hash5'
  AND status = 'active';
--list all active users
SELECT user_id, username, role, status
FROM users
WHERE status = 'active';

--Check if a username/email is already taken
SELECT COUNT(*) AS count
FROM users
WHERE username = 'freelancer1' OR email = 'freelancer1@mail.com';

--Retrieve all admins and their email
SELECT username, email
FROM users
WHERE role = 'admin';

--List all freelancer profiles with average rating
SELECT u.username, f.headline, f.rate_per_hour, f.avg_rating
FROM freelancer_profile f
JOIN users u ON f.user_id = u.user_id;

--Find freelancers with a specific skill
SELECT u.username, s.skill_name, fs.proficiency_level
FROM freelancer_skill fs JOIN freelancer_profile f ON fs.profile_id = f.profile_id JOIN users u ON f.user_id = u.user_id JOIN skill s ON fs.skill_id = s.skill_id
WHERE s.skill_name = 'Python';


--Freelancers with proficiency ≥ 4 in SQL
SELECT u.username, s.skill_name
FROM freelancer_skill fs JOIN freelancer_profile f ON fs.profile_id = f.profile_id JOIN users u ON f.user_id = u.user_id JOIN skill s ON fs.skill_id = s.skill_id
WHERE fs.proficiency_level >= 4 AND s.skill_name = 'SQL';

--List all active projects
SELECT project_id, title, budget_min_cents, budget_max_cents, deadline
FROM project;


--Projects within a specific budget range
SELECT title, budget_min_cents, budget_max_cents
FROM project
WHERE budget_min_cents >= 50000 AND budget_max_cents <= 120000;

--Projects requiring a specific skill
SELECT p.title, s.skill_name
FROM project p
JOIN project_skill ps ON p.project_id = ps.project_id
JOIN skill s ON ps.skill_id = s.skill_id
WHERE s.skill_name = 'Django';

--Projects posted by a specific client
SELECT title, budget_min_cents, budget_max_cents
FROM project
WHERE client_id = 1;

--List all proposals for a project
SELECT u.username AS freelancer, pr.bid_amount_cents, pr.status
FROM proposal pr
JOIN users u ON pr.freelancer_id = u.user_id
WHERE pr.project_id = 1;


--List all proposals by a freelancer
SELECT p.title, pr.bid_amount_cents, pr.status
FROM proposal pr JOIN project p ON pr.project_id = p.project_id
WHERE pr.freelancer_id = 5;

--Accepted proposals only
SELECT p.title, u.username, pr.bid_amount_cents
FROM proposal pr JOIN project p ON pr.project_id = p.project_id JOIN users u ON pr.freelancer_id = u.user_id
WHERE pr.status = 'accepted';


--Count proposals per project
SELECT project_id, COUNT(*) AS proposal_count
FROM proposal
GROUP BY project_id;

--List active contracts
SELECT contract_id, client_id, freelancer_id, total_amount_cents, status
FROM contract
WHERE status = 'active';


--Calculate total contract value
SELECT contract_id, SUM(amount_cents) AS total_value
FROM milestone
GROUP BY contract_id;

--Total earnings per freelancer
SELECT payee_id, SUM(amount_cents) AS total_earned
FROM payment
GROUP BY payee_id;

--Average rating per freelancer
SELECT reviewee_id, AVG(rating) AS avg_rating
FROM review
GROUP BY reviewee_id;


--Blocked users (not yet implemented)
SELECT username, role
FROM users
WHERE status = 'blocked';


--Projects marked as disabled (not yet implemented)
SELECT title, client_id
FROM project
WHERE title LIKE '%(Disabled)%';

--Freelancers with avg_rating < 4
SELECT f.profile_id, u.username, f.avg_rating
FROM freelancer_profile f JOIN users u ON f.user_id = u.user_id
WHERE f.avg_rating < 4;


--Average bid per project
SELECT project_id, AVG(bid_amount_cents) AS avg_bid
FROM proposal
GROUP BY project_id;

--Views

--Display freelancer listings in the platform
CREATE OR REPLACE VIEW freelancer_public_view AS
SELECT 
    u.user_id,
    u.username,
    f.headline,
    f.rate_per_hour,
    f.avg_rating
FROM users u
JOIN freelancer_profile f ON u.user_id = f.user_id
WHERE u.role = 'freelancer';



--to Help freelancers see projects with all required skills in one row
CREATE OR REPLACE VIEW project_skills_view AS
SELECT 
    p.project_id,
    p.title,
    p.description,
    p.budget_min_cents,
    p.budget_max_cents,
    STRING_AGG(s.skill_name, ', ') AS required_skills
FROM project p
JOIN project_skill ps ON p.project_id = ps.project_id
JOIN skill s ON ps.skill_id = s.skill_id
GROUP BY p.project_id, p.title, p.description, p.budget_min_cents, p.budget_max_cents;

--to Show progress of each contract
CREATE OR REPLACE VIEW contract_milestone_status AS
SELECT 
    c.contract_id,
    c.client_id,
    c.freelancer_id,
    c.total_amount_cents,
    c.status AS contract_status,
    SUM(CASE WHEN m.status='completed' THEN 1 ELSE 0 END) AS milestones_completed,
    SUM(CASE WHEN m.status='pending' THEN 1 ELSE 0 END) AS milestones_pending
FROM contract c
LEFT JOIN milestone m ON c.contract_id = m.contract_id
GROUP BY c.contract_id, c.client_id, c.freelancer_id, c.total_amount_cents, c.status;

--to Show freelancers’ accumulated earnings
CREATE OR REPLACE VIEW freelancer_earnings AS
SELECT 
    u.user_id,
    u.username,
    SUM(p.amount_cents) AS total_earned
FROM users u
JOIN payment p ON u.user_id = p.payee_id
WHERE u.role = 'freelancer'
GROUP BY u.user_id, u.username;








