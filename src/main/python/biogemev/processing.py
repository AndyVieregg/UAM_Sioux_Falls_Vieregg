import numpy as np


def print_results(results=None, ll_list=None):
    print("Results:")

    # General stats

    stats = results.getGeneralStatistics()
    print(f"Sample size: {stats['Sample size'][0]}")
    print(f"Init LL: {stats['Init log likelihood'][0]}")
    print(f"Final LL: {stats['Final log likelihood'][0]}")
    print(f"rho^2: {stats['Rho-square for the init. model'][0]}")
    print(f"rhobar^2: {stats['Rho-square-bar for the init. model'][0]}")

    # Estimated params

    print("Estimated parameters: ")
    print(results.getEstimatedParameters().loc[:, ['Value', 'Std err', 't-test', 'Rob. Std err', 'Rob. t-test']])

    # Validation results if they exist
    if ll_list is not None:
        ll_array = np.array(ll_list)
        print(f"No of LL observations: {np.shape(ll_array)[0]}")
        print(f"Mean LL: {np.mean(ll_array)}")
        print(f"Max LL: {np.amax(ll_array)}")
        print(f"Min LL: {np.amin(ll_array)}")
        print(f"SD of LL: {np.std(ll_array)}")


def results_as_dict(results=None, ll_list=None, ms_scenario=None, est_time="0000"):
    gs = results.getGeneralStatistics()
    ep = results.getEstimatedParameters()

    # Results from all scenarios
    rd = {
        'ms_scenario': ms_scenario,
        'est_time': est_time,
        'sample_size': gs['Sample size'][0],
        'init_ll': gs['Init log likelihood'][0],
        'final_ll': gs['Final log likelihood'][0],
        'rho2': gs['Rho-square for the init. model'][0],
        'rhobar2': gs['Rho-square-bar for the init. model'][0],
        'est_asc_pt': ep.loc['ASC_PT', 'Value'],
        'est_asc_walk': ep.loc['ASC_WALK', 'Value'],
        'est_b_cost': ep.loc['B_COST', 'Value'],
        'est_b_tt': ep.loc['B_TIME', 'Value']
    }

    # UAM-only results
    if 'ASC_UAM' in ep.index.values:
        rd.update({
            'est_asc_uam': ep.loc['ASC_UAM', 'Value']
        })

    # Validation results if validation performed
    if ll_list is not None:
        ll = np.array(ll_list)

        rd.update({
            'val_no': np.shape(ll)[0],
            'val_mean_ll': np.mean(ll),
            'val_min_ll': np.amin(ll),
            'val_max_ll': np.amax(ll),
            'val_ll_sd': np.std(ll)
        })

    return rd