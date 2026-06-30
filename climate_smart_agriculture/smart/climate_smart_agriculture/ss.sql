CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    experience VARCHAR(100),
    job_type VARCHAR(100),
    description TEXT,
    salary DECIMAL(10, 2),
    skills TEXT
);
INSERT INTO jobs (title, company, location, experience, job_type, description, salary, skills) VALUES
('Software Developer', 'TechCorp', 'Chennai', '2-4 years', 'Full-time', 'Responsible for developing software applications.', 60000.00, 'Python, Java, SQL'),
('Data Scientist', 'DataWorks', 'Bangalore', '3-5 years', 'Full-time', 'Analyze large datasets and build predictive models.', 80000.00, 'Python, R, Machine Learning'),
('Project Manager', 'WebSolutions', 'Hyderabad', '5-7 years', 'Full-time', 'Manage project teams and oversee project execution.', 90000.00, 'Agile, Scrum, Leadership'),
('HR Manager', 'PeopleFirst', 'Mumbai', '4-6 years', 'Full-time', 'Oversee recruitment, training, and employee management.', 70000.00, 'Recruitment, HR Policies, Communication'),
('UI/UX Designer', 'CreativeLabs', 'Delhi', '2-4 years', 'Full-time', 'Design and improve the user experience of web applications.', 50000.00, 'Figma, Adobe XD, HTML, CSS'),
('Network Engineer', 'TechNetwork', 'Kolkata', '3-5 years', 'Full-time', 'Manage and maintain networking systems.', 55000.00, 'Networking, Cisco, Troubleshooting'),
('Marketing Specialist', 'BizGrowth', 'Pune', '1-3 years', 'Full-time', 'Develop and implement marketing strategies.', 45000.00, 'SEO, Social Media, Content Writing'),
('Business Analyst', 'FinSolutions', 'Chennai', '4-6 years', 'Full-time', 'Analyze business processes and provide solutions.', 75000.00, 'Business Analysis, MS Excel, SQL'),
('Web Developer', 'Innovative IT', 'Coimbatore', '2-4 years', 'Full-time', 'Develop and maintain web applications.', 60000.00, 'HTML, CSS, JavaScript, PHP'),
('Graphic Designer', 'VisualArts', 'Bangalore', '1-3 years', 'Full-time', 'Create visual concepts and designs for digital media.', 40000.00, 'Photoshop, Illustrator, Graphic Design'),
('SEO Specialist', 'DigitalExperts', 'Mumbai', '3-5 years', 'Full-time', 'Optimize website content to rank higher on search engines.', 50000.00, 'SEO, Google Analytics, Content Writing'),
('Accountant', 'FinPro', 'Delhi', '5-7 years', 'Full-time', 'Handle financial transactions and reports for the company.', 65000.00, 'Tally, Accounting, Excel'),
('Software Tester', 'QualityTech', 'Chennai', '2-4 years', 'Full-time', 'Test and debug software applications.', 55000.00, 'Testing, Java, Automation'),
('Content Writer', 'ContentHub', 'Hyderabad', '1-3 years', 'Full-time', 'Write engaging and informative content for various platforms.', 35000.00, 'Content Writing, SEO, Copywriting'),
('Product Manager', 'TechGlobal', 'Bangalore', '5-7 years', 'Full-time', 'Lead product development and manage product lifecycle.', 95000.00, 'Product Management, Agile, Leadership');
