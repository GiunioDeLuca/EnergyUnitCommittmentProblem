import json
import pandas as pd
import numpy as np
from itertools import product


def totsum(x: np.array, y: np.array) -> float:
    if isinstance(x, list):
        x = np.array(x)
    if isinstance(y, list):
        y = np.array(y)
    return sum(x * y)


def optimAlg(ROCK: dict, finit=6, fref=8, fctapp=1.5) -> list:
    """
    Elaborate the solution.

    :param
        ROCK: dictionary coming from the json file
        finit: sampling number for the first guess solution
        fref: sampling number for the refined solution
    :return:
        the solution in the required format
    """


    DF = pd.DataFrame(ROCK["powerplants"])
    FUELS = pd.Series(ROCK["fuels"])
    Load = ROCK["load"]
    DFDIM = len(DF)

    def aggeff(row):
        if row["type"] == "windturbine":
            return FUELS["wind(%)"] * 0.01
        else:
            return row['efficiency']
    DF['eff'] = DF.apply(aggeff, axis=1)

    # check the maximum power of the power plants
    powermax = totsum(DF['pmax'].to_numpy(), DF['eff'].to_numpy())
    if powermax < Load:
        print(f"""demand cannot be supplied.
        Required Load: {Load:.0f} MWh
        Max supplied Load: {powermax:.0f} MWh
        """)
        return {"message" : "Powerplants cannot supply the required load"}, 406
        # raise Exception(f"""Required demand cannot be supplied.
        # Required Load: {Load:.0f} MWh
        # Max supplied Load: {powermax:.0f} MWh
        # """)

    def getNcomb(row):  # get number of operating status for each powerplant
        if row['type'] == "gasfired":
            return row['pmax'] - row['pmin'] + 1
        else:
            return row['pmax'] - row['pmin']
    DF['Ncomb'] = DF.apply(getNcomb,axis=1)

    def buildcosts(row):  # build array for the energy costs
        if row["type"] == "gasfired":
            return FUELS["gas(euro/MWh)"] + FUELS["co2(euro/ton)"] * 0.3
        elif row["type"] == "turbojet":
            return FUELS["kerosine(euro/MWh)"]
        elif row['type'] == 'windturbine':
            return 0
    DF['costMWh'] = DF.apply(buildcosts,axis=1)

    n = 0  # count the number of solutions evaluated
    initCost = np.inf
    states = [None] * DFDIM
    prec = [None] * DFDIM
    fctpow = 1.0
    while True:
        prodapp = None
        ## define states with precs
        for k in range(DFDIM):
            #print('mannaggia')
            stateapp, prec[k] = np.linspace(DF.iloc[k]['pmin'],
                                            DF.iloc[k]['pmax'],
                                            finit, retstep=True)
            states[k] = np.unique(np.round(stateapp))
            if DF.iloc[k]['type'] == 'gasfired':
                states[k] = np.append(0,states[k])
        #print(states)

        print("Computing first guess solution")
        print("\tLoad\tPower\tCost")
        powertol = min(prec) * fctpow
        for prod in product(*states):
            n += 1
            powersupp = totsum(prod, DF['eff'].to_numpy())
            if - powertol < powersupp - Load < powertol:
                costo = totsum(prod, DF['costMWh'].to_numpy())
                if costo < initCost:
                    initCost = costo
                    prodapp = prod
                    print(f"\t{Load:.0f}  \t{powersupp:.0f}  \t{costo:.0f}")
        if prodapp is not None:
            break
        else:
            print("Recomputing the first guess solution")
            fctpow *= 1.5

    print("Refining first guess solution")
    initCost = np.inf
    while True:
        refiniment = False
        # compute new states and prec
        for k in range(DFDIM):
            stateapp, prec[k] = np.linspace(prodapp[k] - prec[k],
                                            prodapp[k] + prec[k],
                                            fref, retstep=True)
            stateapp = np.unique(np.round(stateapp))
            states[k] = stateapp[((stateapp >= DF.iloc[k]['pmin']) &
                                  (stateapp <= DF.iloc[k]['pmax'])) |
                                 (stateapp == 0)]
            if DF.iloc[k]['type'] == 'gasfired' and\
                    np.array_equiv(0, states[k]):
                states[k] = np.zeros(1)
        powertol = min(prec)
        for prod in product(*states):
            n += 1
            powersupp = totsum(prod, DF['eff'].to_numpy())
            if -powertol/2 < powersupp - Load < powertol/2:
                costo = totsum(prod, DF['costMWh'].to_numpy())
                if costo < initCost:
                    refiniment = True
                    #print("...refining solution")
                    initCost = costo
                    prodapp = prod
                    print(f"\t{Load:.0f}  \t{powersupp:.0f}  \t{costo:.0f}")

        if max(prec) <= 1:
            if not refiniment:
                print("solution not refined")
            break
        else:
            prec = [kak * fctapp for kak in prec]
        #else:
        #    prec = [kak * fctapp for kak in prec]


    prodappint = [int(kak) for kak in prodapp]
    DF['p'] = prodappint

    print(f"Evaluated {n:.3e} out of {DF['Ncomb'].product():.3e} solutions")
    print("Final Solution")
    print(DF[['name', 'type', 'pmin', 'pmax', 'costMWh', 'eff', 'p']].to_string(index=False))
    output = DF[['name', 'p']].to_dict("records")
    return output, 200


def debugAlg(ROCK: dict):
    """Like optimAlg syntax but gives all zero.

    Used for debugging
    """
    DF = pd.DataFrame(ROCK["powerplants"])
    DF['p'] = 0
    return DF[['name', 'p']].to_dict("records")


if __name__ == '__main__':
    with open('../example_payloads/payload2.json', 'r') as jsonnelle:
        coco = json.load(jsonnelle)
    jsonnelle.close()
    pip=optimAlg(coco)
    print(pip)
