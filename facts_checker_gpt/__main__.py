import time

import openai
from colorama import Fore
from scripts.config import Config
from scripts.logger import logger
import scripts.utils
from alpaca import Alpaca
import chat

cfg = Config()


def judge_llm(user_prompt, alpaca: Alpaca):
    prompt = user_prompt
    fact_checker_agent_response = ""
    if fact_checker_agent_response != "":
        prompt = prompt + "\nConsider that while we compared you to another agent, the result was: \n" + fact_checker_agent_response
    logger.typewriter_log(f"Prompt: {prompt}", Fore.LIGHTYELLOW_EX, "")

    if cfg.chatbot_agent_1_model == "alpaca":
        agent1_response: str = chat.get_alpaca_response(prompt, alpaca)
    else:
        agent1_response: str = chat.get_chatgpt_response(prompt, cfg.chatbot_agent_1_model)
    if cfg.chatbot_agent_2_model == "alpaca":
        agent2_response: str = chat.get_alpaca_response(prompt, alpaca)
    else:
        agent2_response: str = chat.get_chatgpt_response(prompt, cfg.chatbot_agent_2_model)
    if cfg.fact_checker_agent_model == "alpaca":
        fact_checker_agent_response: str = chat.judge_answers_with_alpaca(prompt, agent1_response,
                                                                          agent2_response, alpaca)
    else:
        fact_checker_agent_response: str = chat.judge_answers_with_gpt(prompt, agent1_response, agent2_response, cfg.chatbot_agent_2_model)

    logger.typewriter_log(f"Chatbot Agent1 ({cfg.chatbot_agent_1_model}) responded:", Fore.YELLOW, "")
    print(agent1_response)
    logger.typewriter_log(f"Chatbot Agent2 ({cfg.chatbot_agent_2_model}) responded:", Fore.YELLOW, "")
    print(agent2_response)

    logger.typewriter_log(f"The Judge Agent ({cfg.fact_checker_agent_model}) responded:", Fore.GREEN, "")
    logger.typewriter_log(fact_checker_agent_response, Fore.GREEN, "")


def llms_competition(user_prompt, alpaca: Alpaca):
    prompt = user_prompt
    retries = 0
    fact_checker_agent_response = ""
    while retries <= 2:
        if fact_checker_agent_response != "":
            prompt = prompt + "\nConsider that while we compared you to another agent, the result was: \n" + fact_checker_agent_response
        logger.typewriter_log(f"Prompt: {prompt}", Fore.LIGHTYELLOW_EX, "")

        if cfg.chatbot_agent_1_model == "alpaca":
            agent1_response: str = chat.get_alpaca_response(prompt, alpaca)
        else:
            agent1_response: str = chat.get_chatgpt_response(prompt, cfg.chatbot_agent_1_model)
        if cfg.chatbot_agent_2_model == "alpaca":
            agent2_response: str = chat.get_alpaca_response(prompt, alpaca)
        else:
            agent2_response: str = chat.get_chatgpt_response(prompt, cfg.chatbot_agent_2_model)
        if cfg.fact_checker_agent_model == "alpaca":
            fact_checker_agent_response: str = chat.verify_answer_with_alpaca(prompt, agent1_response,
                                                                              agent2_response, alpaca)
        else:
            fact_checker_agent_response: str = chat.verify_answer_with_gpt(prompt, agent1_response, agent2_response, cfg.chatbot_agent_2_model)

        logger.typewriter_log(f"Chatbot Agent1 ({cfg.chatbot_agent_1_model}) responded:", Fore.YELLOW, "")
        print(agent1_response)
        logger.typewriter_log(f"Chatbot Agent2 ({cfg.chatbot_agent_2_model}) responded:", Fore.YELLOW, "")
        print(agent2_response)

        if fact_checker_agent_response.lower() == "are the same":
            logger.typewriter_log(f"FactsCheckerGPT Agent ({cfg.fact_checker_agent_model}) responded:", Fore.GREEN, "")
            logger.typewriter_log(fact_checker_agent_response, Fore.GREEN, "")
            return agent1_response
        else:
            logger.typewriter_log(f"FactsCheckerGPT Agent ({cfg.fact_checker_agent_model}) responded:", Fore.RED, "")
            logger.typewriter_log(fact_checker_agent_response, Fore.RED, "")
            retries += 1


def prompts_feeding_mode(prompt, alpaca: Alpaca):
    retries = 0
    while retries <= 2:
        if cfg.chatbot_agent_1_model == "alpaca":
            agent1_response: str = chat.get_alpaca_response(prompt, alpaca)
        else:
            agent1_response: str = chat.get_chatgpt_response(prompt, cfg.chatbot_agent_1_model)
        if cfg.chatbot_agent_2_model == "alpaca":
            agent2_response: str = chat.verify_answer_with_alpaca(prompt, agent1_response, alpaca)
        else:
            agent2_response: str = chat.verify_answer_with_gpt(prompt, agent1_response, cfg.chatbot_agent_2_model)

        logger.typewriter_log(f"Chatbot Agent1 ({cfg.chatbot_agent_1_model}) responded:", Fore.YELLOW, "")
        print(agent1_response)

        if agent2_response.lower() == "seems correct":
            logger.typewriter_log(f"FactsCheckerGPT Agent2 ({cfg.chatbot_agent_2_model}) responded:", Fore.GREEN, "")
            logger.typewriter_log(agent2_response, Fore.GREEN, "")
            return agent1_response
        else:
            logger.typewriter_log(f"FactsCheckerGPT Agent2 ({cfg.chatbot_agent_2_model}) responded:", Fore.RED, "")
            logger.typewriter_log(agent2_response, Fore.RED, "")
            retries += 1

def main():
    openai.api_key = cfg.openai_api_key

    alpaca_cli_path = cfg.alpaca_executable_path
    model_path = cfg.alpaca_model_path
    alpaca: Alpaca = None
    try:
        alpaca = Alpaca(alpaca_cli_path, model_path)
        # sleep until Alpaca is ready
        time.sleep(50)
        logger.typewriter_log(
            "Welcome to FactsCheckerGPT! ",
            Fore.GREEN,
            "Designed to let you talk with ChatGPT in a safer way. Please enter your prompt below.", )
        count = 0
        while True:
            count += 1
            logger.typewriter_log(
                "PROMPT NUMBER " + str(count),
                Fore.CYAN,
                "")
            user_prompt = scripts.utils.clean_input("Prompt: ")
            if user_prompt.lower() == "quit":
                break
            llms_competition(user_prompt, alpaca)
    finally:
        # check if alpaca is not null
        if alpaca is not None:
            print("Closing Alpaca")
            alpaca.stop()


if __name__ == "__main__":
    main()
