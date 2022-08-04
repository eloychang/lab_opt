import pandas as pd
from ortools.linear_solver import pywraplp
from datetime import datetime

if __name__ == "__main__":
    start_at = datetime.now()
    solver = pywraplp.Solver.CreateSolver('SCIP')
    data = pd.read_csv("data/branches_example_2.csv", index_col = "branch_name")
    N = 10000

    # Declaramos las variables.
    shipments = {f"X_{branch}" : solver.IntVar(0, N, f"X_{branch}") for branch in data.index}

    branches = {f"Y_{branch}" : solver.BoolVar(f"Y_{branch}") for branch in data.index}

    # Declaramos la función objetivo
    solver.Minimize(sum(branch.cost * shipments[f"X_{branch_name}"] + branch.open_cost * branches[f"Y_{branch_name}"]for branch_name, branch in data.iterrows()))

    # Declaramos las restricciones
    ## Capacidad
    for branch_name, branch in data.iterrows():
        solver.Add(shipments[f"X_{branch_name}"] <= branch.capacity * branches[f"Y_{branch_name}"])
    ## Envios
    solver.Add(sum(var for var_name, var in shipments.items()) == N)
    ## Contrato
    for branch_name, branch in data.iterrows():
        solver.Add(branch.min_shipments * branches[f"Y_{branch_name}"] <= shipments[f"X_{branch_name}"])

    # Resolvemos
    status = solver.Solve()

    # Resulados
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Costo Total: {solver.Objective().Value()}")
        print("Sucursales usadas:")
        for var_name, var in branches.items():
            print(f"{var_name.split('_')[1]}: {var.solution_value()}")
        print("Envios por sucursal:")
        for var_name, var in shipments.items():
            print(f"{var_name.split('_')[1]}: {var.solution_value()}")
    else:
        print("No se encontro el optimo")
    print(f"Total time: {datetime.now() - start_at}")