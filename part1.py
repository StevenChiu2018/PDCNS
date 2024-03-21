from survey_database import Disease as DiseaseData
import time
import statsmodels.stats.proportion as confidence_interval_calculator

N = 1000000
diseases = ['chlamydia', 'gonorrhoea', 'syphilis', 'herpes', 'hiv', 'healthy']
disease_data = DiseaseData(
    '/mnt/c/Users/Steven/Desktop/data/projects/CSE568BIO/Assign2/data=1000000', N)

disguised_statistical = disease_data.retrieve_data()

reconstructed_statistical = {
    disease: N - ((len(diseases) - 1) * disguised_statistical[disease]) for disease in diseases}

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
