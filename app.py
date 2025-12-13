from fastapi import FastAPI
from traffic_lights import (
    get_traffic_light_phases,
    simulate_with_user_phases,
    list_traffic_lights,
    calc_improvement
)
from fastapi.middleware.cors import CORSMiddleware
from schemas import TrafficLightPhasesRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/traffic-lights")
def get_traffic_lights():
    return {
        "count": len(list_traffic_lights()),
        "traffic_lights": list_traffic_lights()
    }


# @app.get("/traffic-lights/{tl_id}")
# def get_traffic_light(tl_id: str):
#     phases = get_traffic_light_phases(tl_id)
#     baseline = simulate_with_user_phases(tl_id, user_phases={})

#     return {
#         "traffic_light_id": tl_id,
#         "phases": phases,
#         "baseline": baseline
#     }

@app.get("/traffic-lights/{tl_id}")
def get_traffic_light(tl_id: str):
    phases = get_traffic_light_phases(tl_id)
    return {
        "traffic_light_id": tl_id,
        "phases": phases
    }



# @app.post("/traffic-light/{tl_id}/simulate")
# def simulate(tl_id: str, payload: dict):
#     """
#     payload example:
#     {
#       "phases": {
#         "0": 35,
#         "1": 5,
#         "2": 20
#       }
#     }
#     """
#     user_phases = {
#         int(k): v for k, v in payload.get("phases", {}).items()
#     }

#     result = simulate_with_user_phases(tl_id, user_phases)

#     return {
#         "traffic_light_id": tl_id,
#         "result": result
#     }



# @app.post("/traffic-lights/{tl_id}/compare")
# def compare(tl_id: str, payload: dict):
#     user_phases = {
#         int(k): v for k, v in payload.get("phases", {}).items()
#     }

#     baseline = simulate_with_user_phases(tl_id, {})
#     custom = simulate_with_user_phases(tl_id, user_phases)

#     queue_cmp = calc_improvement(
#         baseline["avg_queue"],
#         custom["avg_queue"]
#     )

#     wait_cmp = calc_improvement(
#         baseline["avg_waiting_time"],
#         custom["avg_waiting_time"]
#     )

#     return {
#         "traffic_light_id": tl_id,
#         "baseline": baseline,
#         "custom": custom,
#         "comparison": {
#             "avg_queue": queue_cmp,
#             "avg_waiting_time": wait_cmp
#         },
#         "summary": {
#             "text": "Очереди и время ожидания уменьшились"
#             if queue_cmp["percent"] < 0 and wait_cmp["percent"] < 0
#             else "Изменения требуют доработки"
#         }
#     }


@app.post("/traffic-lights/{tl_id}/compare")
def compare(tl_id: str, payload: TrafficLightPhasesRequest):
    user_phases = payload.phases

    baseline = simulate_with_user_phases(tl_id, {})
    custom = simulate_with_user_phases(tl_id, user_phases)

    queue_cmp = calc_improvement(
        baseline["avg_queue"],
        custom["avg_queue"]
    )
    wait_cmp = calc_improvement(
        baseline["avg_waiting_time"],
        custom["avg_waiting_time"]
    )

    return {
        "traffic_light_id": tl_id,

        "baseline": {
            "avg_queue": baseline["avg_queue"],
            "avg_waiting_time": baseline["avg_waiting_time"],
            "timeline": baseline["timeline"]
        },

        "custom": {
            "avg_queue": custom["avg_queue"],
            "avg_waiting_time": custom["avg_waiting_time"],
            "timeline": custom["timeline"]
        },

        "comparison": {
            "avg_queue": queue_cmp,
            "avg_waiting_time": wait_cmp
        },

        "summary": {
            "text": (
                "Очереди и время ожидания уменьшились"
                if queue_cmp["percent"] < 0 and wait_cmp["percent"] < 0
                else "Требуется дополнительная настройка"
            )
        }
    }
