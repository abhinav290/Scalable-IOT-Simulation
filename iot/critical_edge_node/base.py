from iot.utils.queue_service import AWSService

"""
Critical Edge Node and its functions.
"""
class CriticalEdge:
    queue_service = AWSService()

    def __init__(self):
        # Queue URL
        self.edge_url = 'https://sqs.eu-west-1.amazonaws.com/386707910583/sink-to-edge.fifo'

    def receive_data(self):
        # Receiving critical messages from queue and processing them.
        received_messages = CriticalEdge.queue_service.receive_and_delete_message(self.edge_url)
        if received_messages:
            self.process_data(received_messages)

    def process_data(self, data):

        # Printing critical information.
        for val in data:
            print(val)

    def start(self):
        while True:
            self.receive_data()

if __name__ == '__main__':
    # Creating the instance of Critical Edge and starting it.
    criticalDevice = CriticalEdge()
    criticalDevice.start()
