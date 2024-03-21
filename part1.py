import matplotlib.pyplot as plt
import matplotlib
from survey_database import Disease as DiseaseData
import time
import statsmodels.stats.proportion as confidence_interval_calculator

matplotlib.use('Agg')


def get_disguised_statistical(rows, n):
    disease_dict = {}
    for i in range(n - 10000, n):
        if rows[i] in disease_dict:
            disease_dict[rows[i]] += 1
        else:
            disease_dict[rows[i]] = 1

    return disease_dict


N = 1000000

diseases = ['chlamydia', 'gonorrhoea',
            'syphilis', 'herpes', 'hiv', 'healthy']

disease_data = DiseaseData('http://178.16.143.126:8000/get_samples',
                           '/mnt/c/Users/Steven/Desktop/data/projects/CSE568BIO/Assign2/data=1000000', N)


disguised_rows = disease_data.retrieve_row()
upper = [[] for _ in range(len(diseases))]
lower = [[] for _ in range(len(diseases))]
rate_in_population = [[] for _ in range(len(diseases))]
running_times = []
negative = []


for n in range(10000, 1000000, 10000):
    disguised_statistical = get_disguised_statistical(disguised_rows, n)

    start_at = time.time()
    prevalence_result = []
    for disease in diseases:
        prevalence_result.append(
            n - ((len(diseases) - 1) * disguised_statistical[disease]))
    end_at = time.time()

    confidence_interval = confidence_interval_calculator.multinomial_proportions_confint(
        counts=prevalence_result, alpha=0.01)

    for i, (lo, up) in enumerate(confidence_interval):
        upper[i].append(up)
        lower[i].append(lo)
        rate_in_population[i].append(disguised_statistical[diseases[i]])

    running_times.append(end_at - start_at)

for i in range(len(diseases)):
    diff = []
    for j in range(len(upper[i])):
        diff.append(upper[i][j] - lower[i][j])

    plt.plot(range((len(diff))), diff)
    plt.savefig('./relationship_survey_confidence_' + diseases[i] + '.png')
    plt.close()

for i in range(len(diseases)):
    plt.plot(range(len(rate_in_population[i])),
             rate_in_population[i], label=diseases[i])

plt.legend()
plt.savefig('./rate_in_population' + '.png')
plt.close()

plt.plot(range(len(running_times)), running_times)
plt.savefig('./running_times.png')
plt.close()

print('Average: ' + str(sum(running_times) / len(running_times)))
print('Max: ' + str(max(running_times)))
print('Min: ' + str(min(running_times)))
