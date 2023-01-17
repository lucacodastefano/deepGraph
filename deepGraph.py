#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openai
import re

# Set up the OpenAI API client
openai.api_key = "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"

def read_text_file(filepath):
    try:
        with open(filepath, 'r') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"{filepath} not found.")
    except:
        print(f"An error occurred while reading {filepath}.")

def add_tab(n):
    indentation = ""
    for i in range(n):
        indentation += "\t"
    return indentation

def extract_topics(tuples):
    topics = ''
    for tuple in tuples:
        topics += str(tuple[0]) + ','
    return topics
        
def generate_deep_info(sentence, depth = 1, original_depth = 1, topic_excluded=''):
    
    if (depth == 0):
        return
    
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = read_text_file('sentence.txt')
    prompt = prompt.replace('(%%%)', sentence)
    if (topic_excluded != ''):
        prompt += '\n' + '- not explain these concepts:' + topic_excluded
        
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )

    response = completion.choices[0].text

    text = response


    # Split the text into a list of strings
    list_of_strings = text.split("|")

    # Create an empty list to store the tuples
    results = []

    # Iterate through the list of strings
    for s in list_of_strings:
        # Use regular expressions to extract the information before and after the colon
        match = re.search(r"(.*): (.*)", s)
        if match:
            # Append the tuple to the results list
            results.append((match.group(1), match.group(2)))
            
    for tuple in results:
        print(add_tab(original_depth - depth) + str(tuple))
        generate_deep_info(tuple[1], depth-1, original_depth, extract_topics(results))


# In[ ]:


generate_deep_info("To make an authorized request on a resource server, you need a bearer token. If your resource server is configured for JWTs, the bearer token needs to be signed and then encoded according to the JWT specification. All of this can be quite daunting, especially when this is not the focus of your test.", 3, 3)


# In[ ]:




