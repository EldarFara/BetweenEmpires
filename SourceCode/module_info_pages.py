####################################################################################################################
#  Each quest record contains the following fields:
#  1) Info page id: used for referencing info pages in other files. The prefix ip_ is automatically added before each info page id.
#  2) Info page name: Name displayed in the info page screen.
#
####################################################################################################################

info_pages = [
 ("economics", "Economics in Between Empires", "Economical information of regions is available in region menu, that can be opened in town/castle menu.^\
Economical information of certain resources and factions is shown in resource menu, which can be opened from region menu described above.^\
^\
Each region has it's characteristics:^\
GDP - sum of cost of all resources produced in the region. Affects region development.^\
Population - affects number of workers available in production, grows with time depending on healthcare expenses. Decreased by famine and battle casualties.^\
Literacy - insignificantly increases production output in villages, as well as political activity increasing speed, and urbanization increasing speed.^\
Urbanization - defines ratio of population in villages and cities. regions with higher value have more workers in cities, and less in villages.^\
^\
All regions produce all kinds of raw resources in villages, except for cotton, which is available only in the east and overseas. Some regions have bonus for production of one of resources, such as flour or coal, which leads to some countries producing much more resources of certain type than others.^\
^\
Towns and castles have fixed amount of factory slots (6 and 3 respectively). Factories are built by the population (depending on GDP value) and by player, with speed of building being dependant on region GDP amount. Each factory has characteristics:^\
Workers amount: affects production size.^\
Maximum workers amount: defines maximum amount of workers that factory can hire, can be increased by development mode. Can be decresed during riots.^\
Quality of product: value depends on other characteristics, defines how attractive product is for sellers. Effective only if there is big supply of this resource in the market.^\
Machine tools deterioration: increases with time, decreased by development mode. Affects produciton output and quality of product.^\
Engineers percentage: depends on region literacy, affects quality of product.^\
Workers wage: depends on factory owner choice, does inrease spending but also does increase quality of product and quality of life in the region.^\
Working conditions: decreases with time, increased by development mode. Increases quality of product and quality of life in the region.^\
^\
Development mode of factory is available to player only if he owns 100% shares of factory. There are 3 development modes:^\
Incerase number of workplaces: increases maximum workers value.^\
Increase working conditions: increases working conditions value.^\
Improve tools: increases quality of product and decreases machine tools deterioration.^\
Effectiveness of development mode depends on budget amount.^\
^\
Expenses and income of factories depend on these factors:^\
Cost of raw resources that factory uses for production. It depends on workers amount and on resource price itself.^\
Workers wage amount.^\
Cost of output resources that factory produces. It depends on workers amount and on resource price itself.^\
Investitions from capitalists, size of which depends on GDP of the region.^\
Having development mode also costs 1% of budget every day.^\
^\
Resources, both urban and rural, are being bought from any region in any region worldwide, with some factors affecting selection process:^\
Home faction is prioritized.^\
Resources with higher quality of product is prioritized.^\
If foreign, factions with lower import tax are prioritized.^\
^\
Regions that do not have enough factories to occupy all urban population, has them occupied in handicraft industry. Handicraft industry is much less productive and only fulfills needs of home region."),
 ("politics", "Politics in Between Empires", "Politics menu can be opened in reports menu. If you are faction leader, you will have additional options for management of your country. Some options related to country management are also available in secretary of state dialog options.^\
^\
Each faction has political parties, political movements and 5 population classes. It also has 17 laws:^\
Voting Franchise. It defines which classes of population have right to vote, both in parliament and executive branch elections. Different vote franchise laws will result in different parliament and executive branch compositions depending on levels of parties' support of different classes.^\
Ruling Party Influence law. It defines how ruling party influences voters during elections, which can help ruling party get more votes.^\
Nomination Rules law, It defines amount of land citizen need to be able to be nominated and be voted for in parliament. Universal nomination rule will lead to lower classes having more weight in parliament and executive branch.^\
Executive Branch Elective Posts law It defines how many executive branch posts are being selected by elections.^\
Public meetings law. Allowing public meetings will inrease quality of life of population, while increasing movements popularity levels.^\
Minimum Worker Wage law. It makes factory owners to not decrease wage of workers below level defined in law, increasing quality of life of lower classes, while increasing spending of factories.^\
Maximum Work Hours law. It defines maximum amount of work hours in a day. Lower values will slighty decrease productivity of industry while increasing quality of life of lower classes.^\
Press law. It defines level of censorship in mass media. More free press will lead to ruling party having less influence and increasing quality of life of the population.^\
Trade unions law. Allowing trade unions results in higher quality of life for population, wjile also leading to factory owners funding in increasing workers conditions in their factories more often.^\
Child labour law. Putting child labour under restrictions will lead to higher quality of life, while increasing wage spendings of factories.^\
Infrastructure expenses. Higher infrastructure expenses will lead to faster development of infrastructure in all regions. and slower damaging during war.^\
Education expenses. Higher education expenses will increase speed of literacy level growing.^\
Healthcare expenses. Higher healthcare expenses will increase speed of population growing.^\
Military expenses. Higher military expenses will increase supply level of army, if supplies are available.^\
Income tax. Higher income tax will increase budget income, while decreasing wealth of population.^\
Goods and services tax. It is being imposed to sellers of any resources which are citizens of this country. Higher tax will decrease income of factories.^\
Import tax. It is being imposed to any resources being transported over this country borders. Lesser tax will increase income of factories and attract more foreign resource buyers.^\
^\
Each population class (aristocracy, bourgeoisie, middle class, lower urban class and lower rural class) has it's characteristics:^\
Political activity. Each political party and population estate has its political view on laws, i. e. laws that they want to be applied in their country. This defines amount of support for each party from each class depending on political activity. Higher political activity of class leads to more support towards parties that share same political view with them. ^\Aristocracy tends to support reactionary and conservative parties, bourgeoisie - liberal parteis, and lower estates - socialist parties, as well as liberal parties. Political activity increases gradually, but can jump up in case of popular pacifist movevment going.^\
Quality of life. It depends on laws and wealth of each class, as well as some other specific factors.^\
Wealth. Depending on different factors for each class, wealth defines quality of life. Low wealth amount in combination with low supply of flour in country can lead to famine. Higher GDP per capita and workers wage laws will lead to higher wealth.^\
Famine. High famine level leads to slower population increase, and slower urbanization growth. Mainly affects urban lower class.^\
^\
Parliament compositions is being defined by election laws and population classes support for different classes. Executive branch composition, on the other hand, depends on 3 factors, ratio of which depending on Executive Branch Elective Posts law:^\
Wealth of classes. Parties that get support from most wealthy classes get more places in executive branch, except for Soviet Republic goverment type, where this factor does not apply.^\
Ruling party. Ruling party gets big number of places depending on Executive Branch Elective Posts law.^\
Elections. Depending on suffage laws, leftover places in executive branch are being distributed depending on election laws, just like parliament, according to Executive Branch Elective Posts law.^\
^\
Administration efficiency level of facction depends on executive branch composition. If it has too many party members that don't agree current state laws (for example liberal in faction with protectionist economy), administration efficiency will be lower. Low administration efficiency level leads to more income from taxes lost due to corruption.^\
^\
Political movements are reactions to political situation in country. There are 3 types of political movements:^\
Liberal movement demands establishment of parliament, universal, equal and direct suffrage and regions autonomy. Mainly supported and funded by bourgeoisie, it's popularity depends on their wealth and quality of life levels.^\
Socialist movement demands social welfare laws, which lead to governmental investment in economic development and protection of the economic rights of the lower class. It's popularity depends on lower classes quality of life levels.^\
Pacifist movement is a result of being involved in wars. It's supporters are demanding peace at any cost. It's popularity depends on success of the wars - the less successful war is, the more popularity pacifist movement has. High popularity of pacifist movement increases political activity of population, which can shift on other movements. Successful war will decrease popularity of pacifist movement.^\
^\
Each movement has characteristics:^\
Popularity level represents widespreadness of the movement in country. High popularity level will lead to mass protests in support of movement, and will raise radicalism level. Enforcing demands of movement will decrease movement popularity level.^\
Radicalism level represents willingness of movement supporters to enforce their demands with force. High level of radicalism will lead to riots and rebellions, and success of the latter can lead to revolution and civil war. Radicalism level is being increased by high popularity level and low influence of ruling party compared to influence of other parties. Enforcing demands of movement will decrease movement radicalism level.^\
^\
Each political party has influence level, which depends on various factors and makes population support them even without sharing the same political views.^\
^\
There are 4 government types:^\
Absolute monarchy. This type gives additional influence to ruling party and gives faction leader full control on laws and gives possibility to buy factories in the country and choose ruling party.^\
Constitutionl monarchy. This type gives possibility to choose ruling party, but law choosing is limited by parliament.^\
Republic. Ruling party is elected by the population.^\
Soviet republic. Despite the name, this type in mod represents authoritarian socialist government with control of laws and factories, with additional features, such as rural and urban industries nationalisation or forced urbanization available for faster industrialisation."),
]
