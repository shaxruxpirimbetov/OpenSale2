import smtplib, secrets, difflib


def search(query, data):
    results = []

    for row in data:
        title = row["title"].lower()
        description = row["description"].lower()
        if query in title or query in description:
            results.append(row)
        else:
            matches = difflib.get_close_matches(query, [title], cutoff=0.6)
            if matches:
                results.append(row)

    return results
    