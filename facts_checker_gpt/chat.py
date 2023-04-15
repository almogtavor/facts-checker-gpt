import openai
from scripts.config import Config
from alpaca import Alpaca

cfg = Config()


def get_chatgpt_response(prompt, model):
    response = openai.ChatCompletion.create(
        model=model,
        max_tokens=150,
        n=1,
        stop=None,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def get_alpaca_response(prompt, alpaca: Alpaca) -> str:
    # try:
    response = alpaca.run(prompt)
    return response


def verify_answer_with_gpt(prompt, answer, model):
    check_prompt = f"""Please perform fact check (return \"SEEMS CORRECT\" or not and why) to the following text.
                   The prompt is: \"{prompt}\"
                   The answer to validate is: \"{answer}\"
                   It is important that if everything is correct return \"SEEMS CORRECT\"."""
    response = get_chatgpt_response(check_prompt, "gpt-3.5-turbo")
    # check if the response contains the string "seems correct" or "is correct"
    if "seems correct" in response.lower() or "is correct" in response.lower() or answer.lower() in response.lower():
        response = "SEEMS CORRECT"
    return response


def verify_answer_with_alpaca(prompt, answer, alpaca: Alpaca):
    check_prompt = f"""Please perform fact check (return \"SEEMS CORRECT\" or not and why) to the following text.
                   The prompt is: \"{prompt}\"
                   The answer to validate is: \"{answer}\"
                   It is important that if everything is correct return \"SEEMS CORRECT\"."""
    # check if the response contains the string "seems correct" or "is correct"
    response = alpaca.run(check_prompt)
    if "seems correct" in response.lower() or "is correct" in response.lower() or answer.lower() in response.lower():
        response = "SEEMS CORRECT"
    return response
