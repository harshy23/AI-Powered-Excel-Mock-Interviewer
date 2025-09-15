from django.shortcuts import render ,redirect
from django.contrib import messages
from pydantic_ai import Agent
from pydantic_ai.tools import RunContext
# Create your views here.
def index(request):
    return render(request , 'index.html')


SYSTEM_PROMPT = (
    "You are an expert Excel skills interviewer at a finance and analytics company. "
    "Conduct a realistic, multi-turn mock interview with the user to evaluate their advanced Excel skills. "
    "Start the conversation by introducing yourself and briefly describing the interview process. "
    "Ask one challenging but relevant Excel interview question at a time, wait for the candidate’s answer, then analyze it for technical accuracy, depth, and clarity. "
    "After each response, provide a brief evaluation and resume the interview until finished. "
    "At the end, generate a clear and constructive feedback summary highlighting strengths, weaknesses, and readiness for the job. "
    "Keep your tone professional, neutral, and supportive. Do not give model answers until the end of the interview."
)




flow_agent = Agent[None](
    "openai:gpt-4o-mini",
    system_prompt=SYSTEM_PROMPT,
)

def aimodel(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        if not prompt:
            return render(request, "index.html", {"error": "Please enter a question."})

        try:
            result = flow_agent.run_sync(
                f"User question: {prompt}\nPlease respond as the Excel interviewer."
            )
            response_text = result.output
            return render(request, "index.html", {"response": response_text})
        except Exception as e:
            return render(request, "index.html", {"error": f"AI processing failed: {str(e)}"})
    
    # For GET or any other method, just show the form page
    return render(request, "index.html")

