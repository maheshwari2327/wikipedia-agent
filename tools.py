import warnings
import wikipedia
from langchain_core.tools import tool
from wikipedia.exceptions import DisambiguationError, PageError

# Suppress BeautifulSoup GuessedAtParserWarning from wikipedia package
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")


@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for a topic and return a concise summary with the article URL.
    Handles disambiguation by listing options. Uses the wikipedia Python package — free.
    """
    try:
        suggestions = wikipedia.search(query)
        if not suggestions:
            return "No page found"

        target = suggestions[0]
        summary = wikipedia.summary(target, sentences=5, auto_suggest=False)
        try:
            page = wikipedia.page(target, auto_suggest=False)
        except Exception:
            page = wikipedia.page(target)

        return (
            f"Topic : {page.title}\n"
            f"URL   : {page.url}\n\n"
            f"{summary}"
        )
    except DisambiguationError as e:
        options = ", ".join(e.options[:8])
        return (
            f"Disambiguation error: '{query}' may refer to multiple topics. "
            f"Options include: {options}"
        )
    except PageError:
        return "No page found"
    except Exception as e:
        return f"Error searching Wikipedia: {e}"
