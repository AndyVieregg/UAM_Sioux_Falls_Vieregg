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