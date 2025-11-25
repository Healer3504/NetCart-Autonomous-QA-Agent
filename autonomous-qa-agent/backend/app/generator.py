from typing import Dict
from .llm_integration import generate_selenium_with_html
from .rag import HTML_STRUCTURE


def create_selenium_script(test_case: Dict) -> str:
    """
    Generate Selenium script using YOUR actual checkout.html selectors.
    """
    return generate_selenium_with_html(test_case, HTML_STRUCTURE)