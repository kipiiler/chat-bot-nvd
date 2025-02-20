from langchain_core.tools import Tool
from langchain.agents import AgentType, initialize_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from typing import Optional
import logging
from rich.console import Console

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger("security_analyst")

class CheckIfAskingAboutCertainCVE():
    def __init__(self, llm):
        self.chain = LLMChain(llm=llm, prompt=self._get_system_prompt())

    def run(self, user_input: str):
        res = self.chain.run(user_input)
        # remove thinking steps
        remove_think = res.split("</think>")[-1]
        if "<HOHO>" in remove_think:
            return True
        return False
    
    def _get_system_prompt(self):
        p = """
You are an AI assistant specialized in identifying cybersecurity-related queries. 
Your task is to determine if the given text is related to cybersecurity, computer security, or information security. DO NOT provide any additional information only output "<HOHO>" if the text is related to cybersecurity, otherwise output an empty string.

Examples:
Query: "What is CVE-2021-1234?"
Output: <HOHO>

Query: "How are you doing?"
Output: 

Query: "Were there any OpenSSL vulnerabilities in January of 2024?"
Output: <HOHO>

Query: "What is the weather like in New York?"
Output: 

Query: "Can you explain the Log4Shell vulnerability?"
Output: <HOHO>

Query: "What's your favorite color?"
Output: 

Current query: {user_input}

Output:
"""
        return PromptTemplate(input_variables=["user_input"], template=p)

class SecurityAnalystCLI:
    def __init__(self, llm, tools: list, system_prompt: Optional[str] = None):
        """
        Initialize the Security Analyst CLI.
        
        Args:
            llm: Language model instance
            tools: List of available tools
            system_prompt: Optional system prompt override
        """
        self.console = Console()
        self.llm = llm
        self.check_agent = CheckIfAskingAboutCertainCVE(llm)
        self.tools = tools
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.agent = self._initialize_agent()

    def _get_default_system_prompt(self) -> str:
        return """You are a security analyst working for a large company. Your primary responsibility is to assist clients by explaining details about CVEs (Common Vulnerabilities and Exposures) and CPEs (Common Platform Enumerations)."""
    
    def _initialize_agent(self):
        """Initialize the LangChain agent with memory and prompt template."""
        try:
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                max_buffer_length=10,
                
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ])

            return initialize_agent(
                self.tools,
                self.llm,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                memory=memory,
                prompt=prompt,
                iterations=3,
                handle_parsing_errors=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}")
            raise

    def _process_input(self, user_input: str) -> bool:
        """
        Process user input and return whether to continue the conversation.
        
        Returns:
            bool: True if conversation should continue, False if should exit
        """
        if user_input.lower() in ['q', 'quit', 'exit']:
            self.console.print("[yellow]Goodbye![/yellow]")
            return False

        try:
            self.console.print("[blue]Processing your query...[/blue]")
            if self.check_agent.run(user_input):
                reply = self.agent.invoke(user_input)
                if reply:
                    response = reply["output"]
                else:
                    response= "I'm sorry, I'm not find what you're asking about. Could you please rephrase your question?"
            else:
                response = self.llm.invoke(user_input)
            self.console.print("\n[green]Response:[/green]")
            self.console.print(response)
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            self.console.print(f"\n[red]An error occurred while processing your query: {str(e)}[/red]")
            self.console.print("[yellow]Please try rephrasing your question or try again later.[/yellow]")

        return True

    def run(self):
        """Start the interactive CLI session."""
        self.console.print("[bold blue]Welcome to the Security Analyst Chatbot[/bold blue]")
        self.console.print("Type 'q', 'quit', or 'exit' to end the session\n")

        user_input = self.console.input("[bold green]You:[/bold green] ")
        while True:
            try:
                if not self._process_input(user_input):
                    break
                user_input = self.console.input("[bold green]You:[/bold green] ")
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session terminated by user.[/yellow]")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                self.console.print("\n[red]An unexpected error occurred. The application will now exit.[/red]")
                break

def main():
    """Main entry point for the application."""
    try:
        from custom_llm import llm
        # from openai_llm import model as llm
        from tools import (
            search_cve_by_keyword_brief,
            search_cve_by_keyword_and_date,
            search_cve_by_keyword,
            search_cveID_by_keyword,
            search_cve_by_cveid,
            search_cve_by_keyword_and_window,
            convert_cve_list_to_str,
        )
        
        tools = [
            search_cve_by_keyword_brief,
            search_cve_by_keyword_and_date,
            search_cve_by_keyword,
            search_cveID_by_keyword,
            search_cve_by_cveid,
            search_cve_by_keyword_and_window,
            convert_cve_list_to_str,
            ]
        cli = SecurityAnalystCLI(llm=llm, tools=tools)
        cli.run()
    except ImportError as e:
        logger.error(f"Failed to import required modules: {str(e)}")
        print("Please ensure all required modules are installed.")
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        print("The application encountered an error and could not start.")

if __name__ == "__main__":
    main()