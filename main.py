def tablename_to_specimenname(nameF):
    return nameF[len('contacts_of_specimen_'):]

name = 'contacts_of_specimen_3220I.csv'

print(tablename_to_specimenname(name))