"""
GründerAI Assessment API
FastAPI backend for Gründungszuschuss readiness assessment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import os

# Import assessment engine (we'll create this next)
from assessment.engine import AssessmentEngine
from assessment.questions import get_question_bank

# Initialize FastAPI app
app = FastAPI(
    title="GründerAI Assessment API",
    description="Scientific assessment for Gründungszuschuss applications",
    version="1.0.0"
)

# CORS configuration - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:5173",  # Vite dev server
        "https://gruenderai-frontend.vercel.app",   # Vercel preview deployments
        "https://gruenderai.com", # Production domain (update with yours)
        "https://www.gruenderai.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (for MVP - use Redis/PostgreSQL later)
sessions = {}

# Initialize assessment engine
assessment_engine = AssessmentEngine()

# ============================================================================
# DATA MODELS
# ============================================================================

class StartAssessmentRequest(BaseModel):
    user_id: Optional[str] = None
    language: str = "de"

class StartAssessmentResponse(BaseModel):
    session_id: str
    total_questions: int
    estimated_time_minutes: int
    first_question: Dict[str, Any]

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: Any  # Can be string, number, list, etc.

class SubmitAnswerResponse(BaseModel):
    next_question: Optional[Dict[str, Any]]
    progress: int  # Percentage
    is_complete: bool

class GetResultsRequest(BaseModel):
    session_id: str

class AssessmentResults(BaseModel):
    session_id: str
    overall_score: float
    readiness_level: str  # "Hoch", "Mittel", "Niedrig"
    dimensions: Dict[str, Any]
    recommendations: List[str]
    next_steps: List[str]
    completion_time: str

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "GründerAI Assessment API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "active_sessions": len(sessions),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/assessment/start", response_model=StartAssessmentResponse)
async def start_assessment(request: StartAssessmentRequest):
    """
    Start a new assessment session
    Returns the first question and session ID
    """
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Initialize session
        session_data = {
            "session_id": session_id,
            "user_id": request.user_id or str(uuid.uuid4()),
            "language": request.language,
            "started_at": datetime.utcnow().isoformat(),
            "current_question_index": 0,
            "answers": {},
            "scores": {}
        }
        
        # Store session
        sessions[session_id] = session_data
        
        # Get first question
        first_question = assessment_engine.get_next_question(session_data)
        
        return StartAssessmentResponse(
            session_id=session_id,
            total_questions=assessment_engine.total_questions,
            estimated_time_minutes=10,
            first_question=first_question
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start assessment: {str(e)}")

@app.post("/api/assessment/answer", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """
    Submit an answer and get the next question
    """
    try:
        # Validate session
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[request.session_id]
        
        # Store answer
        session_data["answers"][request.question_id] = {
            "answer": request.answer,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update progress
        session_data["current_question_index"] += 1
        
        # Check if assessment is complete
        is_complete = session_data["current_question_index"] >= assessment_engine.total_questions
        
        # Get next question or None if complete
        next_question = None if is_complete else assessment_engine.get_next_question(session_data)
        
        # Calculate progress
        progress = int((session_data["current_question_index"] / assessment_engine.total_questions) * 100)
        
        return SubmitAnswerResponse(
            next_question=next_question,
            progress=progress,
            is_complete=is_complete
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")

@app.post("/api/assessment/results", response_model=AssessmentResults)
async def get_results(request: GetResultsRequest):
    """
    Calculate and return assessment results
    """
    try:
        # Validate session
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_data = sessions[request.session_id]
        
        # Calculate results
        results = assessment_engine.calculate_results(session_data)
        
        # Format response
        return AssessmentResults(
            session_id=request.session_id,
            overall_score=results["overall_score"],
            readiness_level=results["readiness_level"],
            dimensions=results["dimensions"],
            recommendations=results["recommendations"],
            next_steps=results["next_steps"],
            completion_time=datetime.utcnow().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate results: {str(e)}")

@app.get("/api/assessment/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Get current session information (for debugging/resuming)
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    
    return {
        "session_id": session_id,
        "progress": int((session_data["current_question_index"] / assessment_engine.total_questions) * 100),
        "answers_count": len(session_data["answers"]),
        "started_at": session_data["started_at"]
    }

# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code
    }

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    print("🚀 GründerAI Assessment API starting...")
    print(f"📊 Question bank loaded: {assessment_engine.total_questions} questions")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 GründerAI Assessment API shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
