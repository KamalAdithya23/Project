import subprocess
def handle_task_A2():
    """Formats /data/format.md using Prettier 3.4.2."""
    file_path = "/data/format.md"

    npm_path = shutil.which("npm")
    if not npm_path:
        raise FileNotFoundError("npm is not installed. Please install Node.js.")

    try:
        subprocess.run(["npm", "install", "-g", "prettier@3.4.2"], check=True)
        subprocess.run(["prettier", "--write", str(file_path)], check=True)
    except FileNotFoundError:
        subprocess.run(["npx", "prettier", "--write", str(file_path)], check=True)

    print(f"✅ Task A2 completed: Formatted {file_path}")

### 📆 Task A3: Count Wednesdays in `/data/dates.txt`
def handle_task_A3():
    """Counts the number of Wednesdays in /data/dates.txt and saves the count."""
    input_path = DATA_DIR / "dates.txt"
    output_path = DATA_DIR / "dates-wednesdays.txt"

    with open(input_path, "r") as f:
        dates = [line.strip() for line in f if line.strip()]

    count = sum(1 for date in dates if datetime.strptime(date, "%Y-%m-%d").weekday() == 2)

    with open(output_path, "w") as f:
        f.write(str(count))

    print(f"✅ Task A3 completed: {count} Wednesdays found.")

### 📝 Task A4: Sort `/data/contacts.json` by last_name, then first_name
def handle_task_A4():
    """Sorts contacts.json by last_name, then first_name and saves it."""
    input_path = DATA_DIR / "contacts.json"
    output_path = DATA_DIR / "contacts-sorted.json"

    with open(input_path, "r") as f:
        contacts = json.load(f)

    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))

    with open(output_path, "w") as f:
        json.dump(contacts, f, indent=4)

    print(f"✅ Task A4 completed: Contacts sorted.")

### 📝 Task A5: Extract the first line of the 10 most recent `.log` files
def handle_task_A5():
    """Extracts the first line of the 10 most recent `.log` files and writes them."""
    log_dir = DATA_DIR / "logs"
    output_path = DATA_DIR / "logs-recent.txt"

    log_files = sorted(log_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]

    with open(output_path, "w") as f:
        for file in log_files:
            with open(file, "r") as log:
                first_line = log.readline().strip()
                f.write(first_line + "\n")

    print(f"✅ Task A5 completed: Extracted first lines.")

### 📑 Task A6: Extract H1 titles from Markdown files
def handle_task_A6():
    """Creates an index.json mapping filenames to their first H1 titles."""
    docs_dir = DATA_DIR / "docs"
    output_path = docs_dir / "index.json"
    index = {}

    for file in docs_dir.glob("*.md"):
        with open(file, "r") as f:
            for line in f:
                if line.startswith("# "):
                    index[file.name] = line[2:].strip()
                    break

    with open(output_path, "w") as f:
        json.dump(index, f, indent=4)

    print(f"✅ Task A6 completed: Created index.json.")

### 📧 Task A7: Extract sender’s email from `/data/email.txt`
def handle_task_A7():
    """Extracts the sender's email from /data/email.txt using LLM."""
    input_path = DATA_DIR / "email.txt"
    output_path = DATA_DIR / "email-sender.txt"

    with open(input_path, "r") as f:
        email_content = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the sender's email from this email message."},
            {"role": "user", "content": email_content}
        ]
    )
    email_address = response['choices'][0]['message']['content'].strip()

    with open(output_path, "w") as f:
        f.write(email_address)

    print(f"✅ Task A7 completed: Extracted {email_address}")

### 💳 Task A8: Extract credit card number from `/data/credit-card.png`
def handle_task_A8():
    """Extracts credit card number from an image using OCR."""
    from PIL import Image
    import pytesseract

    image_path = DATA_DIR / "credit-card.png"
    output_path = DATA_DIR / "credit-card.txt"

    card_number = pytesseract.image_to_string(Image.open(image_path)).replace(" ", "").strip()

    with open(output_path, "w") as f:
        f.write(card_number)

    print(f"✅ Task A8 completed: Extracted card number.")

### 💬 Task A9: Find most similar pair of comments
def handle_task_A9():
    """Finds the most similar pair of comments using embeddings."""
    input_path = DATA_DIR / "comments.txt"
    output_path = DATA_DIR / "comments-similar.txt"

    with open(input_path, "r") as f:
        comments = [line.strip() for line in f if line.strip()]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Find the most similar pair of comments."},
            {"role": "user", "content": "\n".join(comments)}
        ]
    )
    similar_pair = response['choices'][0]['message']['content']

    with open(output_path, "w") as f:
        f.write(similar_pair)

    print(f"✅ Task A9 completed: Found similar comments.")

### 🎟 Task A10: Compute total sales for "Gold" tickets
def handle_task_A10():
    """Computes total sales of Gold tickets."""
    db_path = DATA_DIR / "ticket-sales.db"
    output_path = DATA_DIR / "ticket-sales-gold.txt"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
        total_sales = cursor.fetchone()[0]

    with open(output_path, "w") as f:
        f.write(str(total_sales))

    print(f"✅ Task A10 completed: Total Gold ticket sales = {total_sales}")