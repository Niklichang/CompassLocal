from flask import Flask, request, jsonify
from flask_cors import CORS
import dotenv
from chat import create_docchain_retriever, create_retrieval_chain, reply, create_chat_history

app = Flask(__name__)
CORS(app)  # Enable CORS

dotenv.load_dotenv()
# input filepath
docchain, retriever = create_docchain_retriever('review_sample.csv')
retrieval_chain = create_retrieval_chain(docchain, retriever)


chat_history = create_chat_history()
# Backend function for processing input
def backend_process(user_input):
    global chat_history
    # Imagine this function processes the input and returns a result
    output, chat_history = reply(user_input, retrieval_chain, chat_history)
    return f"Processed: {output}"

@app.route('/process', methods=['POST'])
def process():
    # Parse JSON data from the request
    data = request.get_json()
    user_input = data['user_input']
    result = backend_process(user_input)
    # Send back the processed result as JSON
    return jsonify({"response": result})

# reset button/ create new chat with new chat history
@app.route('/reset', methods=['POST'])
def reset_chat_history():
    global chat_history
    chat_history = create_chat_history()  # reset chat history
    return jsonify({"message": "New chat created"})

if __name__ == '__main__':
    app.run(debug=True)

