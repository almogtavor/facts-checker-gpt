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


def verify_answer_with_gpt(prompt, first_answer, second_answer, model):
    check_prompt = f"""Please compare both answers (return \"THESE ARE THE SAME\" or not and why) to the following prompt.
                   The prompt is: \"{prompt}\"
                   The first answer to validate is: \"{first_answer}\"
                   The second answer to validate is: \"{second_answer}\"
                   It is important that if everything is correct return \"THESE ARE THE SAME\"."""
    response = get_chatgpt_response(check_prompt, "gpt-3.5-turbo")
    # check if the response contains the string "are the same" or "is correct"
    if "are the same" in response.lower():
        response = "are the same"
    return response


def judge_answers_with_gpt(prompt, first_answer, second_answer, model):
    check_prompt = f"""Please decide with of these answers is the correct one to the following prompt.
                   The prompt is: \"{prompt}\"
                   The first answer to validate is: \"{first_answer}\"
                   The second answer to validate is: \"{second_answer}\""""
    return get_chatgpt_response(check_prompt, "gpt-3.5-turbo")


def judge_answers_with_alpaca(prompt, first_answer, second_answer, alpaca: Alpaca):
    check_prompt = f"""Please decide with of these answers is the correct one to the following prompt.
                   The prompt is: \"{prompt}\"
                   The first answer to validate is: \"{first_answer}\"
                   The second answer to validate is: \"{second_answer}\""""
    return alpaca.run(check_prompt)


def verify_answer_with_alpaca(prompt, first_answer, second_answer, alpaca: Alpaca):
    check_prompt = f"""Please compare both answers (return \"THESE ARE THE SAME\" or not and why) to the following prompt.
                   The prompt is: \"{prompt}\"
                   The first answer to validate is: \"{first_answer}\"
                   The second answer to validate is: \"{second_answer}\"
                   It is important that if everything is correct return \"THESE ARE THE SAME\"."""
    # check if the response contains the string "are the same" or "is correct"
    response = alpaca.run(check_prompt)
    if "are the same" in response.lower():
        response = "are the same"
    return response


def verify_answer_with_gpt_supply_answers_mode(prompt, answer, model):
    check_prompt = f"""Please perform fact check (return \"SEEMS CORRECT\" or not and why) to the following text.
                   The prompt is: \"{prompt}\"
                   The answer to validate is: \"{answer}\"
                   It is important that if everything is correct return \"SEEMS CORRECT\"."""
    response = get_chatgpt_response(check_prompt, "gpt-3.5-turbo")
    # check if the response contains the string "seems correct" or "is correct"
    if "seems correct" in response.lower() or "is correct" in response.lower() or answer.lower() in response.lower():
        response = "SEEMS CORRECT"
    return response


def verify_answer_with_alpaca_supply_answers_mode(prompt, answer, alpaca: Alpaca):
    check_prompt = f"""Please perform fact check (return \"SEEMS CORRECT\" or not and why) to the following text.
                   The prompt is: \"{prompt}\"
                   The answer to validate is: \"{answer}\"
                   It is important that if everything is correct return \"SEEMS CORRECT\"."""
    # check if the response contains the string "seems correct" or "is correct"
    response = alpaca.run(check_prompt)
    if "seems correct" in response.lower() or "is correct" in response.lower() or answer.lower() in response.lower():
        response = "SEEMS CORRECT"
    return response
