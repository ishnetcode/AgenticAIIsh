from crewai import Agent, Task, Crew, Process, LLM
from crewai.tasks.output_format import OutputFormat
from crewai.tools import tool
import json

model= LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

@tool
def forward_email(category: str) -> str:
    """Clear description for what this tool is useful for, your agent will need this information to use it."""
    forwarding_rules = {
            "claims_enquiry": "claims.handler@insurancecompany.com",
            "price_enquiry": "sales@insurancecompany.com",
            "customer_complaint": "complaints@insurancecompany.com",
            "product_enquiry": "products@insurancecompany.com",
            "customer_feedback": "feedback@insurancecompany.com",
            "off_topic": "support@insurancecompany.com"
        }
    to_email = forwarding_rules.get(category, "general@example.com")
    return (f"Email forwarded to: {to_email}\n successfully.")

emails = [
  {
    "sender": "claimant@example.com",
    "receiver": "insurance@example.com",
    "subject": "Claim Status Inquiry",
    "body": "I am reaching out to check the status of my insurance claim, [Claim Number], which I submitted on [Submission Date]. I have not yet received any updates and would appreciate any information regarding its progress.",
    "date": "2022-01-01T12:00:00"
  },
  {
    "sender": "policyholder@example.com",
    "receiver": "insurance@example.com",
    "subject": "Policy Issue - Urgent Attention Required",
    "body": "I am writing to formally express my dissatisfaction with the handling of my insurance policy, [Policy Number]. Despite my repeated attempts to resolve the issue, I have yet to receive a satisfactory response. I am concerned about the lack of communication and resolution, and would like to know what action should be taken?",
    "date": "2022-01-05T14:00:00"
  },
  {
    "sender": "customer@example.com",
    "receiver": "insurance@example.com",
    "subject": "Feedback on Online Policy Purchase",
    "body": "I wanted to take a moment to share my feedback regarding my recent experience with your insurance services. I appreciate the ease of purchasing my policy online. It was a smooth process, and I felt well-guided throughout.",
    "date": "2022-01-10T10:00:00"
  },
  {
    "sender": "test@example.com",
    "receiver": "support@example.com",
    "subject": "Poor Service Experience - Claim Process",
    "body": "Dear Support Team,I am very disappointed with the service I received during my recent claim process. The representative was unhelpful and the process took much longer than expected. Please address this issue immediately.Regards,test",
    "date": "2022-01-15T16:00:00"
  }
]

email_categories = Agent(
    role='Email Categorizer Agent',
    goal="""take in a email from a human that has emailed out company email address and categorize it \
    into one of the following categories: \
    claims_enquiry - used when someone is asking for thier claim status \
    price_enquiry - used when someone is asking for information about pricing \
    customer_complaint - used when someone is complaining about something \
    product_enquiry - used when someone is asking for information about a product feature, benefit or service but not about pricing \\
    customer_feedback - used when someone is giving feedback about a product \
    off_topic when it doesnt relate to any other category """,
    backstory="""You are a master email categorizer at understanding what a customer wants when they write an email and are able to categorize it in a useful way""",
    verbose=True,
    allow_delegation=False,
    llm=model)

forwarder_agent = Agent(
    role="Email Forwarder",
    goal="Forward emails to the appropriate department based on category.",
    backstory="You are an AI that forwards emails to the correct department after categorizing them.",
    tools=[forward_email],  # Add the forwarding function as a tool
    verbose=True,
    llm=model)

# responder = Agent(
#     role = "email support agent",
#     goal = "respond to emails based on their importance",
#     backstory = "You are an AI assistant that helps people manage their emails. You have been trained on a dataset"
#                 "of emails that have been labeled as spam, important, or casual. You have been trained to respond to emails"
#                 "based on their importance.",
#     verbose = True,
#     allow_delegation=False,
#     llm=model)

catagorisation_tasks = []

# Loop through each email and create a classification task
for email in emails:
    catagorise_email_task = Task(
        description=f"Categorise the email: {email['subject']}\n{email['body']}",
        agent=email_categories,
        expected_output="One of these categories: claims_enquiry, price_equiry, customer_complaint, product_enquiry, customer_feedback, off_topic",
        # output_file='outcome1.json',
        # output_format=OutputFormat.JSON
    )
    
    forward_task = Task(
        description="Forward the email based on its classification.",
        agent=forwarder_agent,
        context=[catagorise_email_task],  # Pass the output of classify_task as context
        expected_output="A confirmation that the email has been forwarded to the correct department, including the email body."
    )
    # catagorisation_tasks.append(catagorise_email_task, forward_task)

    # respond_to_email = Task(
    #     description = f"Respond to the email: {email}",
    #     agent = responder,
    #     expected_output = "A response to the email",
    # )

    email_crew = Crew(
        agents = [email_categories, forwarder_agent],
        tasks = [catagorise_email_task, forward_task],
        verbose = False,
        process = Process.sequential
    )

    result = email_crew.kickoff(inputs={"email": email})
    # Print the result for the current email
    print(f"Processing Email from {email['sender']} to {email['receiver']}")
    print(result)
    print("-" * 40)  # Separator for readability
    
# print(output.tasks_output)
# Extract the relevant data from the CrewOutput object
# data = []
# for task in output.tasks_output:
#     data.append({
#         'category': task.raw,
#         'input': task.description
#     })

# # Write the data to a JSON file
# with open('outcome.json', 'w') as f:
#     json.dump(data, f)