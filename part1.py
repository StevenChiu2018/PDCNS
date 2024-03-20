from survey_database import Disease as DiseaseData

N = 1000000
diseases = ['chlamydia', 'gonorrhoea', 'syphilis', 'herpes', 'hiv']
disease_data = DiseaseData('http://178.16.143.126:8000/get_samples',
                           '/mnt/c/Users/Steven/Desktop/data/projects/CSE568BIO/Assign2/data=1000000', N)

disguised_statistical = disease_data.retrieve_data()

reconstructed_statistical = {
    disease: N - ((len(diseases) - 1) * disguised_statistical[disease]) for disease in diseases}

for disease in diseases:
    print(disease + ': ' + str(disguised_statistical[disease]) + ' -> ' + str(
        reconstructed_statistical[disease]) + ' : ' + str(reconstructed_statistical[disease] * 100 / N) + ' %')
