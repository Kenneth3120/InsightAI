import csv
import random

# Define post types
post_types = ["carousel", "reel", "static_image"]

# Number of entries
num_entries = 150

# File name
file_name = "mock_social_data.csv"

# Generate random data
data = []
for post_id in range(1, num_entries + 1):
    post_type = random.choice(post_types)
    likes = random.randint(50, 500)  # Random likes between 50 and 500
    shares = random.randint(5, 100)  # Random shares between 5 and 100
    comments = random.randint(2, 50)  # Random comments between 2 and 50
    data.append({"post_id": post_id, "post_type": post_type, "likes": likes, "shares": shares, "comments": comments})

# Write the dataset to a CSV file
with open(file_name, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["post_id", "post_type", "likes", "shares", "comments"])
    writer.writeheader()
    writer.writerows(data)

print(f"Random dataset with {num_entries} entries has been written to {file_name}")
