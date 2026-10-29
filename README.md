# Python AI Chatbot (Flask + Groq)

A simple web chatbot with Auto detect, IT, Medical / Health, and Share Market topics.

## Run locally

1. Install Python 3.10+ (Python 3.13 is configured for Vercel).
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your real Groq API key:

   ```env
   GROQ_API_KEY=your_real_key_here
   GROQ_MODEL=openai/gpt-oss-20b
   ```

5. Start the server:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Deploy to Vercel

1. Push this folder to a GitHub repository. Do not upload `.env`.
2. Import the repository at https://vercel.com/new.
3. In Vercel project Settings → Environment Variables, add `GROQ_API_KEY` with your real key. Optionally add `GROQ_MODEL`.
4. Redeploy the project.

The app uses `public/style.css` because Vercel serves files in `public/` as static assets.

## Important

- Never publish your real API key in GitHub or frontend JavaScript.
- Medical answers are general information and are not a substitute for professional care.
- Share-market answers are educational and not personalized financial advice.
