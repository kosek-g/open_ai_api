import sqlite3
import json

def extract_order_info_from_email(email_info):
    # Connect to the SQLite database
    conn = sqlite3.connect('C:/Users/grzegorz.kosek/Desktop/My Projects/Data & AI/GenAI/GenAI%20Traning/sql_db/gen_ai.db')
    cursor = conn.cursor()

    try:
        # Extract information from the provided email
        email_content, email_date, client_address = email_info

        # Query to retrieve client ID based on the client's address from the email
        cursor.execute("SELECT client_id FROM clients WHERE address = ?", (client_address,))
        client_id = cursor.fetchone()

        if client_id:
            client_id = client_id[0]

            # Query to fetch previous orders for the identified client
            cursor.execute("""
                SELECT client_orders.order_no, products.product_name, client_orders.order_date, client_orders.quantity, client_orders.payment_status
                FROM client_orders
                INNER JOIN products ON client_orders.product_id = products.product_id
                WHERE client_orders.client_id = ?
                ORDER BY client_orders.order_date DESC
                """, (client_id,))

            previous_orders = cursor.fetchall()

            if previous_orders:
                # Convert fetched orders into JSON format
                orders_info = []
                for order in previous_orders:
                    order_info = {
                        'order_no': order[0],
                        'product_name': order[1],
                        'order_date': order[2],
                        'quantity': order[3],
                        'payment_status': order[4]
                    }
                    orders_info.append(order_info)

                # Convert orders info to JSON and print it
                orders_json = json.dumps(orders_info, indent=4)
                return orders_json
            else:
                print("No previous orders found for the client associated with the provided address.")

        else:
            print("No client found with the provided address.")

    except sqlite3.Error as e:
        print("Error querying the database:", e)

    finally:
        # Close the database connection
        conn.close()