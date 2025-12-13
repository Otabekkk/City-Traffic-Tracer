import traci

SUMO_CMD = ["sumo", "-c", "bishkek.sumocfg"]

def run_simulation(tl_multiplier=1.0, steps=300):
    traci.start(SUMO_CMD)
    traci.simulationStep()

    # применяем настройки светофоров
    for tl_id in traci.trafficlight.getIDList():
        base_logic = traci.trafficlight.getAllProgramLogics(tl_id)[0]
        new_phases = []

        for phase in base_logic.phases:
            new_phases.append(
                traci.trafficlight.Phase(
                    duration=phase.duration * tl_multiplier,
                    state=phase.state
                )
            )

        new_logic = traci.trafficlight.Logic(
            programID="custom",
            type=base_logic.type,
            currentPhaseIndex=0,
            phases=new_phases
        )

        traci.trafficlight.setProgramLogic(tl_id, new_logic)

    lanes = traci.lane.getIDList()
    edges = traci.edge.getIDList()

    queue_sum = 0
    waiting_sum = 0

    for _ in range(steps):
        traci.simulationStep()
        queue_sum += sum(
            traci.lane.getLastStepHaltingNumber(l) for l in lanes
        )
        waiting_sum += sum(
            traci.edge.getWaitingTime(e) for e in edges
        )

    traci.close()

    return {
        "avg_queue": queue_sum / steps,
        "avg_waiting_time": waiting_sum / steps
    }
