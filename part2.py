from survey_database import Disease as DiseaseData
import statsmodels.stats.proportion as confidence_interval_calculator
import time

N = 1000000

disguised_data = DiseaseData(
    '/mnt/c/Users/Steven/Desktop/data/projects/CSE568BIO/Assign2/data=1000000', N)

herpes = {'yes': 0, "no": 0}
cities = {}
herpes_city = {}

for row in disguised_data.retrieve_rows():
    row = row.split(',')
    has_herpes_string = 'no'
    if row[0] == 'herpes':
        herpes['yes'] += 1
        has_herpes_string = 'yes'
    else:
        herpes['no'] += 1

    if row[1] in cities:
        cities[row[1]] += 1
    else:
        cities[row[1]] = 1

    if f'{has_herpes_string} {row[1]}' in herpes_city:
        herpes_city[f'{has_herpes_string} {row[1]}'] += 1
    else:
        herpes_city[f'{has_herpes_string} {row[1]}'] = 1

start_at = time.time()
prevalence_result = []
for city in ['Mesa', 'Tempe', 'Scottsdale', 'Phoenix', 'Chandler']:
    prevalence = N - (5 * herpes['yes'] + 4 * cities[city] -
                      20 * herpes_city[f'yes {city}'])
    print(city)
    print('\tY: ' + str(herpes_city[f'yes {city}']))
    print('\tA: ' + str(prevalence))
    print('\tRate: ' + str(prevalence * 100 / N))
    prevalence_result.append(prevalence)

prevalence_result.append(N - sum(prevalence_result))

confidence_interval = confidence_interval_calculator.multinomial_proportions_confint(
    counts=prevalence_result, alpha=0.01)

print(confidence_interval)
print('It takes ' + str(time.time() - start_at) + ' to calculate result')
