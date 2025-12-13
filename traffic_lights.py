import traci

SUMO_CMD = ["sumo", "-c", "bishkek.sumocfg"]

def run_baseline(tl_id, steps=300):
    return simulate_with_user_phases(tl_id, user_phases={}, steps=steps)

def safe_traci_start(cmd):
    if traci.isLoaded():
        traci.close()
    traci.start(cmd)

def calc_improvement(baseline, custom):
    if baseline <= 0:
        return {
            "percent": 0,
            "direction": "no_data"
        }

    diff = custom - baseline
    percent = diff / baseline * 100

    return {
        "percent": round(percent, 2),
        "direction": "improved" if percent < 0 else "worsened"
    }

def get_traffic_light_phases(tl_id):
    safe_traci_start(SUMO_CMD)
    traci.simulationStep()

    logic = traci.trafficlight.getAllProgramLogics(tl_id)[0]

    phases = []
    for i, phase in enumerate(logic.phases):
        phases.append({
            "index": i,
            "duration": phase.duration,
            "state": phase.state
        })

    traci.close()
    return phases


# def simulate_with_user_phases(tl_id, user_phases, steps=300):
#     safe_traci_start(SUMO_CMD)
#     traci.simulationStep()

#     base_logic = traci.trafficlight.getAllProgramLogics(tl_id)[0]

#     new_phases = []
#     for i, phase in enumerate(base_logic.phases):
#         new_duration = user_phases.get(i, phase.duration)
#         new_phases.append(
#             traci.trafficlight.Phase(
#                 duration=new_duration,
#                 state=phase.state
#             )
#         )

#     new_logic = traci.trafficlight.Logic(
#         programID="user_custom",
#         type=base_logic.type,
#         currentPhaseIndex=0,
#         phases=new_phases
#     )

#     traci.trafficlight.setProgramLogic(tl_id, new_logic)

#     lanes = traci.lane.getIDList()
#     edges = traci.edge.getIDList()

#     queue_sum = 0
#     waiting_sum = 0

#     for _ in range(steps):
#         traci.simulationStep()
#         queue_sum += sum(
#             traci.lane.getLastStepHaltingNumber(l) for l in lanes
#         )
#         waiting_sum += sum(
#             traci.edge.getWaitingTime(e) for e in edges
#         )

#     traci.close()

#     return {
#         "avg_queue": queue_sum / steps,
#         "avg_waiting_time": waiting_sum / steps
#     }


def list_traffic_lights():
    safe_traci_start(SUMO_CMD)
    traci.simulationStep()

    tls_ids = traci.trafficlight.getIDList()

    result = []
    for tl_id in tls_ids:
        logic = traci.trafficlight.getAllProgramLogics(tl_id)[0]
        result.append({
            "id": tl_id,
            "phases_count": len(logic.phases)
        })

    traci.close()
    return result


def simulate_with_user_phases(tl_id, user_phases, steps=300):
    safe_traci_start(SUMO_CMD)
    traci.simulationStep()

    base_logic = traci.trafficlight.getAllProgramLogics(tl_id)[0]

    # применяем пользовательские duration
    new_phases = []
    for i, phase in enumerate(base_logic.phases):
        new_duration = user_phases.get(i, phase.duration)
        new_phases.append(
            traci.trafficlight.Phase(
                duration=new_duration,
                state=phase.state
            )
        )

    new_logic = traci.trafficlight.Logic(
        programID="user_custom",
        type=base_logic.type,
        currentPhaseIndex=0,
        phases=new_phases
    )
    traci.trafficlight.setProgramLogic(tl_id, new_logic)

    lanes = traci.lane.getIDList()
    edges = traci.edge.getIDList()

    # --- агрегаты ---
    queue_sum = 0
    waiting_sum = 0

    # --- таймлайны ---
    timeline_queue = []
    timeline_waiting = []
    timeline_phase = []

    for _ in range(steps):
        traci.simulationStep()

        step_queue = sum(
            traci.lane.getLastStepHaltingNumber(l) for l in lanes
        )
        step_waiting = sum(
            traci.edge.getWaitingTime(e) for e in edges
        )
        current_phase = traci.trafficlight.getPhase(tl_id)

        queue_sum += step_queue
        waiting_sum += step_waiting

        timeline_queue.append(step_queue)
        timeline_waiting.append(step_waiting)
        timeline_phase.append(current_phase)

    traci.close()

    return {
        "avg_queue": queue_sum / steps,
        "avg_waiting_time": waiting_sum / steps,
        "timeline": {
            "queue": timeline_queue,
            "waiting_time": timeline_waiting,
            "phase": timeline_phase
        }
    }
