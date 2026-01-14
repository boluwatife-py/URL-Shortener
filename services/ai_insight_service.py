from typing import List
from google import genai
from fastapi import HTTPException
from schemas.analytics import LinkAnalyticsResponse
from core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class AIInsightService:
    async def generate_insights(
        self,
        analytics: List[LinkAnalyticsResponse],
        user_prompt: str
    ) -> str:

        if not user_prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")


        analytics_summary = ""
        if analytics:
            for link in analytics:
                per_day_text = ", ".join(
                    f"{cp.day}: {cp.clicks} clicks" for cp in link.clicks_per_day
                ) or "no daily clicks"
                source_text = ", ".join(
                    f"{src.source} ({src.clicks})" for src in link.clicks_by_source
                ) or "no sources recorded"
                analytics_summary += (
                    f"Link {link.shortended_url} ({link.url}): "
                    f"{link.total_clicks} total clicks; "
                    f"daily breakdown: {per_day_text}; "
                    f"sources: {source_text}.\n"
                )


        final_prompt = user_prompt
        if analytics_summary:
            final_prompt += "\n\nHere is your analytics data:\n" + analytics_summary

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )
            return response.text  # type: ignore

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini generation failed: {str(e)}")
