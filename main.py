from KPIs.midweek_distance import MidweekDistance
from schedulers.simulation_schedule import SimulationSchedule
from schedulers.mip_schedule import MIPScheduler
from input_data import InputData


if __name__ == "__main__":
    input_data = InputData.from_csv("data")

    print("-- Scheduling --")
    methods = {
        # "mip": MIPScheduler,
        "simulation": SimulationSchedule
    }
    kpis = [MidweekDistance(input_data)]

    for method_name, method in methods.items():
        print("\n")
        print(method_name)
        schedule = method(input_data).schedule()
        schedule.to_csv(output_file=f"output/{method_name}_schedule.csv")

        for kpi in kpis:
            kpi_value = kpi.compute(schedule)
            print(f"{kpi.name} = {kpi_value}")
