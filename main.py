from queue import Queue

class Event:
    def __init__(self, payload):
        self.payload = payload

    def process(self):
        raise NotImplementedError("Subclasses must implement this method.")

class ApplicationSentEvent(Event):
    def process(self):
        print(f"Application sent: {self.payload}")

class ApplicationAcceptedEvent(Event):
    def process(self):
        print(f"Application accepted: {self.payload}")

class ApplicationRejectedEvent(Event):
    def process(self):
        print(f"Application rejected: {self.payload}")

class EnrollmentConfirmedEvent(Event):
    def process(self):
        print(f"Enrollment confirmed: {self.payload}")

class CommunicationQueue:
    def __init__(self):
        self.queue = Queue()

    def add_event(self, event):
        self.queue.put(event)

    def process_events(self):
        while not self.queue.empty():
            event = self.queue.get()
            event.process()

class Student:
    def __init__(self, name, communication_queue):
        self.name = name
        self.communication_queue = communication_queue

    def send_application(self, university):
        payload = {
            "student": self.name,
            "university": university.name
        }
        event = ApplicationSentEvent(payload)
        self.communication_queue.add_event(event)
        university.receive_application(event)

class University:
    def __init__(self, name, communication_queue):
        self.name = name
        self.received_applications = []
        self.communication_queue = communication_queue

    def receive_application(self, event):
        self.received_applications.append(event.payload)
        print(f"{event.payload['student']} applied to {self.name}.")

    def respond_to_application(self, student, decision):
        payload = {
            "student": student.name,
            "university": self.name,
            "decision": decision
        }
        if decision == "accepted":
            event = ApplicationAcceptedEvent(payload)
        else:
            event = ApplicationRejectedEvent(payload)

        self.communication_queue.add_event(event)

if __name__ == "__main__":
    communication_queue = CommunicationQueue()

    student1 = Student("Mert", communication_queue)
    student2 = Student("Zeynep", communication_queue)
    university1 = University("İstanbul Üniversitesi", communication_queue)
    university2 = University("Ankara Üniversitesi", communication_queue)

    student1.send_application(university1)
    student2.send_application(university2)

    university1.respond_to_application(student1, "accepted")
    university2.respond_to_application(student2, "rejected")

    print("Processing events:")
    communication_queue.process_events()