import csv

CHUNK_SIZE = 100000  # You can tune this (based on memory)


def load_users_chunk(reader, chunk_size):
    chunk = {}
    count = 0

    for row in reader:
        user_id = row['user_id']
        chunk[user_id] = row
        count += 1

        if count >= chunk_size:
            yield chunk
            chunk = {}
            count = 0

    if chunk:
        yield chunk


def join_files(users_file, transactions_file, output_file):
    with open(users_file, 'r') as u_file, \
         open(transactions_file, 'r') as t_file, \
         open(output_file, 'w', newline='') as out_file:

        user_reader = csv.DictReader(u_file)
        transaction_reader = csv.DictReader(t_file)

        # Remove duplicate user_id from transactions
        transaction_fields = [col for col in transaction_reader.fieldnames if col != 'user_id']

        # Final columns
        fieldnames = user_reader.fieldnames + transaction_fields

        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        # Process users in chunks
        for user_chunk in load_users_chunk(user_reader, CHUNK_SIZE):

            print(f"Processing chunk: {len(user_chunk)} users")

            # Restart transactions file
            t_file.seek(0)
            transaction_reader = csv.DictReader(t_file)

            for t_row in transaction_reader:
                user_id = t_row['user_id']

                if user_id in user_chunk:
                    merged_row = {
                        **user_chunk[user_id],
                        **{k: v for k, v in t_row.items() if k != 'user_id'}
                    }
                    writer.writerow(merged_row)

    print("✅ Join completed. Output saved to:", output_file)


if __name__ == "__main__":
    join_files(
        "data/users.csv",
        "data/transactions.csv",
        "data/result.csv"
    )