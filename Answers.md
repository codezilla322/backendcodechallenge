# Implementation and Conceptual Questions

## 1. How were you debugging this mini-project? Which tools?

### **Tools and Techniques Used:**

1. **Flask Debug Mode**
   - Enabled with `FLASK_ENV=development` for auto-reload and detailed tracebacks.

2. **Logging**
   - Used Python’s `print()` statements for:
     - GitHub API calls
     - Data transformation
     - DB operations

3. **Postman**
   - Tested API endpoints manually:
     ```bash
     GET /api/github/fetch_commits
     GET /api/github/commits?author=livia@cirno.name
     ```

4. **MySQL Client**
   - Verified data and schema using MySQL Workbench

5. **Unit Testing**
   - Used `pytest` to test logic like API fetches.

---

## 2. Please give a detailed answer on your approach to test this mini-project.

### **Testing Strategy:**

#### Unit Tests
- `fetch_github_commits()` - Tested core functions working:
  - ensures GitHub commits are pushed to MySQL database correctly.
  - ensures Database commits are in correct format.

#### Manual Testing
- Used browser/Postman to visually inspect output and debug views.

---

## 3. Imagine this mini-project needs microservices with one single database; how would you draft an architecture?

### **Microservice Architecture Overview:**

```
                +-------------------+
                |    API Gateway    |
                +----------+--------+
                           |
         +-----------------+-----------------+
         |                                   |
+-----------------------+            +-----------------------+
| Commit Ingestor       |            | Commit Viewer Service |
| (GitHub/Bitbucket...) |            |                       |
+--------+--------------+            +-----------+-----------+
         |                                    |
         +------------+-----------------------+
                      |
             +--------v--------+
             |   Shared DB     |
             | (MySQL/Postgres)|
             +-----------------+
```

### **Components:**
- **Commit Ingestor Service**: Fetches and stores commits (GitHub, GitLab, Bitbucket, etc.)
- **Viewer Service**: Queries DB and formats results by author
- **Shared DB**: Centralized storage for commit metadata

---

## 4. How would your solution differ if instead of saving to a Database, you had to call another external API to store and receive the commits?

### **Differences in Architecture**

If the number of commits becomes too large to push synchronously, the system should be asynchronous using a message broker like **Kafka**, **RabbitMQ**, **AWS SQS**, or **Redis Queue (RQ)**: