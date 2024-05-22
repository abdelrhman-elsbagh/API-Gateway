import docker

# Docker client
client = docker.from_env()

# Account details (read from API, file, etc.)
accounts = [
    {"phone": "1234567890", "password": "password123", "country": "USA"},
    {"phone": "0987654321", "password": "pass456", "country": "UK"},
    # Add more accounts as needed
]

# Launch a Docker container for each account
for account in accounts:
    # Create and start a Docker container
    container = client.containers.run(
        "your-image-name",  # Docker image name
        ["python", "app.py", account["phone"], account["password"], account["country"]],
        detach=True
    )
    print(f"Container for {account['phone']} started: {container.id}")
