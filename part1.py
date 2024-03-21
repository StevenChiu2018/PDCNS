from survey_database import Disease as DiseaseData
import time
import random
import statsmodels.stats.proportion as confidence_interval_calculator

N = 1000000
diseases = ['chlamydia', 'gonorrhoea', 'syphilis', 'herpes', 'hiv', 'healthy']
probability = [1, 1, 1, 1, 1, 1]
exclude_self_probability = []
total = sum(probability)
for cur_probability in probability:
    exclude_self_probability.append(total - cur_probability)
disease_data = DiseaseData('http://178.16.143.126:8000/get_samples',
                           '/mnt/c/Users/Steven/Desktop/data/projects/CSE568BIO/Assign2/data=1000000', N)

old_disguised_statistical = disease_data.retrieve_data()

disguised_statistical = {disease: 0 for disease in diseases}

print('\n')

reconstructed_statistical = {
    disease: N - ((len(diseases) - 1) * old_disguised_statistical[disease]) for disease in diseases}

for i, disease in enumerate(diseases):
    for _ in range(reconstructed_statistical[disease]):
        while True:
            new_disease = random.choices(diseases, probability)[0]
            if new_disease != disease:
                disguised_statistical[new_disease] += 1
                break

print(old_disguised_statistical)
print(disguised_statistical)

reconstructed_statistical = {}


for i, disease in enumerate(diseases):
    possibility = 0 if probability[i] == 0 else (
        exclude_self_probability[i] / probability[i])
    reconstructed_statistical[disease] = N - \
        disguised_statistical[disease] * possibility

print('\n')

start_at = time.time()
prevalence_result = []
total_number = sum(list(reconstructed_statistical.values()))
for disease in diseases:
    print(disease + ':')
    print('\tY: ' + str(disguised_statistical[disease]))
    print('\tA: ' + str(reconstructed_statistical[disease]))
    print('\tRate of people with this disease: ' +
          str(reconstructed_statistical[disease] * 100 / total_number) + ' %')
    prevalence_result.append(reconstructed_statistical[disease])

confidence_interval = confidence_interval_calculator.multinomial_proportions_confint(
    counts=prevalence_result, alpha=0.01)

print(confidence_interval)
print('It takes ' + str(time.time() - start_at) + ' to calculate result')
