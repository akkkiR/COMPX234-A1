import threading
import time
import random
from platform import machine
from threading import main_thread

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads

        # Create semaphores
        self.semaphore = threading.Semaphore(self.NUM_PRINTERS)  # counting semaphore
        self.binary = threading.Semaphore(1)

    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here

        for i in range(self.NUM_MACHINES):
            machine = self.machineThread(i,self)
            self.mThreads.append(machine)

        for i in range(self.NUM_PRINTERS):
            printer = self.printerThread(i,self)
            self.pThreads.append(printer)

        # Start all the threads
        # Write code here

        for machine in self.mThreads:
            machine.start()

        for printer in self.pThreads:
            printer.start()

        # Let the simulation run for some time
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        self.sim_active = False

        # Wait until all printer threads finish by joining them
        # Write code here

        for printer in self.pThreads:
            printer.join()

        print("Simulation finish")

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
            print(f"Printer ID: {printerID} : now available")
            # Write code here for Binary and counting Semaphore
            self.outer.binary.acquire()
            # Acquire the binary semaphore to ensure mutual exclusion
            self.outer.print_list.queuePrint(printerID)
            # Print from the queue
            self.outer.print_list.queuePrint(printerID)
            # Release the binary semaphore
            self.outer.binary.release()
            # Increment the semaphore count so that machines can send requests
            self.outer.semaphore.release()

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def isRequestSafe(self, id):
            print(f"Machine {id} Checking availability")
            # Acquire counting semaphore (wait for an available printer)
            self.outer.semaphore.acquire()
            # Acquire binary semaphore for mutual exclusion of the print queue
            self.outer.binary.acquire()
            # Both semaphores acquired
            print(f"Machine {id} will proceed")


        def printRequest(self, id):
            print(f"Machine {id} Sent a print request")
            # Build a print document
            doc = printDoc(f"My name is machine {id}", id)
            # Insert it in the print queue
            self.outer.print_list.queueInsert(doc)

        def postRequest(self, id):
            print(f"Machine {id} Releasing binary semaphore")
            # Release the binary semaphore
            self.outer.binary.release()