import os
import pandas as pd
import random
from utils.db_connector import DBConnector


class Datasets:
    def __init__(
        self, data_dir: str = None, config: dict = None, project_id: str = None
    ):
        self.config = config
        if not data_dir:
            self.data_dir = os.path.join(os.getcwd(), "data")
        else:
            self.data_dir = data_dir
        self.project_id = project_id
        self.db_connector = DBConnector()

    def create_dataset(self):
        self.dataset = self.db_connector.create_dataset(
            name=self.config["dataset"]["name"], projectID=self.project_id
        )

    def load_data(self):
        self.df = pd.read_csv(
            os.path.join(
                self.data_dir, f"{self.config['dataset']['name'].lower()}.csv"
            ),
            sep="\t",
            na_values=[None],
            keep_default_na=False,
        )
        print(self.df.shape)
        with self.db_connector.db.tx() as tx:
            for i in self.df.itertuples():
                self.db_connector.create_article(
                    tx=tx,
                    key=str(i.key),
                    abstract=str(i.abstract),
                    title=str(i.title),
                    doi=str(i.doi),
                    mode=str(i.mode),
                    screenedDecision=str(i.decision),
                    exclusionCriteria=str(i.exclusion_criteria),
                    reviewerCount=int(i.reviewer_count),
                    datasetID=self.dataset.DatasetID,
                )

    def get_posisitve_shots(self):
        self.positiveShots = self.db_connector.get_shots(
            self.project_id,
            self.config["configurations"]["shots"]["positive"],
            positive=True,
        )
        pshots = []
        for j in self.positiveShots:
            tmp = {}
            for i in self.config["configurations"]["features"]:
                tmp[i] = getattr(j, i.title())
            pshots.append(tmp)
        self.positiveShots = pshots
        return self.positiveShots

    def get_negative_shots(self):
        self.negativeShots = self.db_connector.get_shots(
            self.project_id,
            self.config["configurations"]["shots"]["negative"],
            positive=False,
        )
        nshots = []
        for j in self.negativeShots:
            tmp = {}
            for i in self.config["configurations"]["features"]:
                tmp[i] = getattr(j, i.title())
            nshots.append(tmp)
        self.negativeShots = nshots
        return self.negativeShots

    def get_articles(self, retries=None):
        # get all the articles
        self.articles, self.error_decisions = self.db_connector.get_task_articles(
            self.project_id, retries=retries
        )
        return self.articles, self.error_decisions

    def get_trainable_datapath(self):
        return os.path.join(self.data_dir, f"{self.config['dataset']['name']}.csv")


# {
#     "title": "",
#     "abstract": "",
#     "keyword": "",
#     "authors": "",
#     "venue": "",
#     "reference": "",
#     "bibtex": "",
# }
# self.dummy = [
#     {
#         "title": "Addressing the trade off between smells and quality when refactoring class diagrams",
#         "abstract": "Models are core artifacts of modern software engineering processes, and they are subject to evolution throughout their life cycle due to maintenance and to comply with new requirements as any other software artifact. Smells in modeling are indicators that something may be wrong within the model design. Removing the smells using refactoring usually has a positive effect on the general quality of the model. However, it could have a negative impact in some cases since it could destroy the quality wanted by stakeholders. PARMOREL is a framework that, using reinforcement learning, can automatically refactor models to comply with user preferences. The work presented in this paper extends PARMOREL to support smells detection and selective refactoring based on quality characteristics to assure only the refactoring with a positive impact is applied. We evaluated the approach on a large available public dataset to show that PARMOREL can decide which smells should be refactored to maintain and, even improve, the quality characteristics selected by the user.",
#         "keyword": " Smells, Refactoring, Quality evaluation, Reinforcement learning.",
#         "authors": "Barriga Rodriguez, Angela and Bettini, Lorenzo and Iovino, Ludovico and Rutle, Adrian and Heldal, Rogardt",
#         "venue": "The Journal of Object Technology",
#         "bibtex": "@article{article,\nauthor = {Barriga Rodriguez, Angela and Bettini, Lorenzo and Iovino, Ludovico and Rutle, Adrian and Heldal, Rogardt},\nyear = {2021},\nmonth = {01},\npages = {1:1},\ntitle = {Addressing the trade off between smells and quality when refactoring class diagrams.},\nvolume = {20},\njournal = {The Journal of Object Technology},\ndoi = {10.5381/jot.2021.20.3.a1}\n}",
#         "decision": "Included",
#     },
#     {
#         "title": "Improving model repair through experience sharing",
#         "abstract": "In model-driven software engineering, models are used in all phases of the development process. These models may get broken due to various editions throughout their life-cycle. There are already approaches that provide an automatic repair of models, however, the same issues might not have the same solutions in all contexts due to different user preferences and business policies. Personalization would enhance the usability of automatic repairs in different contexts, and by reusing the experience from previous repairs we would avoid duplicated calculations when facing similar issues. By using reinforcement learning we have achieved the repair of broken models allowing both automation and personalization of results. In this paper, we propose transfer learning to reuse the experience learned from each model repair. We have validated our approach by repairing models using different sets of personalization preferences and studying how the repair time improved when reusing the experience from each repair.",
#         "keyword": "Model Repair, Reinforcement Learning, Transfer Learning",
#         "authors": " Angela Barriga, Adrian  Rutl and Rogardt Heldal",
#         "venue": "Journal of Object Technology",
#         "bibtex": '@article{JOT:issue_2020_02/article13,\n  author = {<a href="/contents.php?query=Barriga">Angela   Barriga</a> and <a href="/contents.php?query=Rutle">Adrian   Rutle</a> and <a href="/contents.php?query=Heldal">Rogardt    Heldal</a>},\n  title = {Improving Model Repair through Experience Sharing},\n  journal = {Journal of Object Technology},\n  volume = {19},\n  number = {2},\n  issn = {1660-1769},\n  year = {2020},\n  month = jul,\n  editor = {<a href="/contents.php?query=Paige">Richard Paige</a> and <a href="/contents.php?query=Vallecillo">Antonio Vallecillo</a>},\n  note = {The 16th European Conference on Modelling Foundations and Applications (ECMFA 2020)},\n  pages = {13:1-21},\n  doi = {10.5381/jot.2020.19.2.a13},\n  url = {http://www.jot.fm/contents/issue_2020_02/article13.html}\n}',
#         "decision": "Included",
#     },
#     {
#         "title": "Toward code evolution by artificial economies ",
#         "abstract": "We have begun exploring code evolution by artificial economies. We implemented a reinforcement learning machine called Hayek2 consisting of agents, written in a machine language inspired by Ray's Tierra, that interact economically. The economic structure of Hayek2 addresses credit assignment at both the agent and meta levels. Hayek2 succeeds in evolving code to solve Blocks World problems, and has been more effective at this than our hillclimbing program and our genetic program (GP). Our hillclimber and our GP also performed well, learning algorithms as strong as a simple search program that incorporates hand-coded domain knowledge. We made efforts to optimize our hillclimbing program and it has features that may be of independent interest. Our GP using crossover performed far better than a version utilizing other macro-mutations or our hillclimber, bearing on a controversy in the genetic programming literature.",
#         "keyword": "genetic algorithms, genetic programming",
#         "authors": "Eric B. Baum and Igor Durdanovic",
#         "venue": "NEC Research Institute",
#         "bibtex": '\n@TechReport{baum:1998:tceaeTR,\n\n    author = "Eric B. Baum and Igor Durdanovic",\n    title = "Toward Code Evolution By Artificial Economies",\n    institution = "NEC Research Institute",\n    year = "1998",\n    address = "4 Independence Way, Princeto, NJ 08540, USA",\n    month = "10 " # jul,\n    keywords = "genetic algorithms, genetic programming",\n    size = "53 pages",\n    notes = "Hayek2 blocks world \'crossover is much better than headless chicken mutation\' meta-agents, inherited wealth, rent, intellectual property, strong typing STGP. See also \\cite{baum:1998:tceae}, \\cite{oai:CiteSeerPSU:5199}", \n\n}',
#         "decision": "Excluded",
#     },
#     {
#         "title": "DEVS Modeling and Simulation of Financial Leverage Effect Based on Markov Decision Process ",
#         "abstract": "Decision making during a financial asset optimization process leading to a potential leverage effect is a major issue in the management of an investment program such as European development programs. Modeling and simulation based on reinforcement learning can propose a decision-making policy in this kind of process. This paper presents a DEVS discrete-event modeling and simulation approach from Markov decision-making processes applied to the search for maximum leverage on self-financing capabilities in grant application instruction phase. The application of the approach presented in this paper is made on the search for the leverage effect linked to the price volatility of the main stock market indices (CAC40, NasDaq, etc.).",
#         "keyword": "    Mathematical model, Decision making, Indexes, Reinforcement learning, Load modeling, Integrated circuit modeling",
#         "authors": "Barbieri, E. and Capocchi, L. and Santucci, J.F.",
#         "venue": "2018 4th International Conference on Universal Village (UV)",
#         "bibtex": "@INPROCEEDINGS{8642121,\n\n  author={Barbieri, E. and Capocchi, L. and Santucci, J.F.},\n\n  booktitle={2018 4th International Conference on Universal Village (UV)}, \n\n  title={DEVS Modeling and Simulation of Financial Leverage Effect Based on Markov Decision Process}, \n\n  year={2018},\n\n  volume={},\n\n  number={},\n\n  pages={1-5},\n\n  doi={10.1109/UV.2018.8642121}}",
#         "decision": "Excluded",
#     },
#     {
#         "title": "On testing machine learning programs ",
#         "abstract": "Nowadays, we are witnessing a wide adoption of Machine learning (ML) models in many software systems. They are even being tested in safety-critical systems, thanks to recent breakthroughs in deep learning and reinforcement learning. Many people are now interacting with systems based on ML every day, e.g., voice recognition systems used by virtual personal assistants like Amazon Alexa or Google Home. As the field of ML continues to grow, we are likely to witness transformative advances in a wide range of areas, from finance, energy, to health and transportation. Given this growing importance of ML-based systems in our daily life, it is becoming utterly important to ensure their reliability. Recently, software researchget_articles()ers have started adapting concepts from the software testing domain (e.g., code coverage, mutation testing, or property-based testing) to help ML engineers detect and correct faults in ML programs. This paper reviews current existing testing practices for ML programs. First, we identify and explain challenges that should be addressed when testing ML programs. Next, we report existing solutions found in the literature for testing ML programs. Finally, we identify gaps in the literature related to the testing of ML programs and make recommendations of future research directions for the scientific community. We hope that this comprehensive review of software testing practices will help ML engineers identify the right approach to improve the reliability of their ML-based systems. We also hope that the research community will act on our proposed research directions to advance the state of the art of testing for ML programs. (C) 2020 Published by Elsevier Inc.",
#         "keyword": "Machine learning, Data cleaning, Feature engineering testing, Model testing, Implementation testing",
#         "authors": "Houssem Ben Braiek and Foutse Khomh",
#         "venue": "Journal of Systems and Software",
#         "bibtex": "@article{BRAIEK2020110542,\ntitle = {On testing machine learning programs},\njournal = {Journal of Systems and Software},\nvolume = {164},\npages = {110542},\nyear = {2020},\nissn = {0164-1212},\ndoi = {https://doi.org/10.1016/j.jss.2020.110542},\nurl = {https://www.sciencedirect.com/science/article/pii/S0164121220300248},\nauthor = {Houssem Ben Braiek and Foutse Khomh},\nkeywords = {Machine learning, Data cleaning, Feature engineering testing, Model testing, Implementation testing},\nabstract = {Nowadays, we are witnessing a wide adoption of Machine learning (ML) models in many software systems. They are even being tested in safety-critical systems, thanks to recent breakthroughs in deep learning and reinforcement learning. Many people are now interacting with systems based on ML every day, e.g., voice recognition systems used by virtual personal assistants like Amazon Alexa or Google Home. As the field of ML continues to grow, we are likely to witness transformative advances in a wide range of areas, from finance, energy, to health and transportation. Given this growing importance of ML-based systems in our daily life, it is becoming utterly important to ensure their reliability. Recently, software researchers have started adapting concepts from the software testing domain (e.g., code coverage, mutation testing, or property-based testing) to help ML engineers detect and correct faults in ML programs. This paper reviews current existing testing practices for ML programs. First, we identify and explain challenges that should be addressed when testing ML programs. Next, we report existing solutions found in the literature for testing ML programs. Finally, we identify gaps in the literature related to the testing of ML programs and make recommendations of future research directions for the scientific community. We hope that this comprehensive review of software testing practices will help ML engineers identify the right approach to improve the reliability of their ML-based systems. We also hope that the research community will act on our proposed research directions to advance the state of the art of testing for ML programs.}\n}",
#         "decision": "Excluded",
#     },
#     {
#         "title": "QFlow: A Learning Approach to High QoE Video Streaming at the Wireless Edge",
#         "abstract": "The predominant use of wireless access networks is for media streaming applications. However, current access networks treat all packets identically, and lack the agility to determine which clients are most in need of service at a given time. Software reconfigurability of networking devices has seen wide adoption, and this in turn implies that agile control policies can be now instantiated on access networks. Exploiting such reconfigurability requires the design of a system that can enable a configuration, measure the impact on the application performance (Quality of Experience), and adaptively select a new configuration. Effectively, this feedback loop is a Markov Decision Process whose parameters are unknown. The goal of this work is to develop QFlow, a platform that instantiates this feedback loop, and instantiate a variety of control policies over it. We use the popular application of video streaming over YouTube as our use case. Our context is priority queueing, with the action space being that of determining which clients should be assigned to each queue at each decision period. We first develop policies based on model-based and model-free reinforcement learning. We then design an auction-based system under which clients place bids for priority service, as well as a more structured index-based policy. Through experiments, we show how these learning-based policies on QFlow are able to select the right clients for prioritization in a high-load scenario to outperform the best known solutions with over 25\\% improvement in QoE, and a perfect QoE score of 5 over 85\\% of the time.",
#         "keyword": "Reinforcement learning , wireless edge networks , video streaming , auction mechanisms , OpenFlow",
#         "authors": "Bhattacharyya, Rajarshi and Bura, Archana and Rengarajan, Desik and Rumuly, Mason and Xia, Bainan and Shakkottai, Srinivas and Kalathil, Dileep and Mok, Ricky K. P. and Dhamdhere, Amogh",
#         "venue": "IEEE/ACM Transactions on Networking",
#         "bibtex": "@ARTICLE{9528909,\n\n  author={Bhattacharyya, Rajarshi and Bura, Archana and Rengarajan, Desik and Rumuly, Mason and Xia, Bainan and Shakkottai, Srinivas and Kalathil, Dileep and Mok, Ricky K. P. and Dhamdhere, Amogh},\n\n  journal={IEEE/ACM Transactions on Networking}, \n\n  title={QFlow: A Learning Approach to High QoE Video Streaming at the Wireless Edge}, \n\n  year={2022},\n\n  volume={30},\n\n  number={1},\n\n  pages={32-46},\n\n  doi={10.1109/TNET.2021.3106675}}",
#         "decision": "Excluded",
#     },
#     {
#         "title": "Ground Delay Program Analytics with Behavioral Cloning and Inverse Reinforcement Learning ",
#         "abstract": " Historical data are used to build two types of models that predict Ground Delay Program implementation decisions and produce insights into how and why those decisions are made. More specifically, behavioral cloning and inverse reinforcement learning models are built that predict hourly Ground Delay Program implementation at Newark Liberty International and San Francisco International airports. Data available to the models include actual and scheduled air traffic metrics and observed and forecasted weather conditions. The developed random forest models are substantially better at predicting hourly Ground Delay Program implementation for these airports than the developed inverse reinforcement learning models. However, all of the models struggle to predict the initialization and cancellation of Ground Delay Programs. The structure of the models are also investigated in order to gain insights into Ground Delay Program implementation decision making. Notably, characteristics of both types of model suggest that Ground Delay Program implementation decisions are more tactical than strategic: they are made primarily based on conditions now or conditions anticipated in only the next couple of hours.",
#         "keyword": "    Inverse Reinforcement LearningGround Delay Program Parameters Selection ModelNewark Liberty International AirportAir Traffic Flow ManagementRunway ConfigurationAirspaceWeather ForecastingPythonFederal Aviation AdministrationMarkov Decision Process",
#         "authors": "Bloem, Michael and Bambos, Nicholas",
#         "venue": "Journal of Aerospace Information Systems",
#         "bibtex": "\n@article{doi:10.2514/1.I010304,\nauthor = {Bloem, Michael and Bambos, Nicholas},\ntitle = {Ground Delay Program Analytics with Behavioral Cloning and Inverse Reinforcement Learning},\njournal = {Journal of Aerospace Information Systems},\nvolume = {12},\nnumber = {3},\npages = {299-313},\nyear = {2015},\ndoi = {10.2514/1.I010304},\n\nURL = { \n    \n        https://doi.org/10.2514/1.I010304\n    \n    \n\n},\neprint = { \n    \n        https://doi.org/10.2514/1.I010304\n    \n    \n\n}\n,\n    abstract = { Historical data are used to build two types of models that predict Ground Delay Program implementation decisions and produce insights into how and why those decisions are made. More specifically, behavioral cloning and inverse reinforcement learning models are built that predict hourly Ground Delay Program implementation at Newark Liberty International and San Francisco International airports. Data available to the models include actual and scheduled air traffic metrics and observed and forecasted weather conditions. The developed random forest models are substantially better at predicting hourly Ground Delay Program implementation for these airports than the developed inverse reinforcement learning models. However, all of the models struggle to predict the initialization and cancellation of Ground Delay Programs. The structure of the models are also investigated in order to gain insights into Ground Delay Program implementation decision making. Notably, characteristics of both types of model suggest that Ground Delay Program implementation decisions are more tactical than strategic: they are made primarily based on conditions now or conditions anticipated in only the next couple of hours. }\n}\n\n",
#         "decision": "Excluded",
#     },
#     {
#         "title": "Crypto-Deep Reinforcement Learning Based Cloud Security For Trusted Communication",
#         "abstract": "",
#         "keyword": "Side-channel attack , Multi Agent Deep reinforcement Learning Multi Agent Deep Reinforcement Learning (MADRL) , linear classification , machine learning algorithm and cloud security",
#         "authors": "Abirami, P. and Vijay Bhanu, S. and Thivakaran, T.K.",
#         "venue": "2022 4th International Conference on Smart Systems and Inventive Technology (ICSSIT)",
#         "bibtex": "@INPROCEEDINGS{9716429,\n  author={Abirami, P. and Vijay Bhanu, S. and Thivakaran, T.K.},\n  booktitle={2022 4th International Conference on Smart Systems and Inventive Technology (ICSSIT)}, \n  title={Crypto-Deep Reinforcement Learning Based Cloud Security For Trusted Communication}, \n  year={2022},\n  volume={},\n  number={},\n  pages={1-10},\n  doi={10.1109/ICSSIT53264.2022.9716429}}",
#         "decision": "Excluded",
#     },
#     {
#         "title": "Virtual Hardware-in-the-Loop FMU Co-Simulation Based Digital Twins for Heating, Ventilation, and Air-Conditioning (HVAC) Systems ",
#         "abstract": "In this paper, a novel self-adaptive control method based on a digital twin is developed and investigated for a multi-input multi-output (MIMO) nonlinear system, which is a heating, ventilation, and air-conditioning system. For this purpose, hardware-in-loop (HIL) and software-in-loop (SIL) are integrated to develop the digital twin control concept in a straightforward manner. A nonlinear integral backstepping (NIB) model-free control technique is integrated with the HIL (implemented as a physical controller) and SIL (implemented as a virtual controller) controllers to control the HVAC system without the need for dynamic feature identification. The main goal is to design the virtual controller to minimize the distinction between system outputs in the SIL and HIL setups. For this purpose, Deep Reinforcement Learning (DRL) is applied to update the NIB controller coefficients of the virtual controller based on the measured data of the physical controller. Since the temperature and humidity of HVAC systems should be regulated, the NIB controllers in the HIL and SIL are designed by the DRL algorithm in a multi-objective scheme (MO). In particular, the simulations of the HIL and SIL environments are coupled by a new advanced tool: function mockup interface (FMI) standard. The Functional Mock-up Unit (FMU) is adopted into the FMI interface for data exchange. The extensive research of HIL and SIL controllers shows that the system outputs of the virtual controller are controlled exactly according to the physical controller.",
#         "keyword": "Heating , ventilating and air-conditioning (HVAC) , deep reinforcement learning (DRL) , nonlinear integral-backstepping (NIB) , digital twin , hardware-in-loop (HIL)",
#         "authors": "Abrazeh, Saber and Mohseni, Saeid-Reza and Zeitouni, Meisam Jahanshahi and Parvaresh, Ahmad and Fathollahi, Arman and Gheisarnejad, Meysam and Khooban, Mohammad-Hassan",
#         "venue": "IEEE Transactions on Emerging Topics in Computational Intelligence",
#         "bibtex": "@ARTICLE{9782098,\n  author={Abrazeh, Saber and Mohseni, Saeid-Reza and Zeitouni, Meisam Jahanshahi and Parvaresh, Ahmad and Fathollahi, Arman and Gheisarnejad, Meysam and Khooban, Mohammad-Hassan},\n  journal={IEEE Transactions on Emerging Topics in Computational Intelligence}, \n  title={Virtual Hardware-in-the-Loop FMU Co-Simulation Based Digital Twins for Heating, Ventilation, and Air-Conditioning (HVAC) Systems}, \n  year={2023},\n  volume={7},\n  number={1},\n  pages={65-75},\n  doi={10.1109/TETCI.2022.3168507}}",
#         "decision": "Excluded",
#     },
#     {
#         "title": "Interest forwarding strategy in Named Data Networks (NDN) using Thompson Sampling",
#         "abstract": "",
#         "keyword": "forwarding, Receiver-driven, Source-driven, Reinforcement learning, Scoped-flooding",
#         "authors": "Nazma Akther and Kingshuk Dhar and Shahid Md. Asif Iqbal and Mohammed Nurul Huda and  Asaduzzaman",
#         "venue": "Journal of Network and Computer Applications",
#         "bibtex": "@article{AKTHER2022103458,\ntitle = {Interest forwarding strategy in Named Data Networks (NDN) using Thompson Sampling},\njournal = {Journal of Network and Computer Applications},\nvolume = {205},\npages = {103458},\nyear = {2022},\nissn = {1084-8045},\ndoi = {https://doi.org/10.1016/j.jnca.2022.103458},\nurl = {https://www.sciencedirect.com/science/article/pii/S1084804522001084},\nauthor = {Nazma Akther and Kingshuk Dhar and Shahid Md. Asif Iqbal and Mohammed Nurul Huda and  Asaduzzaman},\nkeywords = { forwarding, Receiver-driven, Source-driven, Reinforcement learning, Scoped-flooding},\nabstract = {Optimizing Interest forwarding and Data delivery has been among the top dissected problems in NDN for the last decade; however, only a few contributions thrive to minimize communication cost and delay concurrently. In NDN, a receiver-driven forwarding strategy is considered resource-consuming as the routers incur computation to find the best path to the desired item, specified by an Interest’s name. On the other hand, a source-driven forwarding strategy, a scheme that suppresses the sub-optimal sources, experiences increased delay when no source answers in the exploration phase. The confluence of the two strategies can counteract the drawbacks of each one, which, however, has never been investigated. In this work, a reinforcement learning-based, namely Thompson Sampling, strategy is proposed that operates in a receiver-cum-source-driven fashion to optimize Interest forwarding and answering. The proposed method introduces a ’Beam’ concept coupled with adaptive scoped-flooding to optimize Interest forwarding, and the sources adopt Thompson Sampling to suppress the sub-optimal responses. When hit by an Interest, an optimal source sends back the desired Data to the consumer whereas a sub-optimal source remains Silent. Together, the ’Beam’ and the scoped-flooding adapt the Interest forwarding range based on cache hit/miss ratio. The adaptation optimizes communication cost and delay, and contributes to scheming the proposed strategy resource-savvy. The proof-of-concept implementation in software (simulation) reveals that the proposed system outperforms the counterpart benchmarks by reducing the communication costs and delay in NDN (by around 350% and 10%, respectively) without negotiating packet delivery ratio.}\n}",
#         "decision": "Excluded",
#     },
# ]
# self.posisitveShots = [k for k in self.dummy[1:] if k["decision"] == "Included"]
# self.negativeShots = [k for k in self.dummy[1:] if k["decision"] == "Excluded"]
# self.article = self.dummy[0]
# for i in self.dummy:
#     i.pop("decision")
