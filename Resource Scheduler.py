
import random
from collections import deque

class Customer:
    def __init__(self, id, priority, service_time):
        self.id = id
        self.priority = priority  # VIP, Corporate, Normal
        self.service_time = service_time

class CustomerGenerator:
    def __init__(self):
        self.customer_id = 0

    def generate_customer(self):
        self.customer_id += 1
        priority = random.choices(["VIP", "Corporate", "Normal"], weights=[0.1, 0.3, 0.6])[0]
        service_time = random.randint(1, 10)
        return Customer(self.customer_id, priority, service_time)
class Agent:
    def __init__(self, id, max_workload):
        self.id = id
        self.max_workload = max_workload
        self.current_workload = 0
        self.availability = True

    def assign_task(self, task):
        if self.current_workload < self.max_workload:
            self.current_workload += 1
            self.availability = False
            return True
        return False

    def complete_task(self):
        self.current_workload -= 1
        if self.current_workload == 0:
            self.availability = True

class Scheduler:
    def __init__(self, agents):
        self.agents = agents
        self.task_queue = deque()

    def add_task(self, task):
        self.task_queue.append(task)

    def round_robin(self):
        for agent in self.agents:
            if agent.availability and self.task_queue:
                task = self.task_queue.popleft()
                agent.assign_task(task)

    def priority_scheduling(self):
        sorted_tasks = sorted(self.task_queue, key=lambda x: x.priority, reverse=True)
        for task in sorted_tasks:
            for agent in self.agents:
                if agent.availability:
                    agent.assign_task(task)
                    self.task_queue.remove(task)
                    break

    def shortest_job_next(self):
        sorted_tasks = sorted(self.task_queue, key=lambda x: x.service_time)
        for task in sorted_tasks:
            for agent in self.agents:
                if agent.availability:
                    agent.assign_task(task)
                    self.task_queue.remove(task)
                    break
import time

class RealTimeMonitor:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def monitor(self):
        while True:
            print("Monitoring Agents...")
            for agent in self.scheduler.agents:
                print(f"Agent {agent.id}: Workload = {agent.current_workload}, Available = {agent.availability}")
            time.sleep(5)
class MetricsCalculator:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.total_wait_time = 0
        self.total_customers = 0

    def update_wait_time(self, wait_time):
        self.total_wait_time += wait_time
        self.total_customers += 1

    def calculate_metrics(self):
        avg_wait_time = self.total_wait_time / self.total_customers if self.total_customers > 0 else 0
        utilization_rates = [agent.current_workload / agent.max_workload for agent in self.scheduler.agents]
        avg_utilization = sum(utilization_rates) / len(utilization_rates)
        print(f"Average Wait Time: {avg_wait_time}")
        print(f"Average Agent Utilization: {avg_utilization}")
if __name__ == "__main__":
    agents = [Agent(i, max_workload=5) for i in range(3)]  # 3 agents
    scheduler = Scheduler(agents)
    monitor = RealTimeMonitor(scheduler)
    metrics = MetricsCalculator(scheduler)

    # Start monitoring in a separate thread
    import threading
    threading.Thread(target=monitor.monitor, daemon=True).start()

    # Simulate customer arrivals and scheduling
    generator = CustomerGenerator()
    for _ in range(20):  # Simulate 20 customers
        customer = generator.generate_customer()
        scheduler.add_task(customer)
        scheduler.round_robin()  # Use Round Robin scheduling
        time.sleep(1)  # Simulate time between customer arrivals

    metrics.calculate_metrics()
