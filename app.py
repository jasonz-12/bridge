from imports import *
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="💭",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
st.title("💭 ChatGPT Clone")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    client = OpenAI()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            for chunk in client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a helpful assistant - your master's name is Olivia."}] + 
                        [{"role": m["role"], "content": m["content"]} 
                         for m in st.session_state.messages],
                stream=True,
            ):
                chunk_msg = chunk.choices[0].delta.content
                if chunk_msg is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
                else:
                    continue
            
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Add a clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []