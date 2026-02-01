import os
import streamlit as st
import google.generativeai as genai

# Configure Gemini safely
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use a valid model name
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Resume Matcher")

# Upload resume file
resume_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])

# Job description input
job_description = st.text_area("Paste Job Description")

if resume_file and job_description:
    # Read resume text
    resume_text = resume_file.read().decode("utf-8")

    # Try to extract candidate name (first line of resume assumed to be name)
    candidate_name = resume_text.splitlines()[0].strip()

    if st.button("Analyze"):
        prompt = f"""
        Compare the following resume with the job description and give a match percentage only.
        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Respond with just a number between 0 and 100.
        """
        try:
            response = model.generate_content(prompt)
            score = response.text.strip()

            st.success(f"Candidate: {candidate_name}\nMatch Score: {score}%")

            # Prepare text for Notepad file
            result_text = f"Candidate: {candidate_name}\nMatch Score: {score}%"

            # Download button for result file
            st.download_button(
                "Download Result",
                result_text,
                file_name="resume_match.txt"
            )

        except Exception as e:
            st.error(f"API Error: {e}")