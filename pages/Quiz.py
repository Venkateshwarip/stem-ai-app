import streamlit as st
import sqlite3
import random
from utils.theme import apply_theme
apply_theme()
st.set_page_config(page_title="AI STEM Tutor", layout="wide")
apply_theme()


# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Topic-wise Quiz", layout="wide")

# ------------------ ENSURE TOPIC IS SELECTED ------------------
if "quiz_topic" not in st.session_state:
    st.error("Please select a topic from Study Material page.")
    st.stop()

raw_topic = st.session_state["quiz_topic"].strip().lower()

# ------------------ TOPIC MAPPING ------------------
TOPIC_MAP = {
    "control flow": "Control Flow",
    "data structures": "Data Structures",
    "oops concepts": "OOPs Concepts",
    "exception handling": "Exception Handling",
    "file handling": "File Handling",

    # 🔬 NEW SCIENCE PYTHON TOPICS
    "python biology": "Python Biology",
    "python botany": "Python Botany",
    "python chemistry": "Python Chemistry",
    "python maths": "Mathematics",
    "python physics": "Python Physics",
    "python zoology": "Python Zoology",

    # EXISTING
    "mathematics": "Mathematics",
}

quiz_topic = TOPIC_MAP.get(raw_topic)
if not quiz_topic:
    st.error("Invalid topic selected.")
    st.stop()

# ------------------ DATABASE ------------------
conn = sqlite3.connect("tutor.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    topic TEXT,
    score INTEGER,
    total INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# ------------------ HEADER ------------------
st.title("📝 Topic-wise Quiz")
st.subheader(f"📘 Topic: {quiz_topic}")
st.markdown("**20 MCQs | 1 Mark Each**")
st.divider()

# ======================================================
# ✅ RESET QUESTIONS WHEN TOPIC CHANGES (IMPORTANT FIX)
# ======================================================
if "last_quiz_topic" not in st.session_state:
    st.session_state.last_quiz_topic = quiz_topic

if st.session_state.last_quiz_topic != quiz_topic:
    st.session_state.pop("quiz_questions", None)
    st.session_state.pop("user_answers", None)
    st.session_state.last_quiz_topic = quiz_topic

# ------------------ QUESTION BANK ------------------
QUESTION_BANK = {
    "Control Flow": [
        ("Which keyword is used for decision making?", ["if", "for", "while", "def"], "if"),
        ("Which loop executes at least once?", ["for", "while", "do-while", "None"], "do-while"),
        ("Which exits a loop?", ["stop", "exit", "break", "pass"], "break"),
        ("Which skips current iteration?", ["continue", "break", "pass", "skip"], "continue"),
        ("elif means?", ["else if", "end if", "else loop", "none"], "else if"),
        ("Python block defined by?", ["Braces", "Indentation", "Semicolon", "Keywords"], "Indentation"),
        ("Infinite loop example?", ["while True", "for i", "if True", "loop"], "while True"),
        ("Used to do nothing?", ["pass", "continue", "break", "skip"], "pass"),
        ("Which is conditional?", ["for", "while", "if", "def"], "if"),
        ("Which repeats fixed times?", ["for", "while", "if", "elif"], "for"),
        ("Logical AND operator?", ["&&", "and", "&", "AND"], "and"),
        ("Logical OR operator?", ["||", "or", "|", "OR"], "or"),
        ("Compare equal?", ["=", "==", "!=", "<="], "=="),
        ("Not equal operator?", ["!", "!=", "<>", "not"], "!="),
        ("Terminate program?", ["exit()", "stop()", "end()", "quit"], "exit()"),
        ("Nested if means?", ["if inside if", "loop", "function", "class"], "if inside if"),
        ("Used for range loop?", ["range()", "list()", "loop()", "count()"], "range()"),
        ("Reverse loop?", ["range(10,0,-1)", "reverse()", "flip()", "back()"], "range(10,0,-1)"),
        ("Boolean values?", ["1,0", "yes,no", "True, False", "on,off"], "True, False"),
        ("Conditional operator?", ["?:", "if else", "switch", "select"], "if else"),
    ],

    "OOPs Concepts": [
        ("Class is?", ["Object", "Blueprint", "Method", "Variable"], "Blueprint"),
        ("Object is?", ["Class", "Instance", "Method", "Function"], "Instance"),
        ("Constructor name?", ["init", "__init__", "create", "start"], "__init__"),
        ("self refers to?", ["Class", "Object", "Module", "Function"], "Object"),
        ("Encapsulation means?", ["Binding data", "Hiding data", "Copy data", "Sharing"], "Hiding data"),
        ("Inheritance provides?", ["Speed", "Memory", "Reusability", "Security"], "Reusability"),
        ("Polymorphism means?", ["Many forms", "One form", "Two forms", "None"], "Many forms"),
        ("Private variable prefix?", ["_", "__", "#", "$"], "__"),
        ("Protected prefix?", ["_", "__", "#", "$"], "_"),
        ("Default access?", ["Public", "Private", "Protected", "Hidden"], "Public"),
        ("Which supports multiple inheritance?", ["Python", "C", "Java", "C#"], "Python"),
        ("Base class keyword?", ["parent", "super", "base", "this"], "super"),
        ("Method overriding means?", ["Same name method", "New method", "Delete method", "None"], "Same name method"),
        ("Abstraction hides?", ["Code", "Logic", "Implementation", "Data"], "Implementation"),
        ("Abstract class module?", ["abc", "os", "sys", "math"], "abc"),
        ("Decorator for abstract method?", ["@abstractmethod", "@abstract", "@method", "@override"], "@abstractmethod"),
        ("isinstance() checks?", ["Type", "Value", "Object", "Size"], "Object"),
        ("type() returns?", ["Type", "Value", "Name", "Id"], "Type"),
        ("Object creation uses?", ["class", "new", "()", "create"], "()"),
        ("Data + Methods together?", ["Encapsulation", "Inheritance", "Abstraction", "Polymorphism"], "Encapsulation"),
    ],

    "Data Structures": [
        ("Which is LIFO?", ["Stack", "Queue", "List", "Array"], "Stack"),
        ("FIFO structure?", ["Queue", "Stack", "List", "Array"], "Queue"),
        ("Dynamic array in Python?", ["list", "array", "tuple", "dict"], "list"),
        ("Immutable sequence?", ["tuple", "list", "set", "dict"], "tuple"),
        ("Dictionary key-value type?", ["dict", "list", "tuple", "set"], "dict"),
        ("Add element to set?", ["add()", "append()", "insert()", "extend()"], "add()"),
        ("Pop from stack?", ["pop()", "remove()", "del()", "discard()"], "pop()"),
        ("Remove from queue?", ["dequeue()", "pop()", "remove()", "delete()"], "dequeue()"),
        ("Access first element of list?", ["list[0]", "list[1]", "list[-1]", "list.first"], "list[0]"),
        ("Sort list?", ["sort()", "sorted()", "order()", "arrange()"], "sort()"),
        ("Immutable mapping?", ["frozenset", "dict", "list", "tuple"], "frozenset"),
        ("Insert in middle of list?", ["insert()", "append()", "extend()", "add()"], "insert()"),
        ("Length of list?", ["len()", "count()", "size()", "length()"], "len()"),
        ("Combine lists?", ["extend()", "append()", "+", "add()"], "extend()"),
        ("Dictionary keys?", ["keys()", "values()", "items()", "all()"], "keys()"),
        ("Dictionary values?", ["values()", "keys()", "items()", "all()"], "values()"),
        ("Queue using list method?", ["append + pop(0)", "append + pop()", "insert + pop()", "insert + remove()"], "append + pop(0)"),
        ("Stack using list method?", ["append + pop()", "append + pop(0)", "insert + pop()", "insert + remove()"], "append + pop()"),
        ("Set removes duplicates?", ["True", "False", "Maybe", "None"], "True"),
        ("Check element in set?", ["in", "contains", "has", "exists"], "in"),
    ],

    "Exception Handling": [
        ("Catch exception?", ["try-except", "catch", "try-catch", "handle"], "try-except"),
        ("Finally block runs?", ["Always", "Sometimes", "Never", "On Error"], "Always"),
        ("Raise exception?", ["raise", "throw", "error", "exception"], "raise"),
        ("ZeroDivisionError type?", ["ArithmeticError", "ValueError", "Exception", "TypeError"], "ArithmeticError"),
        ("File not found error?", ["FileNotFoundError", "IOError", "ValueError", "OSError"], "FileNotFoundError"),
        ("Syntax error?", ["SyntaxError", "TypeError", "NameError", "ValueError"], "SyntaxError"),
        ("Index out of range?", ["IndexError", "KeyError", "ValueError", "AttributeError"], "IndexError"),
        ("Type mismatch?", ["TypeError", "ValueError", "Exception", "IOError"], "TypeError"),
        ("Key not in dict?", ["KeyError", "IndexError", "ValueError", "NameError"], "KeyError"),
        ("Multiple exceptions?", ["except (TypeError, ValueError)", "except TypeError", "except ValueError", "except Exception"], "except (TypeError, ValueError)"),
        ("Ensure code runs?", ["finally", "else", "except", "try"], "finally"),
        ("Else in try?", ["executes if no exception", "always", "never", "on error"], "executes if no exception"),
        ("Custom exception?", ["class MyError(Exception)", "class MyError()", "def MyError()", "raise MyError"], "class MyError(Exception)"),
        ("Try block mandatory?", ["Yes", "No", "Sometimes", "Depends"], "No"),
        ("Except block mandatory?", ["Yes", "No", "Sometimes", "Depends"], "No"),
        ("Handle multiple?", ["except Exception as e", "except e", "catch e", "try-except"], "except Exception as e"),
        ("Re-raise exception?", ["raise", "throw", "exit", "pass"], "raise"),
        ("Error message?", ["str(e)", "e.message", "e.msg", "msg(e)"], "str(e)"),
        ("Exception hierarchy base?", ["BaseException", "Exception", "Error", "Object"], "BaseException"),
        ("Catch all exceptions?", ["except Exception", "except BaseException", "except Error", "except All"], "except Exception"),
    ],

    "File Handling": [
        ("Open file for reading?", ["r", "w", "a", "x"], "r"),
        ("Open file for writing?", ["r", "w", "a", "x"], "w"),
        ("Append to file?", ["a", "r", "w", "x"], "a"),
        ("Read all lines?", ["readlines()", "read()", "readline()", "readall()"], "readlines()"),
        ("Read single line?", ["readline()", "read()", "readlines()", "next()"], "readline()"),
        ("Close file?", ["close()", "exit()", "stop()", "end()"], "close()"),
        ("Delete file?", ["os.remove()", "delete()", "file.remove()", "remove()"], "os.remove()"),
        ("Rename file?", ["os.rename()", "rename()", "file.rename()", "change()"], "os.rename()"),
        ("Check file exists?", ["os.path.exists()", "exists()", "file.exists()", "check()"], "os.path.exists()"),
        ("Write text?", ["write()", "writelines()", "append()", "add()"], "write()"),
        ("Write multiple lines?", ["writelines()", "write()", "append()", "add()"], "writelines()"),
        ("File pointer start?", ["seek(0)", "seek_start()", "start()", "begin()"], "seek(0)"),
        ("File pointer end?", ["seek(0,2)", "seek_end()", "end()", "seek(-1,2)"], "seek(0,2)"),
        ("Truncate file?", ["truncate()", "cut()", "remove()", "delete()"], "truncate()"),
        ("Context manager?", ["with open()", "open()", "file()", "context()"], "with open()"),
        ("Read binary?", ["rb", "wb", "r", "b"], "rb"),
        ("Write binary?", ["wb", "rb", "w", "b"], "wb"),
        ("Check if file is readable?", ["readable()", "writable()", "openable()", "exists()"], "readable()"),
        ("Check if file is writable?", ["writable()", "readable()", "openable()", "exists()"], "writable()"),
    ],
      # ================= MATHEMATICS =================
    "Mathematics": [

        ("What does Python implementation in mathematics mean?",
         ["Using Python to solve mathematical problems",
          "Writing essays",
          "Playing games",
          "Web designing"],
         "Using Python to solve mathematical problems"),

        ("Python helps students to avoid?",
         ["Manual complex calculations",
          "Reading books",
          "Writing notes",
          "Drawing diagrams"],
         "Manual complex calculations"),

        ("Which field uses Python for symbolic mathematics?",
         ["SymPy", "HTML", "CSS", "Java"],
         "SymPy"),

        ("Which library is used for numerical computing?",
         ["NumPy", "Matplotlib", "Math", "Random"],
         "NumPy"),

        ("Which library is mainly used for graph plotting?",
         ["Matplotlib", "NumPy", "SymPy", "OS"],
         "Matplotlib"),

        ("Which library performs basic mathematical operations?",
         ["Math", "Pandas", "Tkinter", "Flask"],
         "Math"),

        ("Which program solves quadratic equations?",
         ["Quadratic Equation Solver", "Factorial Program", "Matrix Multiplication", "Taylor Series"],
         "Quadratic Equation Solver"),

        ("Which program calculates mean and standard deviation?",
         ["Mean & Standard Deviation", "Eigenvalue Method", "LU Decomposition", "Markov Chain"],
         "Mean & Standard Deviation"),

        ("Which program is used for symbolic differentiation?",
         ["Symbolic Differentiation", "Graph Plot", "Monte Carlo", "Power Method"],
         "Symbolic Differentiation"),

        ("Which method is used for root finding?",
         ["Newton–Raphson Method", "Matrix Multiplication", "Fourier Transform", "Markov Chain"],
         "Newton–Raphson Method"),

        ("Which program estimates the value of π?",
         ["Monte Carlo π Estimation", "Taylor Series", "LU Decomposition", "Eigenvalues"],
         "Monte Carlo π Estimation"),

        ("Which method solves differential equations numerically?",
         ["Euler Method", "Factorial Method", "Mean Method", "Probability Simulation"],
         "Euler Method"),

        ("Which program calculates eigenvalues?",
         ["Eigenvalues Calculation", "Graph Plot", "Factorial", "Quadratic Solver"],
         "Eigenvalues Calculation"),

        ("Which technique is used for optimization?",
         ["Gradient Descent", "Simpson Rule", "LU Decomposition", "Matrix Determinant"],
         "Gradient Descent"),

        ("Which rule is used for numerical integration?",
         ["Simpson’s Rule", "Taylor Rule", "Power Rule", "Loop Rule"],
         "Simpson’s Rule"),

        ("Which program simulates probability using randomness?",
         ["Random Probability Simulation", "Determinant of Matrix", "Linear Equation Solver", "Symbolic Differentiation"],
         "Random Probability Simulation"),

        ("Which method expands functions into series?",
         ["Taylor Series Expansion", "Matrix Multiplication", "Eigenvalue Method", "Markov Chain"],
         "Taylor Series Expansion"),

        ("Which decomposition method is used for matrices?",
         ["LU Matrix Decomposition", "Graph Plot", "Monte Carlo", "Euler Method"],
         "LU Matrix Decomposition"),

        ("Which technique is used in signal analysis?",
         ["Fourier Transform", "Factorial", "Quadratic Solver", "Mean Method"],
         "Fourier Transform"),

        ("What is the mini project about?",
         ["Machine Learning Based Differential Equation Solver", "Web Development", "Game Development", "Mobile App Design"],
         "Machine Learning Based Differential Equation Solver"),
    ],
    "Python Biology": [

        ("What does Python implementation in biology mean?",
         ["Using Python to analyze biological data",
          "Designing websites",
          "Writing novels",
          "Playing games"],
         "Using Python to analyze biological data"),

        ("Biology today generates large amounts of?",
         ["DNA sequences and medical data",
          "Video games",
          "Poetry",
          "Animations"],
         "DNA sequences and medical data"),

        ("Which field mainly studies DNA and proteins using Python?",
         ["Bioinformatics",
          "Civil Engineering",
          "Mechanical Design",
          "Architecture"],
         "Bioinformatics"),

        ("Which library is used for DNA and protein analysis?",
         ["Biopython",
          "Tkinter",
          "Flask",
          "Seaborn"],
         "Biopython"),

        ("Which library is used for biological data analysis?",
         ["NumPy / Pandas",
          "HTML",
          "CSS",
          "Bootstrap"],
         "NumPy / Pandas"),

        ("Which library is used for visualization in biology?",
         ["Matplotlib",
          "OS",
          "Random",
          "Time"],
         "Matplotlib"),

        ("Which library is used for machine learning in healthcare?",
         ["Scikit-learn",
          "Math",
          "Turtle",
          "Sys"],
         "Scikit-learn"),

        ("Which program finds the length of a DNA sequence?",
         ["DNA Length Finder",
          "BMI Calculator",
          "Population Model",
          "Mutation Detection"],
         "DNA Length Finder"),

        ("Which program counts DNA bases?",
         ["DNA Base Counter",
          "Enzyme Reaction",
          "Species Comparison",
          "Logistic Growth"],
         "DNA Base Counter"),

        ("DNA is converted into RNA in which program?",
         ["RNA Conversion",
          "GC Content",
          "Palindrome Check",
          "Similarity Percentage"],
         "RNA Conversion"),

        ("Which program analyzes GC content?",
         ["GC Content Analyzer",
          "Bacterial Growth",
          "BMI Calculator",
          "Codon Splitter"],
         "GC Content Analyzer"),

        ("Which program detects genetic mutations?",
         ["Mutation Detection",
          "DNA Frequency Graph",
          "Population Growth",
          "Ecology Model"],
         "Mutation Detection"),

        ("Which program models bacterial growth?",
         ["Simple Bacterial Growth",
          "DNA Reverse Complement",
          "Amino Acid Counter",
          "Enzyme Rate"],
         "Simple Bacterial Growth"),

        ("Which program creates the reverse complement of DNA?",
         ["DNA Reverse Complement",
          "Species Comparison",
          "Logistic Growth",
          "Disease Prediction"],
         "DNA Reverse Complement"),

        ("Which program splits DNA into codons?",
         ["Codon Splitter",
          "BMI Calculator",
          "Mutation Detection",
          "GC Analyzer"],
         "Codon Splitter"),

        ("Which program calculates human body mass index?",
         ["BMI Calculator",
          "DNA Length Finder",
          "GC Content Analyzer",
          "Codon Splitter"],
         "BMI Calculator"),

        ("Which growth model shows limited population growth?",
         ["Logistic Population Growth",
          "DNA Frequency Graph",
          "Palindrome Check",
          "Enzyme Reaction"],
         "Logistic Population Growth"),

        ("Which program checks if DNA is a palindrome?",
         ["DNA Palindrome Check",
          "RNA Conversion",
          "Species Comparison",
          "Mutation Detection"],
         "DNA Palindrome Check"),

        ("What is the aim of the AI-based project?",
         ["Predict disease risk",
          "Create websites",
          "Develop games",
          "Edit videos"],
         "Predict disease risk"),

        ("Which parameters are used for disease prediction?",
         ["Age, Blood Pressure, Sugar Level, BMI",
          "Height, Color, Name",
          "Weather Data",
          "Vehicle Speed"],
         "Age, Blood Pressure, Sugar Level, BMI"),

    ],
    "Python Botany": [

        ("What does Python implementation in botany mean?",
         ["Using Python to study plants scientifically",
          "Designing plant pots",
          "Writing stories about plants",
          "Selling seeds online"],
         "Using Python to study plants scientifically"),

        ("Botanists collect data about?",
         ["Plant growth, climate, and soil",
          "Mobile apps",
          "Video games",
          "Cars"],
         "Plant growth, climate, and soil"),

        ("Python helps predict?",
         ["Plant growth patterns",
          "Movie ratings",
          "Sports scores",
          "Traffic signals"],
         "Plant growth patterns"),

        ("Which field uses AI for plant disease detection?",
         ["Plant pathology",
          "Mechanical engineering",
          "Banking",
          "Astronomy"],
         "Plant pathology"),

        ("Which library is used for plant data analysis?",
         ["Pandas / NumPy",
          "Tkinter",
          "Flask",
          "Pygame"],
         "Pandas / NumPy"),

        ("Which library is used for plant growth graph visualization?",
         ["Matplotlib",
          "Random",
          "OS",
          "Sys"],
         "Matplotlib"),

        ("Which library is used for plant image analysis?",
         ["OpenCV",
          "Math",
          "Time",
          "JSON"],
         "OpenCV"),

        ("Which library is used for AI-based plant disease prediction?",
         ["Scikit-learn",
          "HTML",
          "CSS",
          "Bootstrap"],
         "Scikit-learn"),

        ("Which program calculates plant growth experimentally?",
         ["Plant Growth Calculator",
          "Leaf Area Calculator",
          "NDVI Calculator",
          "Disease Detection"],
         "Plant Growth Calculator"),

        ("Which program measures leaf area?",
         ["Leaf Area Calculator",
          "Seed Germination",
          "Chlorophyll Estimator",
          "Plant Density"],
         "Leaf Area Calculator"),

        ("Which program studies plant population in ecology?",
         ["Plant Population Density",
          "Photosynthesis Rate",
          "Growth Prediction",
          "GC Content"],
         "Plant Population Density"),

        ("Which program analyzes plant DNA GC content?",
         ["Plant DNA GC Content",
          "Leaf Area Calculator",
          "Biodiversity Index",
          "NDVI Index"],
         "Plant DNA GC Content"),

        ("Which model is used for ecological plant growth?",
         ["Logistic Plant Growth Model",
          "Linear Search",
          "Binary Tree",
          "Sorting Algorithm"],
         "Logistic Plant Growth Model"),

        ("Which program calculates photosynthesis rate?",
         ["Photosynthesis Rate Calculator",
          "Plant Density",
          "GC Content",
          "Species Similarity"],
         "Photosynthesis Rate Calculator"),

        ("Which program calculates seed germination percentage?",
         ["Seed Germination Percentage",
          "Leaf Area",
          "Plant Growth Prediction",
          "NDVI Calculator"],
         "Seed Germination Percentage"),

        ("Which program estimates chlorophyll content?",
         ["Chlorophyll Content Estimator",
          "Population Density",
          "Disease Detection",
          "Biodiversity Index"],
         "Chlorophyll Content Estimator"),

        ("Which program compares plant DNA sequences?",
         ["Plant Species Similarity",
          "Photosynthesis Rate",
          "Leaf Area",
          "Growth Calculator"],
         "Plant Species Similarity"),

        ("Which index is used for vegetation monitoring?",
         ["NDVI Vegetation Index",
          "BMI Index",
          "GC Index",
          "DNA Index"],
         "NDVI Vegetation Index"),

        ("Which index measures plant biodiversity?",
         ["Shannon Index",
          "GC Content",
          "NDVI",
          "BMI"],
         "Shannon Index"),

        ("What is the mini project about?",
         ["AI-Based Plant Disease Detection",
          "Game Development",
          "Website Design",
          "Bank Management"],
         "AI-Based Plant Disease Detection"),

    ],
     "Python Zoology": [

        ("What does Python implementation in zoology mean?",
         ["Using Python to study animals scientifically",
          "Training pets",
          "Selling animal products",
          "Drawing cartoons"],
         "Using Python to study animals scientifically"),

        ("Zoologists collect data about?",
         ["Animal movement and population",
          "Computer hardware",
          "Mobile apps",
          "Traffic systems"],
         "Animal movement and population"),

        ("Python helps scientists to predict?",
         ["Animal behavior",
          "Movie collections",
          "Game scores",
          "Website traffic"],
         "Animal behavior"),

        ("Which field uses Python for wildlife conservation?",
         ["Wildlife conservation",
          "Banking",
          "Mechanical repair",
          "Architecture"],
         "Wildlife conservation"),

        ("Which program calculates animal population density?",
         ["Animal Population Density",
          "DNA Translation",
          "Disease Predictor",
          "Classification Model"],
         "Animal Population Density"),

        ("Which program studies animal weight growth?",
         ["Animal Weight Growth Calculator",
          "Fish Growth Model",
          "GC Content",
          "Biodiversity Index"],
         "Animal Weight Growth Calculator"),

        ("Which model is used in marine zoology?",
         ["Fish Population Growth Model",
          "Predator Simulation",
          "Classification ML",
          "DNA Translation"],
         "Fish Population Growth Model"),

        ("Which program analyzes animal DNA GC content?",
         ["Animal DNA GC Content",
          "Animal Movement",
          "Disease Risk",
          "Weight Growth"],
         "Animal DNA GC Content"),

        ("Which simulation studies food chain interaction?",
         ["Predator–Prey Simulation",
          "Animal Classification",
          "DNA Translation",
          "Population Density"],
         "Predator–Prey Simulation"),

        ("Which program predicts animal disease risk?",
         ["Animal Disease Risk Predictor",
          "Population Model",
          "Marine Index",
          "Weight Calculator"],
         "Animal Disease Risk Predictor"),

        ("Which program translates animal DNA sequences?",
         ["Animal DNA Translation",
          "Predator Simulation",
          "Logistic Model",
          "Movement Analysis"],
         "Animal DNA Translation"),

        ("Which program analyzes animal movement speed?",
         ["Animal Movement Speed Analysis",
          "DNA GC Content",
          "Disease Risk",
          "Fish Model"],
         "Animal Movement Speed Analysis"),

        ("Which index is used in marine biodiversity?",
         ["Simpson Index",
          "Shannon Index",
          "BMI",
          "NDVI"],
         "Simpson Index"),

        ("Which model studies limited population growth?",
         ["Logistic Animal Population Model",
          "Linear Model",
          "Sorting Model",
          "Search Model"],
         "Logistic Animal Population Model"),

        ("Which technique is used for animal classification?",
         ["Machine Learning",
          "HTML",
          "CSS",
          "Excel Formatting"],
         "Machine Learning"),

        ("Python helps track?",
         ["Animal migration patterns",
          "Bank transactions",
          "Social media likes",
          "TV ratings"],
         "Animal migration patterns"),

        ("Which field studies animal feeding behavior?",
         ["Animal behavior research",
          "Civil engineering",
          "Web design",
          "Graphic design"],
         "Animal behavior research"),

        ("Which field studies animal health data?",
         ["Veterinary science",
          "Architecture",
          "Fashion design",
          "Marketing"],
         "Veterinary science"),

        ("What is the zoology mini project about?",
         ["Predator–Prey Ecosystem Simulation",
          "Game development",
          "Mobile app design",
          "Website hosting"],
         "Predator–Prey Ecosystem Simulation"),

        ("Python is used in zoology mainly for?",
         ["Data analysis and ecosystem simulation",
          "Painting animals",
          "Cooking recipes",
          "Writing poems"],
         "Data analysis and ecosystem simulation"),

    ],
    "Python Physics": [

        ("What does Python implementation in physics mean?",
         ["Using Python to solve physics problems",
          "Designing circuits manually",
          "Drawing physics diagrams",
          "Writing physics textbooks"],
         "Using Python to solve physics problems"),

        ("Python helps physicists avoid?",
         ["Long manual calculations",
          "Reading books",
          "Writing notes",
          "Laboratory work"],
         "Long manual calculations"),

        ("Which library is used for scientific computing?",
         ["SciPy",
          "Tkinter",
          "Flask",
          "Pygame"],
         "SciPy"),

        ("Which library is used for symbolic mathematics?",
         ["SymPy",
          "NumPy",
          "Pandas",
          "Matplotlib"],
         "SymPy"),

        ("Which program calculates velocity?",
         ["Velocity Calculation",
          "Pressure Calculation",
          "Pendulum Simulation",
          "Wave Analysis"],
         "Velocity Calculation"),

        ("Newton’s Second Law calculates?",
         ["Force",
          "Velocity",
          "Energy",
          "Pressure"],
         "Force"),

        ("Ohm’s Law relates to?",
         ["Electricity",
          "Gravity",
          "Waves",
          "Magnetism only"],
         "Electricity"),

        ("Which program simulates free fall motion?",
         ["Free Fall Motion",
          "Density Calculation",
          "Fourier Analysis",
          "Quantum Box"],
         "Free Fall Motion"),

        ("Which graph visualizes oscillation?",
         ["Oscillation graph",
          "Bar graph",
          "Pie chart",
          "Histogram"],
         "Oscillation graph"),

        ("Which program calculates density?",
         ["Density Calculation",
          "Velocity Program",
          "Electric Field",
          "Wave Function"],
         "Density Calculation"),

        ("Which program calculates pressure?",
         ["Pressure Calculation",
          "Projectile Motion",
          "Fourier Wave",
          "Damped Oscillation"],
         "Pressure Calculation"),

        ("Simple pendulum program calculates?",
         ["Time period",
          "Energy",
          "Charge",
          "Voltage"],
         "Time period"),

        ("Projectile motion simulation studies?",
         ["Object motion in air",
          "Electric current",
          "Heat transfer",
          "Atomic structure"],
         "Object motion in air"),

        ("Fourier Wave Analysis studies?",
         ["Wave patterns",
          "Gravity",
          "Mass",
          "Temperature"],
         "Wave patterns"),

        ("Electric Field Calculation relates to?",
         ["Electrostatics",
          "Thermodynamics",
          "Optics",
          "Sound"],
         "Electrostatics"),

        ("Gravitational force program studies?",
         ["Attraction between masses",
          "Electric charge",
          "Magnetic field",
          "Light reflection"],
         "Attraction between masses"),

        ("Energy levels in particle-in-box are proportional to?",
         ["n²",
          "n",
          "1/n",
          "√n"],
         "n²"),

        ("Quantum number is represented by?",
         ["n",
          "x",
          "L",
          "E"],
         "n"),

        ("Wavefunction symbol is?",
         ["ψ(x)",
          "E(x)",
          "F(x)",
          "V(x)"],
         "ψ(x)"),

        ("Main aim of physics mini project?",
         ["Simulate quantum particle in a box",
          "Build website",
          "Design robot",
          "Create database"],
         "Simulate quantum particle in a box"),

    ],
    "Python Chemistry": [

        ("What does Python implementation in chemistry mean?",
         ["Using Python for chemical calculations and analysis",
          "Cooking chemicals",
          "Drawing molecules by hand",
          "Selling medicines"],
         "Using Python for chemical calculations and analysis"),

        ("Python helps reduce?",
         ["Manual errors",
          "Chemical reactions",
          "Laboratory equipment",
          "Chemical elements"],
         "Manual errors"),

        ("Reaction rate shows?",
         ["Speed of reaction",
          "Color change",
          "Mass only",
          "Volume only"],
         "Speed of reaction"),

        ("Molecular weight is calculated using?",
         ["Atomic masses",
          "Temperature",
          "Pressure",
          "Volume"],
         "Atomic masses"),

        ("pH determines?",
         ["Acidity or alkalinity",
          "Color",
          "Mass",
          "Density"],
         "Acidity or alkalinity"),

        ("Spectroscopy measures?",
         ["Light absorption",
          "Sound waves",
          "Electric current",
          "Magnetic force"],
         "Light absorption"),

        ("Drug discovery uses Python for?",
         ["Molecule analysis",
          "Painting drugs",
          "Packing medicines",
          "Selling tablets"],
         "Molecule analysis"),

        ("Chemical simulations help?",
         ["Model reactions virtually",
          "Explode chemicals",
          "Stop reactions",
          "Destroy molecules"],
         "Model reactions virtually"),

        ("AI-based chemical prediction is used for?",
         ["Toxicity prediction",
          "Cooking analysis",
          "Weather report",
          "Game design"],
         "Toxicity prediction"),

        ("Laboratory data automation helps?",
         ["Store experiment records",
          "Create music",
          "Edit videos",
          "Design clothes"],
         "Store experiment records"),

        ("Python is widely used in?",
         ["Pharmaceutical industries",
          "Fashion industry",
          "Sports training",
          "Film making"],
         "Pharmaceutical industries"),

        ("Chemical data analysis handles?",
         ["Large datasets",
          "Small toys",
          "Paint colors",
          "Music files"],
         "Large datasets"),

        ("Scientific graph plotting helps?",
         ["Visualize experiments",
          "Play games",
          "Design posters",
          "Edit photos"],
         "Visualize experiments"),

        ("Python is advantageous because it is?",
         ["Open-source",
          "Paid only",
          "Hardware device",
          "Mechanical tool"],
         "Open-source"),

        ("One limitation of Python is?",
         ["Requires programming knowledge",
          "Cannot calculate",
          "No libraries",
          "No graphs"],
         "Requires programming knowledge"),

        ("Chemical Reaction Analyzer project does?",
         ["Analyze reaction data",
          "Sell chemicals",
          "Clean lab",
          "Mix random compounds"],
         "Analyze reaction data"),

        ("Reaction rate calculation belongs to?",
         ["Chemical kinetics",
          "Zoology",
          "Botany",
          "Astronomy"],
         "Chemical kinetics"),

        ("pH analysis is used in?",
         ["Water quality testing",
          "Space travel",
          "Mechanical repair",
          "Construction"],
         "Water quality testing"),

        ("Spectroscopy is used in?",
         ["Material analysis",
          "Game design",
          "Vehicle testing",
          "Text editing"],
         "Material analysis"),

        ("Main feature of chemistry mini project?",
         ["Reaction rate, pH, graph plotting",
          "Game creation",
          "Website hosting",
          "Image editing"],
         "Reaction rate, pH, graph plotting"),

    ],
}

# ------------------ LOAD QUESTIONS ------------------
# ------------------ LOAD QUESTIONS ------------------
if "quiz_questions" not in st.session_state:
    if quiz_topic not in QUESTION_BANK:
        st.error(f"No questions available for {quiz_topic}")
        st.stop()

    questions = QUESTION_BANK[quiz_topic].copy()
    random.shuffle(questions)
    st.session_state.quiz_questions = questions

questions = st.session_state.quiz_questions

# ------------------ USER ANSWERS ------------------
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# ------------------ QUESTIONS UI ------------------
for i, (q, options, _) in enumerate(questions):
    st.markdown(f"**Q{i+1}. {q}**")
    st.session_state.user_answers[i] = st.radio("", options, key=f"q{i}")

# ------------------ SUBMIT ------------------
if st.button("✅ Submit Quiz"):
    score = 0
    st.divider()
    st.subheader("📊 Results")

    for i, (_, _, answer) in enumerate(questions):
        if st.session_state.user_answers.get(i) == answer:
            score += 1
            st.success(f"Q{i+1}: Correct")
        else:
            st.error(f"Q{i+1}: Wrong | Correct: {answer}")

    st.markdown(f"## 🎯 Final Score: **{score} / 20**")

    cursor.execute(
        "INSERT INTO quiz_marks (student_name, topic, score, total) VALUES (?, ?, ?, ?)",
         (st.session_state.get("user_email","unknown"), quiz_topic, score, 20)
    )
    conn.commit()

    st.success("✅ Quiz result saved successfully!")

# ------------------ BACK BUTTON ------------------
st.divider()
if st.button("⬅ Back to Study Material"):
    st.session_state.pop("quiz_questions", None)
    st.session_state.pop("user_answers", None)
    st.switch_page("pages/Study_Material.py")
