
import os
from openai import OpenAI


# ============================================================
# OPENAI CLIENT
# ============================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY is not set.")
    print('Run this in PowerShell:')
    print('$env:OPENAI_API_KEY="YOUR_API_KEY"')
    exit()

client = OpenAI(api_key=api_key)

# Use a model available to your API account.
MODEL = "gpt-5.6-luna"


# ============================================================
# 1. PLANNING
# ============================================================

def create_plan(topic):

    print("\n[1] Creating research plan...")

    prompt = f"""
You are a research planner.

Topic:
{topic}

Create a simple research plan.

Include:
1. Main objective
2. Important subtopics
3. Important questions
4. Suggested structure for the final content

Keep the plan clear and organized.
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# 2. RESEARCH NOTES
# ============================================================

def research_topic(topic, plan):

    print("\n[2] Creating research notes...")

    prompt = f"""
You are a research assistant.

Topic:
{topic}

Research Plan:
{plan}

Create useful research notes based on the plan.

Include:
- Important facts
- Explanations
- Examples
- Key points

Do not create the final article yet.
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# 3. FIRST DRAFT
# ============================================================

def generate_draft(topic, research):

    print("\n[3] Generating first draft...")

    prompt = f"""
Write a clear article about:

{topic}

Use these research notes:

{research}

Requirements:
- Clear introduction
- Proper headings
- Simple language
- Useful examples
- Good conclusion
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# 4. REFLECTION
# ============================================================

def reflect_on_content(topic, draft):

    print("\n[4] Reflecting on the draft...")

    prompt = f"""
You are a critical reviewer.

Review this article.

Topic:
{topic}

Draft:
{draft}

Check the following:

1. Missing information
2. Logical structure
3. Clarity
4. Repetition
5. Accuracy problems
6. Weak explanations
7. Whether the topic is properly covered

Give clear suggestions for improvement.
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# 5. FINAL IMPROVEMENT
# ============================================================

def improve_content(topic, draft, reflection):

    print("\n[5] Improving final content...")

    prompt = f"""
Create the final improved article.

Topic:
{topic}

Original Draft:
{draft}

Reflection:
{reflection}

Use the reflection to improve the article.

Requirements:
- Correct problems
- Add missing information
- Remove unnecessary repetition
- Improve clarity
- Keep simple language
- Use proper headings
- Give a strong conclusion

Return ONLY the final article.
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


# ============================================================
# MAIN WORKFLOW
# ============================================================

def deep_research_workflow(topic):

    # Step 1: Planning
    plan = create_plan(topic)

    # Step 2: Research
    research = research_topic(topic, plan)

    # Step 3: Draft
    draft = generate_draft(topic, research)

    # Step 4: Reflection
    reflection = reflect_on_content(topic, draft)

    # Step 5: Final answer
    final_content = improve_content(
        topic,
        draft,
        reflection
    )

    return plan, research, draft, reflection, final_content


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("       DEEP RESEARCH WORKFLOW")
    print("       Planning + Reflection")
    print("=" * 60)

    topic = input("\nEnter your research topic: ")

    if not topic.strip():
        print("Please enter a topic.")
        exit()

    try:

        plan, research, draft, reflection, final_content = \
            deep_research_workflow(topic)

        print("\n")
        print("=" * 60)
        print("RESEARCH PLAN")
        print("=" * 60)
        print(plan)

        print("\n")
        print("=" * 60)
        print("RESEARCH NOTES")
        print("=" * 60)
        print(research)

        print("\n")
        print("=" * 60)
        print("REFLECTION")
        print("=" * 60)
        print(reflection)

        print("\n")
        print("=" * 60)
        print("FINAL CONTENT")
        print("=" * 60)
        print(final_content)

    except Exception as e:

        print("\nERROR:")
        print(e)