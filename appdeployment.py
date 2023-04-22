import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect
    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  
    Here are some examples of words in different dialects:
    - American:"antenna","mad","anyplace","fall","bill","attorney","cookie","hood","trunk","suspenders","janitor","drug store","french fries","the movies","rubber","patrolman","stove","wheat","crib","thread","wreck","intersection","drapes","checkers","thumbtack","divided highway","pacifier","trashcan","garbage can","garbage collector","generator","motor","engineer","movie","apartment","overpass","yard","gear-shift","alumnus","boiler","first floor","rubbers","sneakers","purse","billboard","vacation","vacuum cleaner","sick","intermission","sweater","pitcher","elevator","truck","baggage","raincoat","crazy","highway","corn","math","stingy","freeway","diaper","vicious, mean","noplace","private hospital","optometrist","liquor store","kerosene","sidewalk" 
    - British: "aerial","angry","anywhere","autumn","bank note","barrister, solicitor","biscuit","bonnet","boot","braces","caretaker","chemist's","chips","the cinema","condom","constable","cooker","corn, wheat","cot","cotton","crash","crossroads","curtains","draughts","drawing pin","dual carriageway","dummy","dustbin, rubbish-bin","dustbin, rubbish-bin","dustman","dynamo","engine","engine driver","film","flat","flyover","garden","gear-lever","graduate","grill","ground floor","gumshoes, wellington boots","gym shoes, tennis-shoes","handbag","hoarding","holiday","hoover","ill","interval","jersey, jumper, pullover, sweater","jug","lift","lorry","luggage","mackintosh, raincoat","mad","main road","maize","maths","mean","motorway","nappy","nasty","nowhere","nursing home","optician","off-license","paraffin","pavement"
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. Just giving a shot with LangChain")


st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)