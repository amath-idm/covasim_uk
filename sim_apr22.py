'''
UK scenarios
'''

import sciris as sc
import covasim as cv

# Check version
cv.check_version('0.28.3')
cv.git_info('covasim_version.json')

do_plot = 1
do_save = 1
do_show = 1
verbose = 1
seed    = 1

version   = 'v1'
date      = '2020apr20'
folder    = f'results_{date}'
file_path = f'{folder}/phase_{version}' # Completed below
data_path = 'UK_Covid_19_cases_apr22.xlsx'
pop_path  = f'{file_path}.pop'
fig_path  = f'{file_path}.png'

start_day = sc.readdate('2020-02-14')
end_day   = sc.readdate('2020-04-26')
n_days    = (end_day - start_day).days

# Set the parameters
total_pop = 66.65e6 # UK population size
pop_size = 100e3 # Actual simulated population
ratio = int(total_pop/pop_size)
pop_scale = ratio
pop_infected = 5000
pop_type = 'hybrid'
beta = 0.016
cons = {'h':3.0, 's':20, 'w':20, 'c':20}

pars = sc.objdict(
    pop_size     = pop_size,
    pop_infected = pop_infected//pop_scale,
    pop_scale    = pop_scale,
    pop_type     = pop_type,
    start_day    = start_day,
    n_days       = n_days,
    asymp_factor = 0.8,
    beta         = beta,
    contacts     = cons,
)

# Create the simulation
sim = cv.Sim(datafile=data_path, popfile=pop_path)

# Interventions

interventions = []

ti_start = '2020-05-01'
ti_day   = (sc.readdate(ti_start)-start_day).days

beta_days      = ['2020-03-20', '2020-03-30', '2020-04-12', ti_start]
beta_days      = [(sc.readdate(day)-start_day).days for day in beta_days]
h_beta_changes = [1.00, 1.00, 1.00, 1.00]
s_beta_changes = [1.00, 1.00, 0.00, 0.00]
w_beta_changes = [0.90, 0.80, 0.15, 0.15]
c_beta_changes = [0.90, 0.80, 0.15, 0.15]

h_beta = cv.change_beta(days=beta_days, changes=h_beta_changes, layers='h')
s_beta = cv.change_beta(days=beta_days, changes=s_beta_changes, layers='s')
w_beta = cv.change_beta(days=beta_days, changes=w_beta_changes, layers='w')
c_beta = cv.change_beta(days=beta_days, changes=c_beta_changes, layers='c')

interventions = [h_beta, w_beta, s_beta, c_beta]

# Testing interventions

# sympt_test = 40.0
# daily_tests = sim.data['new_tests']//ratio
# symp_p  = 0.20
# asymp_p = 0.05
# test_t  = 1
# trace_p = {'h':1.0, 's':1.0, 'w':1.0, 'c':1.0}
# trace_t = {'h':1, 's':1, 'w':1, 'c':1}

# interventions += [
#     cv.test_num(daily_tests=daily_tests, sympt_test=sympt_test),
#     cv.test_prob(start_day=ti_day, symp_prob=symp_p, asymp_prob=asymp_p, test_delay=0.0),
#     cv.contact_tracing(start_day=ti_day, trace_probs=trace_p, trace_time=trace_t),
# ]


pars['interventions'] = interventions

sim.update_pars(pars)

if __name__ == '__main__':

    sim.run()

    if do_save:
        sim.save(f'{file_path}.sim', keep_people=True)

    if do_plot:
        fig = sim.plot(do_save=do_save, do_show=do_show, fig_path=fig_path, interval=7)
