CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL,
    UpdatedAt DATETIME
);

CREATE TABLE Projects (
    ProjectID UUID PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    TopicTitle VARCHAR(255),
    TopicDescription TEXT
);

CREATE TABLE LLMs (
    LLMID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID UUID,
    Name VARCHAR(255) NOT NULL,
    URL VARCHAR(255),
    APIKey VARCHAR(255),
    DefaultTemperature FLOAT,
    DefaultMaxTokens INT,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

CREATE TABLE LLMHyperparams (
    HyperparamID INT AUTO_INCREMENT PRIMARY KEY,
    LLMID INT,
    Key VARCHAR(255) NOT NULL,
    Value VARCHAR(255) NOT NULL,
    FOREIGN KEY (LLMID) REFERENCES LLMs(LLMID)
);

CREATE TABLE Datasets (
    DatasetID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID UUID,
    Name VARCHAR(255) NOT NULL,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

CREATE TABLE Configurations (
    ConfigurationID INT AUTO_INCREMENT PRIMARY KEY,
    ProjectID UUID,
    Features TEXT,
    Linient BOOLEAN,
    PositiveShots INT,
    NegativeShots INT,
    SelectionInclusionCondition VARCHAR(255),
    SelectionExclusionCondition VARCHAR(255),
    OutputClasses INT,
    OutputReason BOOLEAN,
    OutputConfidence BOOLEAN,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);