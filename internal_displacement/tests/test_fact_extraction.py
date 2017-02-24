from unittest import TestCase
from internal_displacement.interpreter import Interpreter
from internal_displacement.report import Report
import spacy


outcome_map = {
    0: 'P', 1: 'F'
}

nlp = spacy.load("en")
person_reporting_terms = [
    'displaced', 'evacuated', 'forced', 'flee', 'homeless', 'relief camp',
    'sheltered', 'relocated', 'stranded', 'stuck', 'stranded', "killed", "dead", "died", "drown"
]

structure_reporting_terms = [
    'destroyed', 'damaged', 'swept', 'collapsed',
    'flooded', 'washed', 'inundated', 'evacuate'
]

person_reporting_units = ["families", "person", "people", "individuals", "locals", "villagers", "residents",
                            "occupants", "citizens", "households", "life"]

structure_reporting_units = ["home", "house", "hut", "dwelling", "building", "shop", "business", "apartment",
                                     "flat", "residence"]

relevant_article_terms = ['Rainstorm', 'hurricane',
                          'tornado', 'rain', 'storm', 'earthquake']
relevant_article_lemmas = [t.lemma_ for t in nlp(
    " ".join(relevant_article_terms))]


interpreter = Interpreter(nlp, person_reporting_terms, structure_reporting_terms, person_reporting_units,
                          structure_reporting_units, relevant_article_lemmas, data_path='data')


def test_fact_extraction(article, expected_reports):
    print(article)
    generated_reports = interpreter.process_article_new(article)
    outcome = 0
    for er in expected_reports:
        if er not in generated_reports:
            print("FAILED TO GENERATE EXPECTED REPORT:")
            er.display()
            outcome = 1
    for gr in generated_reports:
        if gr not in expected_reports:
            print("GENERATED UNEXPECTED REPORT:")
            gr.display()
            outcome = 1
    if outcome == 1:
        print("Article facts incorrectly extracted.")
        print("GENERATED:")
        for gr in generated_reports:
            gr.display()
        print("EXPECTED:")
        for er in expected_reports:
            er.display()
    else:
        print("ARTICLE FACTS CORRECTLY EXTRACTED.")
    return outcome


outcomes = []

article = "Further severe weather, floods and landslides have left 14 people dead and 4 missing in southern China.  Yesterday the Chinese government said that the storms and heavy rainfall from 18 to 22 June 2014 affected nine southern provinces. 8,700 homes have been destroyed, 66,000 homes damaged and forced 337,000 people to evacuate. 42,000 hectares of crops have also been destroyed. Further heavy rainfall is forecast for the next 24 hours."
expected_reports = []
expected_reports.append(Report(['China'], [], 'leave dead', 'people', 14, ''))
expected_reports.append(
    Report(['China'], ['Yesterday'], 'destroy', 'home', '8,700', ''))
expected_reports.append(
    Report(['China'], ['Yesterday'], 'damage', 'home', '66,000', ''))
expected_reports.append(
    Report(['China'], ['Yesterday'], 'force', 'people', '337,000', ''))
test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)

article = "Flash flooding across Afghanistan and Pakistan has left more than 160 dead and dozens stranded in one of South Asia's worst natural disasters this year, say officials.  The flooding, caused by unusually heavy rain, has left villagers stuck in remote areas without shelter, food or power.  Mountainous Afghanistan was the worst hit, with 61 people killed and approximately 500 traditional mud-brick homes washed away in more than a dozen villages in Sarobi, a rural district less than an hour from Kabul, officials said.  Floods left a village devastated in the remote eastern Afghan province of Nuristan. At least 60 homes were destroyed across three districts, said provincial spokesman Mohammad Yusufi. No one was killed.  Authorities have been unable to deliver aid to some badly affected villages by land as roads in the area are controlled by the Taliban, Yusufi added.  “We have asked the national government for help as have an overwhelming number of locals asking for assistance, but this is a Taliban-ridden area,” Yusufi said.  At least 24 people were also died in two other eastern border provinces, Khost and Nangarhar, according to local officials. More than fifty homes and shops were destroyed and thousands of acres of farmland flooded.  In Pakistan monsoon rains claimed more than 80 lives, local media reported. Houses collapsing, drowning and electrocution all pushed up the death toll, said Sindh Information Minister Sharjeel Inam Memon.  In Karachi, the commercial capital and a southern port city that is home to 18 million people, poor neighborhoods were submerged waist-deep in water and many precincts suffered long power outages. Deaths were also reported in the north and west of the country.  Additional reporting by Reuters"
expected_reports = []
expected_reports.append(Report(['Afghanistan', 'Pakistan'], [
                        'this year'], 'leave dead', 'person', 160, ''))
expected_reports.append(Report(['Afghanistan', 'Pakistan'], [
                        'this year'], 'strand', 'person', 'dozens', ''))
expected_reports.append(Report(['Afghanistan', 'Pakistan'], [
                        'this year'], 'stick', 'villager', None, ''))
expected_reports.append(
    Report(['Sarobi'], ['this year'], 'kill', 'people', 61, ''))
expected_reports.append(
    Report(['Sarobi'], ['this year'], 'wash', 'home', 500, ''))
expected_reports.append(
    Report(['Nuristan'], ['this year'], 'destroy', 'home', 60, ''))
expected_reports.append(Report(['Khost', 'Nangarhar'], [
                        'this year'], 'die', 'people', 24, ''))
expected_reports.append(Report(['Khost', 'Nangarhar'], [
                        'this year'], 'destroy', 'homes and shops', "fifty", ''))
expected_reports.append(
    Report(['Pakistan'], ['this year'], 'claim lives', 'life', 80, ''))
expected_reports.append(
    Report(['Pakistan'], ['this year'], 'collapse', 'house', None, ''))

test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)


article = "It was early Saturday when a flash flood hit the area and washed away more than 500 houses"
expected_reports = []
expected_reports.append(Report([],['early Saturday'], 'wash', 'house', 500, ''))
test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)


article = "Within hours of the storm, Dowdall had declared a state of emergency and brought in Essa Township emergency departments staff, as well Simcoe County administrators, to assist the 300 people displaced by the storm."
expected_reports = []
expected_reports.append(Report(['Essa Township', 'Simcoe County'], [], 'displace', 'people', 300, ''))
test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)

article = "BEIJING, March 31 (Xinhua) -- The Ministry of Civil Affairs has sent 1,000 tents, 2,000 sleeping bags, 2,000 folding beds and 1,000 sets of folding desks and chairs to Jianhe County in southwestern Guizhou Province after it was hit by a 5.5-magnitude earthquake on Monday morning.  No deaths have been reported, though the quake was Guizhou's biggest in terms of magnitude since 1949. More than 23,000 people have been affected and 2,536 relocated.  Provincial authorities have sent teams to help with the rescue work and allocated 1 million yuan (about 162,880 U.S. dollars) and 206 tents for disaster relief."
expected_reports = []
expected_reports.append(Report(['Guizhou'], ['Monday'], 'relocate', 'person', '2,536', ''))
expected_reports.append(Report(['Guizhou'], ['Monday'], 'affect', 'people', '23,000', ''))
test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)

article = 'As many as 2,214 households have been affected by the rainstorms in Rio Grande do Sul, the Emergency Management Service reported today (Dec. 28). A total of 1,964 households were displaced. The storms hit forty municipalities.  According to the government of Rio Grande do Sul, the State Coordination for Emergency Management continues to monitor and provide assistance to the impacted municipalities and communities.  Last Saturday (26), President Rousseff flew over the region, which borders Argentina and Uruguay, and announced the provision of $6.6 million to help communities hit by the floods.  This has been the fifth flood this year in the state, and the most severe. The Quaraí river rose a record 15.28 meters. The situation got even worse with the rise of the Uruguay river.  The rainstorm has disrupted rice harvest in the municipality of Quaraí and caused the Quaraí-Artigas international bridge between Brazil and Uruguay to remain closed off for 22 hours.    Translated by Mayra Borges'
expected_reports = []
expected_reports.append(Report(['Rio Grande do Sul'], ['Dec. 28'], 'displace', 'household', '1,964', ''))
expected_reports.append(Report(['Rio Grande do Sul'], ['Dec. 28'], 'affect', 'household', '2,214', ''))
test_outcome = test_fact_extraction(article, expected_reports)
outcomes.append(test_outcome)


test_results = "".join([outcome_map[o] for o in outcomes])
print("\n")
print(test_results)

if sum(outcomes) == 0:
    print("All tests passed!")
else:
    print("{} of {} tests failed.".format(sum(outcomes), len(outcomes)))
