from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from .analyzer import TimeComplexityAnalyzer

# ML Integration
try:
    from .ml_integration_simple import analyze_with_ml, ML_AVAILABLE
    print(f"🤖 ML Integration: {'Available' if ML_AVAILABLE else 'Not Available'}")
except ImportError:
    print("⚠️ ML Integration not available")
    ML_AVAILABLE = False
    analyze_with_ml = None

app = FastAPI(
    title="TimeComplexity Analyzer API",
    description="API for analyzing time and space complexity of code",
    version="1.0.0"
)

# Add CORS middleware for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Chrome extension
    allow_credentials=False,  # Set to False for Chrome extension
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
)

class AnalysisRequest(BaseModel):
    code: str
    language: str

class AnalysisResponse(BaseModel):
    time_complexity: str
    space_complexity: str
    breakdown: List[str]
    suggestions: List[str]
    confidence: float

# Initialize the analyzer
analyzer = TimeComplexityAnalyzer()

@app.get("/")
async def root():
    return {
        "message": "TimeComplexity Analyzer API",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    """
    Analyze the time and space complexity of the provided code.
    
    Args:
        request: AnalysisRequest containing code and language
        
    Returns:
        AnalysisResponse with complexity analysis results
    """
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        if request.language not in ["python", "cpp", "java", "javascript", "c", "go", "rust"]:
            raise HTTPException(status_code=400, detail="Unsupported language")
        
        # Perform analysis
        result = analyzer.analyze(request.code, request.language)
        
        return AnalysisResponse(
            time_complexity=result["time_complexity"],
            space_complexity=result["space_complexity"],
            breakdown=result["breakdown"],
            suggestions=result["suggestions"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "analyzer": "ready"}

@app.options("/analyze")
async def analyze_options():
    """Handle OPTIONS requests for /analyze endpoint"""
    return {"message": "OK"}

@app.options("/analyze-ml")
async def analyze_ml_options():
    """Handle OPTIONS requests for /analyze-ml endpoint"""
    return {"message": "OK"}

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": ["python", "cpp", "java", "javascript", "c", "go", "rust"],
        "features": {
            "python": ["AST parsing", "Loop detection", "Recursion analysis"],
            "cpp": ["AST parsing", "Loop detection", "Recursion analysis"],
            "java": ["AST parsing", "Loop detection", "Recursion analysis"],
            "javascript": ["AST parsing", "Loop detection", "Recursion analysis"],
            "c": ["Pattern matching", "Loop detection", "Recursion analysis"],
            "go": ["Pattern matching", "Loop detection", "Recursion analysis"],
            "rust": ["Pattern matching", "Loop detection", "Recursion analysis"]
        }
    }


@app.post("/analyze-ml")
async def analyze_with_ml_endpoint(request: AnalysisRequest):
    """Analyze code using ML-enhanced approach"""
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        if request.language not in ["python", "cpp", "java", "javascript", "c", "go", "rust"]:
            raise HTTPException(status_code=400, detail="Unsupported language")
        
        if analyze_with_ml and ML_AVAILABLE:
            result = analyze_with_ml(request.code, request.language)
            return result
        else:
            # Fallback to regular analysis
            result = analyzer.analyze(request.code, request.language)
            return AnalysisResponse(
                time_complexity=result["time_complexity"],
                space_complexity=result["space_complexity"],
                breakdown=result["breakdown"],
                suggestions=result["suggestions"],
                confidence=result["confidence"]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 