import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()


def create_search_agent():
    """Create a search agent using Tavily search tool."""
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )
    
    
    # Initialize Tavily search tool
    search_tool = TavilySearch(
        max_results=5,
        search_depth="advanced",
    )
    
    # Create the agent using the new API
    agent = create_agent(
        model=llm,
        tools=[search_tool],
        debug=True,  # Enables verbose output
    )
    
    return agent


def format_agent_output(result, query):
    """Format and display agent output in a beautiful way."""
    console.print("\n")
    
    # Display query in a beautiful panel
    query_panel = Panel(
        Text(query, style="bold cyan"),
        title="[bold yellow]🔍 Search Query[/bold yellow]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(query_panel)
    console.print()
    
    if "messages" in result:
        messages = result["messages"]
        
        # Create a table to show agent steps
        steps_table = Table(
            title="[bold green]Agent Execution Steps[/bold green]",
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            border_style="green",
        )
        steps_table.add_column("Step", style="cyan", width=8)
        steps_table.add_column("Type", style="yellow", width=15)
        steps_table.add_column("Content", style="white", overflow="fold")
        
        step_num = 1
        tool_calls = []
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                steps_table.add_row(
                    str(step_num),
                    "[bold blue]Human[/bold blue]",
                    msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                )
                step_num += 1
            elif isinstance(msg, AIMessage):
                content_preview = str(msg.content)[:150] + "..." if len(str(msg.content)) > 150 else str(msg.content)
                steps_table.add_row(
                    str(step_num),
                    "[bold green]AI Agent[/bold green]",
                    content_preview,
                )
                step_num += 1
                
                # Check for tool calls
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_calls.append(tool_call)
                        # Handle both dict and object formats
                        if isinstance(tool_call, dict):
                            tool_name = tool_call.get('name', 'unknown')
                            tool_args = str(tool_call.get('args', {}))[:80]
                        else:
                            tool_name = getattr(tool_call, 'name', 'unknown')
                            tool_args = str(getattr(tool_call, 'args', {}))[:80]
                        steps_table.add_row(
                            "",
                            "[bold yellow]🔧 Tool Call[/bold yellow]",
                            f"[cyan]{tool_name}[/cyan] - {tool_args}",
                        )
            elif isinstance(msg, ToolMessage):
                content_preview = str(msg.content)[:150] + "..." if len(str(msg.content)) > 150 else str(msg.content)
                steps_table.add_row(
                    str(step_num),
                    "[bold magenta]Tool Result[/bold magenta]",
                    content_preview,
                )
                step_num += 1
        
        console.print(steps_table)
        console.print()
        
        # Display final result in a beautiful panel
        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and hasattr(last_message, "content"):
            final_result = last_message.content
            
            result_panel = Panel(
                Markdown(final_result),
                title="[bold green]✨ Final Result[/bold green]",
                border_style="green",
                box=box.DOUBLE,
                padding=(1, 2),
            )
            console.print(result_panel)
        else:
            # Fallback for other message types
            result_panel = Panel(
                str(last_message),
                title="[bold green]✨ Final Result[/bold green]",
                border_style="green",
                box=box.DOUBLE,
                padding=(1, 2),
            )
            console.print(result_panel)
    else:
        # Fallback if structure is different
        result_panel = Panel(
            str(result),
            title="[bold green]✨ Result[/bold green]",
            border_style="green",
            box=box.DOUBLE,
            padding=(1, 2),
        )
        console.print(result_panel)


def main():
    """Main function to run the search agent."""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]❌ Error: OPENAI_API_KEY not found in environment variables[/bold red]")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        console.print("[bold red]❌ Error: TAVILY_API_KEY not found in environment variables[/bold red]")
        console.print("[yellow]You can get a free API key from https://tavily.com/[/yellow]")
        return
    
    # Create the search agent
    with console.status("[bold green]Initializing agent...", spinner="dots"):
        agent = create_search_agent()
    
    # Example query
    query = "search for 3 job postings for an Digital Marketing Director in the bangalore on linkedin and list their details?"
    
    # Execute the search with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Agent is thinking and searching...", total=None)
        result = agent.invoke({"messages": [HumanMessage(content=query)]})
        progress.update(task, completed=True)
    
    # Format and display the result beautifully
    format_agent_output(result, query)


if __name__ == "__main__":
    main()
