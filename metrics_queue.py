import traci

SUMO_CMD = ["sumo", "-c", "bishkek.sumocfg"]
traci.start(SUMO_CMD)

traci.simulationStep()

lanes = traci.lane.getIDList()
print("Total lanes:", len(lanes))

queue_sum = 0
steps = 0

for _ in range(300):
    traci.simulationStep()
    step_queue = 0

    for lane in lanes:
        step_queue += traci.lane.getLastStepHaltingNumber(lane)

    queue_sum += step_queue
    steps += 1

avg_queue = queue_sum / steps
print("Average queue length:", avg_queue)

traci.close()
