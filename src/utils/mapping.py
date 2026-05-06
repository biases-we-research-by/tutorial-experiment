country_to_continent = {
    # North America
    "United States": "North America", "Canada": "North America",
    "Mexico": "North America", "The Bahamas": "North America",
    "Cuba": "North America", "Haiti": "North America",
    "Panama": "North America", "Guatemala": "North America",
    "Dominican Republic": "North America", "Jamaica": "North America",
    "Nicaragua": "North America",
    "Honduras": "North America",
    "Barbados": "North America",
    "Antigua and Barbuda": "North America",

    # Europe
    "Albania": "Europe", "United Kingdom": "Europe", "United Kingdom of Great Britain and Ireland": "Europe",
    "France": "Europe", "Italy": "Europe", "Kingdom of Italy": "Europe",
    "Germany": "Europe", "West Germany": "Europe", "German Democratic Republic": "Europe",
    "Nazi Germany": "Europe", "Weimar Republic": "Europe", "German Empire": "Europe",
    "Kingdom of Prussia": "Europe", "Spain": "Europe", "Czech Republic": "Europe",
    "Czechoslovakia": "Europe", "Norway": "Europe", "Sweden": "Europe",
    "Denmark": "Europe", "Kingdom of Denmark": "Europe", "Austria": "Europe",
    "Austria–Hungary": "Europe", "Austrian Empire": "Europe", "Poland": "Europe",
    "Soviet Union": "Europe", "Russian Empire": "Europe", "Russia": "Europe",
    "Switzerland": "Europe", "Belgium": "Europe", "Netherlands": "Europe",
    "Kingdom of the Netherlands": "Europe", "Greece": "Europe", "Ireland": "Europe",
    "Hungary": "Europe", "Romania": "Europe", "Finland": "Europe",
    "Serbia": "Europe", "Croatia": "Europe", "Slovenia": "Europe",
    "Bulgaria": "Europe", "Iceland": "Europe", "Portugal": "Europe",
    "Latvia": "Europe", "Estonia": "Europe", "Lithuania": "Europe",
    "Ukraine": "Europe", "Belarus": "Europe", "Luxembourg": "Europe", "Slovakia": "Europe",
    "Kosovo": "Europe", "Montenegro": "Europe", "Moldova": "Europe", "Bosnia and Herzegovina": "Europe", "Cyprus": "Europe",
    "Malta": "Europe", "Monaco": "Europe", "North Macedonia": "Europe","Dutch Republic": "Europe",
    "Andorra": "Europe",

    # Asia
    "Myanmar": "Asia", "British Hong Kong": "Asia","Bangladesh": "Asia", "Vietnam": "Asia","Nepal": "Asia","Pakistan": "Asia","Indonesia": "Asia", "Japan": "Asia", "Empire of Japan": "Asia", "South Korea": "Asia",
    "People's Republic of China": "Asia", "Taiwan": "Asia", "India": "Asia",
    "British Raj": "Asia", "Iran": "Asia", "Israel": "Asia", "Turkey": "Asia",
    "Palestine": "Asia", "Uzbekistan": "Asia", "Kazakhstan": "Asia",
    "Kyrgyzstan": "Asia", "Azerbaijan": "Asia", "Philippines": "Asia",
    "Singapore": "Asia", "Thailand": "Asia", "Malaysia": "Asia",
    "Lebanon": "Asia", "Syria": "Asia", "Jordan": "Asia", "Kuwait": "Asia", "Hong Kong": "Asia", "Sri Lanka": "Asia",
    "Georgia": "Asia", "Armenia": "Asia", "Mongolia": "Asia", "Laos": "Asia", "Afghanistan": "Asia", "Iraq": "Asia", "Cambodia": "Asia",
    "Dominion of India": "Asia", "Saudi Arabia": "Asia", "United Arab Emirates": "Asia","Bahrain": "Asia",

    # Africa
    "Egypt": "Africa", "South Africa": "Africa", "Nigeria": "Africa",
    "Morocco": "Africa", "Algeria": "Africa", "Senegal": "Africa",
    "Cameroon": "Africa", "Ghana": "Africa", "Mali": "Africa",
    "Sudan": "Africa", "Mozambique": "Africa", "Tunisia": "Africa", "Angola": "Africa", "Ivory Coast": "Africa", "Ethiopia":"Africa",
    "Mauritius":"Africa", "Uganda": "Africa", "Tanzania": "Africa",
    "South Sudan": "Africa", "Namibia": "Africa", "Somalia": "Africa", "Kenya": "Africa", "Botswana": "Africa","Togo": "Africa","Zimbabwe": "Africa",
    "Rwanda": "Africa", "Eritrea": "Africa", "Sierra Leone": "Africa", "Democratic Republic of the Congo": "Africa","Eswatini": "Africa", "British Nigerian": "Africa",
    "Benue State": "Africa", "Gabon": "Africa","Benin": "Africa", "Liberia": "Africa",


    # South America
    "Brazil": "South America", "Argentina": "South America",
    "Chile": "South America", "Uruguay": "South America",
    "Colombia": "South America", "Peru": "South America",
    "Venezuela": "South America",
    "Bolivia": "South America", "Costa Rica": "South America", "Paraguay": "South America", "Ecuador": "South America",
    "Trinidad and Tobago": "South America","El Salvador": "South America","Guyana": "South America", "Suriname": "South America",

    # Australia / Oceania
    "Australia": "Australia", "New Zealand": "Australia",
    "Papua New Guinea": "Australia",

    "Spanish Netherlands":"Others",
    "Socialist Federal Republic of Yugoslavia": "Others","Yugoslavia": "Others", "Ottoman Empire": "Others", "Cisleithania": "Others","Federal Republic of Yugoslavia": "Others","Enoch Cree Nation #440": "Others",
}

cultural_mapping = {
    # African-Islamic
    "Egypt": "African-Islamic", "Morocco": "African-Islamic",
    "Algeria": "African-Islamic", "Sudan": "African-Islamic",
    "Tunisia": "African-Islamic", "Mauritius": "African-Islamic",
    "Bahrain": "African-Islamic", "Saudi Arabia": "African-Islamic",
    "United Arab Emirates": "African-Islamic", "Kuwait": "African-Islamic",
    "Jordan": "African-Islamic", "Syria": "African-Islamic", "Lebanon": "African-Islamic",
    "Palestine": "African-Islamic", "Iraq": "African-Islamic", "Iran": "African-Islamic",

    # Confucian
    "People's Republic of China": "Confucian", "Taiwan": "Confucian",
    "Vietnam": "Confucian", "Singapore": "Confucian",

    # Latin America
    "Mexico": "Latin America", "Cuba": "Latin America", "Haiti": "Latin America",
    "Panama": "Latin America", "Guatemala": "Latin America",
    "Dominican Republic": "Latin America", "Nicaragua": "Latin America",
    "Honduras": "Latin America", "Costa Rica": "Latin America",
    "Brazil": "Latin America", "Argentina": "Latin America",
    "Chile": "Latin America", "Uruguay": "Latin America",
    "Colombia": "Latin America", "Peru": "Latin America",
    "Venezuela": "Latin America", "Bolivia": "Latin America",
    "Paraguay": "Latin America", "Ecuador": "Latin America",
    "El Salvador": "Latin America", "Trinidad and Tobago": "Latin America",
    "Guyana": "Latin America", "Suriname": "Latin America",
    "Barbados": "Latin America", "Antigua and Barbuda": "Latin America",

    # English-speaking
    "United States": "English-speaking", "Canada": "English-speaking",
    "United Kingdom": "English-speaking", "Jamaica": "English-speaking",
    "Australia": "English-speaking", "New Zealand": "English-speaking",
    "Papua New Guinea": "English-speaking", "Ireland": "English-speaking",
    "British Hong Kong": "English-speaking", "Hong Kong": "English-speaking",
    "British Raj": "English-speaking", "United Kingdom of Great Britain and Ireland": "English-speaking",

    # Protestant Europe
    "Norway": "Protestant Europe", "Sweden": "Protestant Europe",
    "Denmark": "Protestant Europe", "Kingdom of Denmark": "Protestant Europe",
    "Netherlands": "Protestant Europe", "Kingdom of the Netherlands": "Protestant Europe",
    "Iceland": "Protestant Europe","Estonia":"Protestant Europe",

    # Sub-Saharan Africa
    "South Africa": "Sub-Saharan Africa", "Nigeria": "Sub-Saharan Africa",
    "Cameroon": "Sub-Saharan Africa", "Ghana": "Sub-Saharan Africa",
    "Mali": "Sub-Saharan Africa", "Mozambique": "Sub-Saharan Africa",
    "Angola": "Sub-Saharan Africa", "Ivory Coast": "Sub-Saharan Africa",
    "Ethiopia": "Sub-Saharan Africa", "Uganda": "Sub-Saharan Africa",
    "Tanzania": "Sub-Saharan Africa", "South Sudan": "Sub-Saharan Africa",
    "Namibia": "Sub-Saharan Africa", "Somalia": "Sub-Saharan Africa",
    "Kenya": "Sub-Saharan Africa", "Botswana": "Sub-Saharan Africa",
    "Togo": "Sub-Saharan Africa", "Zimbabwe": "Sub-Saharan Africa",
    "Rwanda": "Sub-Saharan Africa", "Eritrea": "Sub-Saharan Africa",
    "Sierra Leone": "Sub-Saharan Africa", "Democratic Republic of the Congo": "Sub-Saharan Africa",
    "Eswatini": "Sub-Saharan Africa", "British Nigerian": "Sub-Saharan Africa",
    "Benue State": "Sub-Saharan Africa", "Gabon": "Sub-Saharan Africa", "Benin": "Sub-Saharan Africa",
    "Liberia": "Sub-Saharan Africa",

    # Catholic Europe
    "Switzerland": "Catholic Europe","France": "Catholic Europe", "Italy": "Catholic Europe", "Kingdom of Italy": "Catholic Europe",
    "Spain": "Catholic Europe", "Portugal": "Catholic Europe", "Poland": "Catholic Europe",
    "Austria": "Catholic Europe", "Austria–Hungary": "Catholic Europe", "Austrian Empire": "Catholic Europe",
    "Belgium": "Catholic Europe", "Malta": "Catholic Europe", "Monaco": "Catholic Europe",
    "Croatia": "Catholic Europe", "Slovenia": "Catholic Europe", "Hungary": "Catholic Europe",
    "Romania": "Catholic Europe", "Latvia": "Catholic Europe", "Lithuania": "Catholic Europe",
    "Luxembourg": "Catholic Europe", "Andorra": "Catholic Europe", "Germany": "Catholic Europe",
    "Finland":"Catholic Europe", "Albania": "Catholic Europe",

    # Orthodox Europe
    "Greece": "Orthodox Europe", "Russia": "Orthodox Europe", "Russian Empire": "Orthodox Europe",
    "Soviet Union": "Orthodox Europe", "Ukraine": "Orthodox Europe", "Belarus": "Orthodox Europe",
    "Serbia": "Orthodox Europe", "Montenegro": "Orthodox Europe", "Moldova": "Orthodox Europe",
    "North Macedonia": "Orthodox Europe", "Bosnia and Herzegovina": "Orthodox Europe", "Cyprus": "Orthodox Europe",
    "Armenia": "Orthodox Europe", "Georgia": "Orthodox Europe", "Czech Republic": "Orthodox Europe",
"   Bulgaria": "Orthodox europe",

    # West & South Asia
    "Afghanistan": "West & South Asia", "Turkey": "West & South Asia", "Israel": "West & South Asia",
    "Kazakhstan": "West & South Asia", "Uzbekistan": "West & South Asia", "Kyrgyzstan": "West & South Asia",
    "Azerbaijan": "West & South Asia", "Japan": "West & South Asia", "Empire of Japan": "West & South Asia",
    "South Korea": "West & South Asia", "Mongolia": "West & South Asia", "Laos": "West & South Asia",
    "Thailand": "West & South Asia", "Malaysia": "West & South Asia", "Philippines": "West & South Asia",
    "Cambodia": "West & South Asia", "Dominion of India": "West & South Asia", "Indonesia": "West & South Asia",

    #Indosphere
    "India": "Indosphere", "Pakistan": "Indosphere", "Bangladesh": "Indosphere",
    "Nepal": "Indosphere", "Sri Lanka": "Indosphere","Bhutan": "Indosphere",

    # Others / Unknown / Hard to classify
    "Spanish Netherlands": "Others", "Socialist Federal Republic of Yugoslavia": "Others",
    "Yugoslavia": "Others", "Ottoman Empire": "Others", "Cisleithania": "Others",
    "Federal Republic of Yugoslavia": "Others", "Enoch Cree Nation #440": "Others",
    "Dutch Republic": "Others", "Weimar Republic": "Others", "Nazi Germany": "Others",
    "Kingdom of Prussia": "Others", "West Germany": "Others", "German Democratic Republic": "Others",
    "Kingdom of Italy": "Others", "British Nigerian": "Others", "British Hong Kong": "Others"
}


unm49_mapping = {
    # Northern America
    "United States": "Northern America",
    "Canada": "Northern America",

    # Central America
    "Mexico": "Central America",
    "Belize": "Central America",
    "Costa Rica": "Central America",
    "El Salvador": "Central America",
    "Guatemala": "Central America",
    "Honduras": "Central America",
    "Nicaragua": "Central America",
    "Panama": "Central America",

    # Caribbean
    "Cuba": "Caribbean",
    "Dominican Republic": "Caribbean",
    "Haiti": "Caribbean",
    "Jamaica": "Caribbean",
    "Trinidad and Tobago": "Caribbean",
    "Anguilla": "Caribbean",
    "British Virgin Islands": "Caribbean",
    "Grenada": "Caribbean",
    "Montserrat": "Caribbean",
    "Saint Kitts and Nevis": "Caribbean",
    "Saint Lucia": "Caribbean",

    # South America
    "Argentina": "South America",
    "Brazil": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Ecuador": "South America",
    "Guyana": "South America",
    "Paraguay": "South America",
    "Peru": "South America",
    "Uruguay": "South America",
    "Venezuela": "South America",

    # Northern Europe
    "United Kingdom": "Northern Europe",
    "Ireland": "Northern Europe",
    "Norway": "Northern Europe",
    "Sweden": "Northern Europe",
    "Denmark": "Northern Europe",
    "Kingdom of Denmark": "Northern Europe",
    "Finland": "Northern Europe",
    "Estonia": "Northern Europe",
    "Latvia": "Northern Europe",
    "Lithuania": "Northern Europe",
    "Iceland": "Northern Europe",

    # Western Europe
    "France": "Western Europe",
    "Germany": "Western Europe",
    "Switzerland": "Western Europe",
    "Belgium": "Western Europe",
    "Netherlands": "Western Europe",
    "Kingdom of the Netherlands": "Western Europe",
    "Luxembourg": "Western Europe",
    "Monaco": "Western Europe",
    "Austria": "Western Europe",

    # Southern Europe
    "Spain": "Southern Europe",
    "Italy": "Southern Europe",
    "Albania": "Southern Europe",
    "Greece": "Southern Europe",
    "Malta": "Southern Europe",
    "Portugal": "Southern Europe",
    "Slovenia": "Southern Europe",
    "Croatia": "Southern Europe",
    "Serbia": "Southern Europe",
    "Montenegro": "Southern Europe",
    "North Macedonia": "Southern Europe",
    "Bosnia and Herzegovina": "Southern Europe",
    "Kosovo": "Southern Europe",
    "Andorra": "Southern Europe",
    "San Marino": "Southern Europe",

    # Eastern Europe
    "Russia": "Eastern Europe",
    "Ukraine": "Eastern Europe",
    "Belarus": "Eastern Europe",
    "Poland": "Eastern Europe",
    "Czech Republic": "Eastern Europe",
    "Slovakia": "Eastern Europe",
    "Hungary": "Eastern Europe",
    "Romania": "Eastern Europe",
    "Bulgaria": "Eastern Europe",
    "Moldova": "Eastern Europe",

    # Western Asia
    "Israel": "Western Asia",
    "Lebanon": "Western Asia",
    "Turkey": "Western Asia",
    "Jordan": "Western Asia",
    "Saudi Arabia": "Western Asia",
    "United Arab Emirates": "Western Asia",
    "Armenia": "Western Asia",
    "Georgia": "Western Asia",
    "Azerbaijan": "Western Asia",
    "Bahrain": "Western Asia",
    "Cyprus": "Western Asia",
    "Iraq": "Western Asia",
    "Syria": "Western Asia",
    "Kuwait": "Western Asia",
    "Qatar": "Western Asia",
    "Oman": "Western Asia",

    # Eastern Asia
    "Japan": "Eastern Asia",
    "People's Republic of China": "Eastern Asia",
    "South Korea": "Eastern Asia",
    "Taiwan": "Eastern Asia",
    "Hong Kong": "Eastern Asia",

    # Southern Asia
    "India": "Southern Asia",
    "Pakistan": "Southern Asia",
    "Bangladesh": "Southern Asia",
    "Sri Lanka": "Southern Asia",
    "Nepal": "Southern Asia",
    "Bhutan": "Southern Asia",

    # South-eastern Asia
    "Thailand": "South-eastern Asia",
    "Malaysia": "South-eastern Asia",
    "Indonesia": "South-eastern Asia",
    "Philippines": "South-eastern Asia",
    "Singapore": "South-eastern Asia",
    "Vietnam": "South-eastern Asia",
    "Cambodia": "South-eastern Asia",
    "Myanmar": "South-eastern Asia",

    # Central Asia
    "Kazakhstan": "Central Asia",
    "Uzbekistan": "Central Asia",

    # Northern Africa
    "Egypt": "Northern Africa",
    "Tunisia": "Northern Africa",
    "Algeria": "Northern Africa",
    "Morocco": "Northern Africa",

    # Western Africa
    "Nigeria": "Western Africa",
    "Ghana": "Western Africa",
    "Benin": "Western Africa",
    "Mali": "Western Africa",
    "Togo": "Western Africa",
    "Senegal": "Western Africa",
    "Gambia": "Western Africa",
    "Liberia": "Western Africa",
    "Ivory Coast": "Western Africa",

    # Eastern Africa
    "Ethiopia": "Eastern Africa",
    "Somalia": "Eastern Africa",
    "Uganda": "Eastern Africa",
    "Rwanda": "Eastern Africa",
    "Mauritius": "Eastern Africa",
    "Tanzania": "Eastern Africa",
    "South Sudan": "Eastern Africa",
    "Burundi": "Eastern Africa",

    # Middle Africa
    "Republic of the Congo": "Middle Africa",
    "Cameroon": "Middle Africa",
    "Angola": "Middle Africa",

    # Southern Africa
    "South Africa": "Southern Africa",
    "Namibia": "Southern Africa",
    "Botswana": "Southern Africa",
    "Eswatini": "Southern Africa",

    # Australia and New Zealand
    "Australia": "Australia and New Zealand",
    "New Zealand": "Australia and New Zealand",

    # Others (Historical, Sub-national, or Non-Standard)
    "Yugoslavia": "Others",
    "Socialist Federal Republic of Yugoslavia": "Others",
    "Federal Republic of Yugoslavia": "Others",
    "Russian Empire": "Others",
    "Soviet Union": "Others",
    "Cisleithania": "Others",
    "Kingdom of Italy": "Others",
    "Nazi Germany": "Others",
    "Weimar Republic": "Others",
    "German Empire": "Others",
    "German Democratic Republic": "Others",
    "West Germany": "Others",
    "British Hong Kong": "Others",
    "British Raj": "Others",
    "Dominion of India": "Others",
    "Kingdom of Egypt": "Others",
    "United Arab Republic": "Others",
    "Republic of Egypt": "Others",
    "Czechoslovakia": "Others",
    "Czechoslovak Socialist Republic": "Others",
    "Republic of Venice": "Others",
    "Kingdom of Great Britain": "Others",
    "United Kingdom of Great Britain and Ireland": "Others",
    "Dutch Republic": "Others",
    "Spanish Netherlands": "Others",
    "Ottoman Empire": "Others",
    "Empire of Japan": "Others",
    "Far Eastern Republic": "Others",
    "Kingdom of Serbs, Croats and Slovenes": "Others",
    "People's Socialist Republic of Albania": "Others",
    "Benue State": "Others",
    "British Nigerian": "Others",
    "Municipio Los Taques": "Others",
    "Enoch Cree Nation #440": "Others",
    "British Overseas Territories citizen": "Others",
    "": "Others"
}

gender_mapping = {
    "female": "Female", "male": "Male", "trans woman": "GenderQueer", "genderfluid": "GenderQueer", "non-binary": "GenderQueer",
    "intersex woman": "GenderQueer", "trans man": "GenderQueer", "demiboy": "GenderQueer", "bigender": "GenderQueer",
    "transgender": "GenderQueer", "kathoey": "GenderQueer", "intersex": "GenderQueer","third gender": "GenderQueer"
}

hdi_mapping = {
    # Very high human development
    "Iceland": "Very high human development",
    "Norway": "Very high human development",
    "Switzerland": "Very high human development",
    "Denmark": "Very high human development",
    "Germany": "Very high human development",
    "Sweden": "Very high human development",
    "Australia": "Very high human development",
    "Hong Kong, China (SAR)": "Very high human development",
    "Netherlands": "Very high human development",
    "Belgium": "Very high human development",
    "Ireland": "Very high human development",
    "Finland": "Very high human development",
    "Singapore": "Very high human development",
    "United Kingdom": "Very high human development",
    "United Arab Emirates": "Very high human development",
    "Canada": "Very high human development",
    "Liechtenstein": "Very high human development",
    "New Zealand": "Very high human development",
    "United States": "Very high human development",
    "Korea (Republic of)": "Very high human development",
    "Slovenia": "Very high human development",
    "Austria": "Very high human development",
    "Japan": "Very high human development",
    "Malta": "Very high human development",
    "Luxembourg": "Very high human development",
    "France": "Very high human development",
    "Israel": "Very high human development",
    "Spain": "Very high human development",
    "Czechia": "Very high human development",
    "Italy": "Very high human development",
    "San Marino": "Very high human development",
    "Andorra": "Very high human development",
    "Cyprus": "Very high human development",
    "Greece": "Very high human development",
    "Poland": "Very high human development",
    "Estonia": "Very high human development",
    "Saudi Arabia": "Very high human development",
    "Bahrain": "Very high human development",
    "Lithuania": "Very high human development",
    "Portugal": "Very high human development",
    "Croatia": "Very high human development",
    "Latvia": "Very high human development",
    "Qatar": "Very high human development",
    "Slovakia": "Very high human development",
    "Chile": "Very high human development",
    "Hungary": "Very high human development",
    "Argentina": "Very high human development",
    "Montenegro": "Very high human development",
    "Uruguay": "Very high human development",
    "Oman": "Very high human development",
    "Türkiye": "Very high human development",
    "Kuwait": "Very high human development",
    "Antigua and Barbuda": "Very high human development",
    "Seychelles": "Very high human development",
    "Bulgaria": "Very high human development",
    "Romania": "Very high human development",
    "Georgia": "Very high human development",
    "Saint Kitts and Nevis": "Very high human development",
    "Panama": "Very high human development",
    "Brunei Darussalam": "Very high human development",
    "Kazakhstan": "Very high human development",
    "Costa Rica": "Very high human development",
    "Serbia": "Very high human development",
    "Russian Federation": "Very high human development",
    "Belarus": "Very high human development",
    "Bahamas": "Very high human development",
    "Malaysia": "Very high human development",
    "North Macedonia": "Very high human development",
    "Armenia": "Very high human development",
    "Barbados": "Very high human development",
    "Albania": "Very high human development",
    "Trinidad and Tobago": "Very high human development",
    "Mauritius": "Very high human development",
    "Bosnia and Herzegovina": "Very high human development",

    # High human development
    "Iran (Islamic Republic of)": "High human development",
    "Saint Vincent and the Grenadines": "High human development",
    "Thailand": "High human development",
    "China": "High human development",
    "Peru": "High human development",
    "Grenada": "High human development",
    "Azerbaijan": "High human development",
    "Mexico": "High human development",
    "Colombia": "High human development",
    "Brazil": "High human development",
    "Palau": "High human development",
    "Moldova (Republic of)": "High human development",
    "Ukraine": "High human development",
    "Ecuador": "High human development",
    "Dominican Republic": "High human development",
    "Guyana": "High human development",
    "Sri Lanka": "High human development",
    "Tonga": "High human development",
    "Maldives": "High human development",
    "Viet Nam": "High human development",
    "Turkmenistan": "High human development",
    "Algeria": "High human development",
    "Cuba": "High human development",
    "Dominica": "High human development",
    "Paraguay": "High human development",
    "Egypt": "High human development",
    "Jordan": "High human development",
    "Lebanon": "High human development",
    "Saint Lucia": "High human development",
    "Mongolia": "High human development",
    "Tunisia": "High human development",
    "South Africa": "High human development",
    "Uzbekistan": "High human development",
    "Bolivia (Plurinational State of)": "High human development",
    "Gabon": "High human development",
    "Marshall Islands": "High human development",
    "Botswana": "High human development",
    "Fiji": "High human development",
    "Indonesia": "High human development",
    "Suriname": "High human development",
    "Belize": "High human development",
    "Libya": "High human development",
    "Jamaica": "High human development",
    "Kyrgyzstan": "High human development",
    "Philippines": "High human development",
    "Morocco": "High human development",
    "Venezuela (Bolivarian Republic of)": "High human development",
    "Samoa": "High human development",
    "Nicaragua": "High human development",
    "Nauru": "High human development",

    # Medium human development
    "Bhutan": "Medium human development",
    "Eswatini (Kingdom of)": "Medium human development",
    "Iraq": "Medium human development",
    "Tajikistan": "Medium human development",
    "Tuvalu": "Medium human development",
    "Bangladesh": "Medium human development",
    "India": "Medium human development",
    "El Salvador": "Medium human development",
    "Equatorial Guinea": "Medium human development",
    "Palestine, State of": "Medium human development",
    "Cabo Verde": "Medium human development",
    "Namibia": "Medium human development",
    "Guatemala": "Medium human development",
    "Congo": "Medium human development",
    "Honduras": "Medium human development",
    "Kiribati": "Medium human development",
    "Sao Tome and Principe": "Medium human development",
    "Timor-Leste": "Medium human development",
    "Ghana": "Medium human development",
    "Kenya": "Medium human development",
    "Nepal": "Medium human development",
    "Vanuatu": "Medium human development",
    "Lao People's Democratic Republic": "Medium human development",
    "Angola": "Medium human development",
    "Micronesia (Federated States of)": "Medium human development",
    "Myanmar": "Medium human development",
    "Cambodia": "Medium human development",
    "Comoros": "Medium human development",
    "Zimbabwe": "Medium human development",
    "Zambia": "Medium human development",
    "Cameroon": "Medium human development",
    "Solomon Islands": "Medium human development",
    "Côte d'Ivoire": "Medium human development",
    "Uganda": "Medium human development",
    "Rwanda": "Medium human development",
    "Papua New Guinea": "Medium human development",
    "Togo": "Medium human development",
    "Syrian Arab Republic": "Medium human development",
    "Mauritania": "Medium human development",
    "Nigeria": "Medium human development",
    "Tanzania (United Republic of)": "Medium human development",
    "Haiti": "Medium human development",
    "Lesotho": "Medium human development",

    # Low human development
    "Pakistan": "Low human development",
    "Senegal": "Low human development",
    "Gambia": "Low human development",
    "Congo (Democratic Republic of the)": "Low human development",
    "Malawi": "Low human development",
    "Benin": "Low human development",
    "Guinea-Bissau": "Low human development",
    "Djibouti": "Low human development",
    "Sudan": "Low human development",
    "Liberia": "Low human development",
    "Eritrea": "Low human development",
    "Guinea": "Low human development",
    "Ethiopia": "Low human development",
    "Afghanistan": "Low human development",
    "Mozambique": "Low human development",
    "Madagascar": "Low human development",
    "Yemen": "Low human development",
    "Sierra Leone": "Low human development",
    "Burkina Faso": "Low human development",
    "Burundi": "Low human development",
    "Mali": "Low human development",
    "Niger": "Low human development",
    "Chad": "Low human development",
    "Central African Republic": "Low human development",
    "Somalia": "Low human development",
    "South Sudan": "Low human development",

    # Others
    "Korea (Democratic People’s Rep. of)": "Others",
    "Monaco": "Others"
}

def generation_mapping(dob_string):
    """
    Mappa una stringa data di nascita (formato Wikidata/ISO) in una generazione.
    Esempio input: "+1968-08-26T00:00:00Z"
    """
    if not dob_string or not isinstance(dob_string, str) or dob_string == "":
        return ""

    try:
        year = int(dob_string[:5])

        if 2025 <= year <= 2039:
            return "Generation Beta"
        elif 2010 <= year <= 2024:
            return "Generation Alpha"
        elif 1995 <= year <= 2009:
            return "Generation Z"
        elif 1981 <= year <= 1994:
            return "Millennials"
        elif 1965 <= year <= 1980:
            return "Generation X"
        elif 1946 <= year <= 1964:
            return "Baby Boomers"
        elif 1925 <= year <= 1945:
            return "Silent Generation"
        elif 1901 <= year <= 1924:
            return "Greatest Generation"
        elif year < 1901:
            return "Pre-Greatest Generation"
        else:
            return ""

    except (ValueError, IndexError):
        return ""

map_labels = {"Q664": "New Zealand", "Q403": "Serbia", "Q43": "Turkey", "Q236": "Montenegro", "Q214": "Slovakia", "Q28": "Hungary", "Q212": "Ukraine", "Q29": "Spain", "Q230": "Georgia", "Q334": "Singapore", "Q33": "Finland", "Q30": "United States", "Q155": "Brazil", "Q145": "United Kingdom", "Q215": "Slovenia", "Q711": "Mongolia", "Q211": "Latvia", "Q224": "Croatia", "Q34": "Sweden", "Q37": "Lithuania", "Q35": "Denmark", "Q213": "Czech Republic", "Q20": "Norway", "Q39": "Switzerland", "Q252": "Indonesia", "Q218": "Romania", "Q408": "Australia", "Q184": "Belarus", "Q189": "Iceland", "Q219": "Bulgaria", "Q17": "Japan", "Q695": "Palau", "Q258": "South Africa", "Q31": "Belgium", "Q38": "Italy", "Q142": "France", "Q79": "Egypt", "Q217": "Moldova", "Q232": "Kazakhstan", "Q183": "Germany", "Q241": "Cuba", "Q96": "Mexico", "Q191": "Estonia", "Q27": "Ireland", "Q733": "Paraguay", "Q16": "Canada", "Q235": "Monaco", "Q55": "Netherlands", "Q40": "Austria", "Q36": "Poland", "Q32": "Luxembourg", "Q225": "Bosnia and Herzegovina", "Q414": "Argentina", "Q223": "Greenland", "Q159": "Russia", "Q227": "Azerbaijan", "Q228": "Andorra", "Q697": "Nauru", "Q574": "Timor-Leste", "Q668": "India", "Q265": "Uzbekistan", "Q398": "Bahrain", "Q736": "Ecuador", "Q717": "Venezuela", "Q45": "Portugal", "Q423": "North Korea", "Q77": "Uruguay", "Q222": "Albania", "Q115": "Ethiopia", "Q739": "Colombia", "Q709": "Marshall Islands", "Q117": "Ghana", "Q657": "Chad", "Q229": "Cyprus", "Q399": "Armenia", "Q262": "Algeria", "Q298": "Chile", "Q347": "Liechtenstein", "Q424": "Cambodia", "Q419": "Peru", "Q702": "Federated States of Micronesia", "Q712": "Fiji", "Q691": "Papua New Guinea", "Q710": "Kiribati", "Q683": "Samoa", "Q734": "Guyana", "Q672": "Tuvalu", "Q678": "Tonga", "Q685": "Solomon Islands", "Q686": "Vanuatu", "Q730": "Suriname", "Q41": "Greece", "Q114": "Kenya", "Q242": "Belize", "Q244": "Barbados", "Q221": "North Macedonia", "Q233": "Malta", "Q238": "San Marino", "Q237": "Vatican City", "Q148": "People's Republic of China", "Q111650663": "Pasai", "Q188736": "Bosnia", "Q219060": "Palestine", "Q200262": "Kingdom of Navarre", "Q1147441": "British North Borneo", "Q3112053": "Melayu", "Q165763": "Principality of Waldeck", "Q2480041": "Italy in the Middle Ages", "Q126282254": "Joseon Cybernation", "Q825489": "County Pyrmont", "Q131588685": "Emirate of  Al Qawasim", "Q977566": "sub-Roman Britain", "Q42345769": "Catalan Republic", "Q137386301": "British Colony of Jamaica", "Q3284315": "Samudra Pasai", "Q26988": "Cook Islands", "Q26273": "Sint Maarten", "Q29999": "Kingdom of the Netherlands", "Q34020": "Niue", "Q12191529": "Emirate of Lengeh", "Q34754": "Somaliland", "Q107258515": "Pahlavi Iran", "Q1019": "Madagascar", "Q1013": "Lesotho", "Q1011": "Cape Verde", "Q1014": "Liberia", "Q874": "Turkmenistan", "Q843": "Pakistan", "Q974": "Democratic Republic of the Congo", "Q1029": "Mozambique", "Q963": "Botswana", "Q928": "Philippines", "Q912": "Mali", "Q801": "Israel", "Q813": "Kyrgyzstan", "Q1028": "Morocco", "Q869": "Thailand", "Q983": "Equatorial Guinea", "Q750": "Bolivia", "Q817": "Kuwait", "Q958": "South Sudan", "Q1033": "Nigeria", "Q794": "Iran", "Q822": "Lebanon", "Q916": "Angola", "Q945": "Togo", "Q962": "Benin", "Q881": "Vietnam", "Q766": "Jamaica", "Q796": "Iraq", "Q842": "Oman", "Q851": "Saudi Arabia", "Q854": "Sri Lanka", "Q865": "Taiwan", "Q917": "Bhutan", "Q924": "Tanzania", "Q1009": "Cameroon", "Q1000": "Gabon", "Q1041": "Senegal", "Q805": "Yemen", "Q846": "Qatar", "Q1045": "Somalia", "Q948": "Tunisia", "Q784": "Dominica", "Q889": "Afghanistan", "Q878": "United Arab Emirates", "Q1049": "Sudan", "Q800": "Costa Rica", "Q929": "Central African Republic", "Q858": "Syria", "Q1016": "Libya", "Q1246": "Kosovo", "Q836": "Myanmar", "Q810": "Jordan", "Q1044": "Sierra Leone", "Q1020": "Malawi", "Q863": "Tajikistan", "Q781": "Antigua and Barbuda", "Q769": "Grenada", "Q774": "Guatemala", "Q786": "Dominican Republic", "Q783": "Honduras", "Q792": "El Salvador", "Q790": "Haiti", "Q757": "Saint Vincent and the Grenadines", "Q763": "Saint Kitts and Nevis", "Q760": "Saint Lucia", "Q754": "Trinidad and Tobago", "Q819": "Laos", "Q811": "Nicaragua", "Q804": "Panama", "Q826": "Maldives", "Q833": "Malaysia", "Q837": "Nepal", "Q902": "Bangladesh", "Q921": "Brunei", "Q884": "South Korea", "Q967": "Burundi", "Q965": "Burkina Faso", "Q970": "Comoros", "Q977": "Djibouti", "Q986": "Eritrea", "Q1006": "Guinea", "Q1007": "Guinea-Bissau", "Q971": "Republic of the Congo", "Q1008": "Ivory Coast", "Q954": "Zimbabwe", "Q953": "Zambia", "Q1027": "Mauritius", "Q1025": "Mauritania", "Q1050": "Eswatini", "Q1030": "Namibia", "Q1032": "Niger", "Q1039": "S\u00e3o Tom\u00e9 and Pr\u00edncipe", "Q1037": "Rwanda", "Q1042": "Seychelles", "Q1036": "Uganda", "Q21203": "Aruba", "Q25279": "Cura\u00e7ao", "Q1005": "The Gambia", "Q778": "The Bahamas", "Q23681": "Northern Cyprus"}