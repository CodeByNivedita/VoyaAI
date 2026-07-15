import requests


def safe_llm_invoke(llm, messages):
    """
    Safely invoke an LLM and return either the response
    or a dictionary containing an error.
    """

    try:
        return llm.invoke(messages)

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "The AI service timed out. Please try again."
        }

    except Exception as e:

        error = str(e).lower()

        if "429" in error or "quota" in error:
            return {
                "success": False,
                "error": "AI usage limit reached. Please try again later."
            }

        elif "401" in error or "unauthorized" in error:
            return {
                "success": False,
                "error": "Authentication failed."
            }

        elif "connection" in error:
            return {
                "success": False,
                "error": "Unable to connect to the AI service."
            }

        else:
            print(e)

            return {
                "success": False,
                "error": "AI service is temporarily unavailable."
            }