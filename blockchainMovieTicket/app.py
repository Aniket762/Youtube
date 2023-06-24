import json
import time

# Class representing a block in the blockchain
class Block:
    def __init__(self, index, timestamp, data, previous_block_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_block_hash = previous_block_hash
        self.hash = None

    def calculate_hash(self):
        # Convert the block object to a JSON string
        block_string = json.dumps(self.__dict__, sort_keys=True, cls=BlockEncoder)
        # Calculate the hash of the JSON string
        return str(hash(block_string))

# encoder: Block Objects to JSON strings by Dict
class BlockEncoder(json.JSONEncoder):
    def default(self, o): # o=object
        # Check if the object is an instance of the Block class
        if isinstance(o, Block):
            # Return the dictionary representation of the block object
            return o.__dict__
        elif isinstance(o, MovieTicket):
            return o.__dict__
        return super().default(o)

# Decoder: !encoder
class BlockDecoder(json.JSONDecoder):
    def object_hook(self, d):
        if 'index' in d and 'timestamp' in d and 'data' in d and 'previous_block_hash' in d and 'hash' in d:
            block = Block(d['index'], d['timestamp'], d['data'], d['previous_block_hash'])
            block.hash = d['hash']
            return block
        return d

# Class representing the blockchain
class Blockchain:
    def __init__(self):
        # initialize the blockchain with genesis block
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # create the genesis block with index 0, current timestamp
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")

    def get_latest_block(self):
         # Create the genesis block with index 0, current timestamp, a message, and previous block hash of '0'
        return self.chain[-1]

    def add_block(self, new_block):
        # Set the previous block hash and calculate the hash of the new block
        new_block.previous_block_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        # Add the new block to the blockchain
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Check if the blockchain is valid by verifying the hashes and previous block hashes
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_block_hash != previous_block.hash:
                return False

        return True

# Class representing a movie ticket
class MovieTicket:
    def __init__(self, movie_name, ticket_id, customer_name):
        self.movie_name = movie_name
        self.ticket_id = ticket_id
        self.customer_name = customer_name

# Class representing the movie ticket booking system
class MovieTicketBookingSystem:
    def __init__(self):
        # Create a blockchain instance for storing movie ticket data
        self.blockchain = Blockchain()
        # List to store pending transactions
        self.pending_transactions = []

    def book_ticket(self, movie_name, ticket_id, customer_name):
        # Create a new MovieTicket object
        ticket = MovieTicket(movie_name, ticket_id, customer_name)
        # Add the ticket to the list of pending transactions
        self.pending_transactions.append(ticket)
        # Mine the pending transactions and add them to a new block in the blockchain
        self.mine_pending_transactions()

    def mine_pending_transactions(self):
        # Create a new block with the pending transactions
        new_block = Block(
            len(self.blockchain.chain), # Index of the new block
            time.time(),    # current timestamp
            self.pending_transactions, # pending transactions (movie tickets)
            self.blockchain.get_latest_block().hash # previous block hash
        )
        # add the new block to the blockchain
        self.blockchain.add_block(new_block)
        # Clear the list of pending transactions
        self.pending_transactions = []

    def get_ticket_count(self):
        # Return the number of tickets in the latest block of the blockchain
        return len(self.blockchain.get_latest_block().data)

    def display_tickets(self):
        # Display the movie tickets stored in the blockchain
        for block in self.blockchain.chain:
            if isinstance(block.data, list):
                for ticket in block.data:
                    print("Movie:", ticket.movie_name)
                    print("Ticket ID:", ticket.ticket_id)
                    print("Customer:", ticket.customer_name)
                    print()
            else:
                print("Message:", block.data["message"])
                print()

    def display_blockchain(self):
        # Display the entire blockchain
        for block in self.blockchain.chain:
            print("Block:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Block Hash:", block.previous_block_hash)
            print("Hash:", block.hash)
            print()

# Create a movie ticket booking system
booking_system = MovieTicketBookingSystem()

while True:
    print("1. Book Ticket")
    print("2. Display Tickets")
    print("3. Display Blockchain")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        movie_name = input("Enter movie name: ")
        ticket_id = input("Enter ticket ID: ")
        customer_name = input("Enter customer name: ")
        booking_system.book_ticket(movie_name, ticket_id, customer_name)
    elif choice == "2":
        booking_system.display_tickets()
    elif choice == "3":
        booking_system.display_blockchain()
    elif choice == "4":
        print("Exiting the System")
        break
    else:
        print("Invalid Choice, Please try again ^-^")
