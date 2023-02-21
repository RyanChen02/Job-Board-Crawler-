job_boards = {
    "Indeed": "https://www.indeed.com/jobs?q=python",
    "Monster": "https://www.monster.com/jobs/search/?q=python",
    "Dice": "https://www.dice.com/jobs?q=python",
}

def scrape_job_board(board_name, board_url):
    response = requests.get(board_url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_listings = soup.find_all("div", class_="job")
    for job in job_listings:
        title = job.find("h2", class_="title").text.strip()
        company = job.find("span", class_="company").text.strip()
        location = job.find("div", class_="location").text.strip()
        salary = job.find("span", class_="salary").text.strip()
        date_posted = job.find("span", class_="date").text.strip()
        # Store data in SQLite database
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute("INSERT INTO jobs (title, company, location, salary, date_posted, board_name) VALUES (?, ?, ?, ?, ?, ?)", (title, company, location, salary, date_posted, board_name))
        conn.commit() 
        
        
def scrape_all_job_boards():
    for board_name, board_url in job_boards.items():
        scrape_job_board(board_name, board_url)
        
        
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    search_query = request.args.get("search_query", "")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE title LIKE ?", ('%' + search_query + '%',))
    jobs = c.fetchall()
    return render_template("index.html", jobs=jobs, search_query=search_query)

if __name__ == "__main__":
    app.run() 
    
    
<!DOCTYPE html>
<html>
<head>
    <title>Job Board Aggregator</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-3">
        <h1>Job Board Aggregator</h1>
        <form class="form-inline mt-3">
            <div class="form-group mr-3">
                <input type="text" class="form-control" placeholder="Search" name="search_query" value="{{ search_query }}">
            </div>
            <button type="
