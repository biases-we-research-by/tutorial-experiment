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